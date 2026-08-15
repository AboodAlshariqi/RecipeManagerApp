"""Builds embeddings for the jewelry catalog and indexes them in ChromaDB.

Run once (or whenever data/Jewellery_Data changes):
    py -3.13 prepare_data.py
"""

import os

# Cap TensorFlow's thread pools before importing it, so it doesn't grab every core.
THREADS = max(1, (os.cpu_count() or 4) // 2)
os.environ["OMP_NUM_THREADS"] = str(THREADS)
os.environ["TF_NUM_INTEROP_THREADS"] = str(THREADS)
os.environ["TF_NUM_INTRAOP_THREADS"] = str(THREADS)

import glob
import time

import chromadb
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.utils import img_to_array, load_img
from tqdm import tqdm

tf.config.threading.set_intra_op_parallelism_threads(THREADS)
tf.config.threading.set_inter_op_parallelism_threads(THREADS)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data", "Jewellery_Data")
CHROMA_DIR = os.path.join(HERE, "data", "chroma_store")
COLLECTION_NAME = "jewelry_images"
IMG_SIZE = (224, 224)


# include_top=False strips the classification head, pooling="avg" collapses the feature
# maps to a single 1280-D vector per image.
print("loading MobileNetV2 (ImageNet weights, no classification head)...")
backbone = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
backbone.trainable = False


def preprocess_img(img_path):
    img = load_img(img_path, target_size=IMG_SIZE)
    img_array = img_to_array(img)
    preprocessed_img = preprocess_input(img_array)
    return preprocessed_img


def extract_embedding(img_path):
    preprocessed_img = preprocess_img(img_path)
    img = np.expand_dims(preprocessed_img, axis=0)
    embedding = backbone.predict(img, verbose=0)
    return embedding


if __name__ == "__main__":
    t0 = time.time()

    image_paths = sorted(glob.glob(os.path.join(DATA_DIR, "*", "*.jpg")))
    categories = [os.path.basename(os.path.dirname(p)) for p in image_paths]
    print(f"found {len(image_paths)} images across {len(set(categories))} categories: "
          f"{sorted(set(categories))}")
    print(f"using {THREADS} CPU thread(s) of {os.cpu_count()} available")

    feature_list = []
    for img_path in tqdm(image_paths, desc="Embedding"):
        feature_list.append(extract_embedding(img_path))

    feature_list = np.squeeze(np.array(feature_list))
    print(f"embeddings: {feature_list.shape}")

    os.makedirs(CHROMA_DIR, exist_ok=True)
    chroma_client = chromadb.PersistentClient(
        path=CHROMA_DIR, settings=chromadb.Settings(anonymized_telemetry=False)
    )
    existing = [c.name for c in chroma_client.list_collections()]
    if COLLECTION_NAME in existing:
        chroma_client.delete_collection(COLLECTION_NAME)
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    ids = [str(i) for i in range(len(feature_list))]
    collection.add(
        ids=ids,
        embeddings=feature_list.tolist(),
        uris=image_paths,
        metadatas=[{"category": c} for c in categories],
    )
    print(f"saved {collection.count()} items to ChromaDB at {CHROMA_DIR}")

    print(f"done in {time.time() - t0:.1f}s")
