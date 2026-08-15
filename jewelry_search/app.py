"""Jewelry Visual Search - Streamlit app.

Upload or photograph a piece of jewelry and get the closest visual matches from the
catalog, using a MobileNetV2 embedding and a ChromaDB similarity index.

Run:
    py -3.13 -m streamlit run app.py
"""

import os

# Don't let TensorFlow claim every core on a laptop.
THREADS = max(1, (os.cpu_count() or 4) // 2)
os.environ["OMP_NUM_THREADS"] = str(THREADS)
os.environ["TF_NUM_INTEROP_THREADS"] = str(THREADS)
os.environ["TF_NUM_INTRAOP_THREADS"] = str(THREADS)

import chromadb
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.utils import img_to_array

tf.config.threading.set_intra_op_parallelism_threads(THREADS)
tf.config.threading.set_inter_op_parallelism_threads(THREADS)

HERE = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(HERE, "data", "chroma_store")
COLLECTION_NAME = "jewelry_images"
IMG_SIZE = (224, 224)
TOP_K = 25
# Cosine distance = 1 - cosine_similarity, so 0 = identical, 2 = opposite. Same-category
# jewelry pairs tend to land around 0.20-0.24 distance, unrelated pairs around 0.55+, so
# 0.60 is a reasonable default cutoff for "probably not actually similar."
DEFAULT_DISTANCE_THRESHOLD = 0.60

st.set_page_config(page_title="Jewelry Visual Search", page_icon="💍", layout="wide")


# ----------------------------------------------------------------------------- caching

@st.cache_resource(show_spinner="Loading MobileNetV2...")
def load_backbone():
    backbone = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
    backbone.trainable = False
    return backbone


@st.cache_resource(show_spinner="Loading the saved index...")
def load_collection():
    if not os.path.isdir(CHROMA_DIR):
        return None
    client = chromadb.PersistentClient(
        path=CHROMA_DIR, settings=chromadb.Settings(anonymized_telemetry=False)
    )
    names = [c.name for c in client.list_collections()]
    if COLLECTION_NAME not in names:
        return None
    return client.get_collection(COLLECTION_NAME)


# ------------------------------------------------------------------------- embedding

def preprocess_img(pil_img):
    img = pil_img.convert("RGB").resize(IMG_SIZE)
    img_array = img_to_array(img)
    return preprocess_input(img_array)


def extract_embedding(backbone, pil_img):
    preprocessed_img = preprocess_img(pil_img)
    batch = np.expand_dims(preprocessed_img, axis=0)
    embedding = backbone.predict(batch, verbose=0)
    return embedding  # shape (1, 1280)


# --------------------------------------------------------------------------------- UI

st.title("💍 Jewelry Visual Search")
st.caption("Upload a photo of a ring or necklace to find visually similar pieces in the catalog.")

backbone = load_backbone()
collection = load_collection()

if collection is None:
    st.error(
        "No saved index found. Run `prepare_data.py` first - it builds the ChromaDB "
        "collection this app loads from `data/chroma_store`."
    )
    st.stop()

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Number of matches to show", 5, TOP_K, TOP_K)
    threshold = st.slider(
        "Similarity threshold (max distance)", 0.10, 1.00, DEFAULT_DISTANCE_THRESHOLD, 0.05,
        help="Matches with a cosine distance above this are treated as not similar - "
             "this is what keeps an unrelated query (a phone, a shoe) from returning 25 "
             "confident-looking but meaningless jewelry matches.",
    )
    st.caption(f"Catalog size: {collection.count()} images")

src = st.radio("Image source", ["Upload", "Camera"], horizontal=True, label_visibility="collapsed")
query_img = None

if src == "Upload":
    up = st.file_uploader("Choose a jewelry photo", type=["jpg", "jpeg", "png", "webp", "bmp"])
    if up:
        query_img = Image.open(up)
else:
    shot = st.camera_input("Take a photo")
    if shot:
        query_img = Image.open(shot)

if query_img is None:
    st.info("Upload a photo or take one to search the catalog.")
    st.stop()

left, right = st.columns([1, 2])
with left:
    st.image(query_img, caption="Query image", use_container_width=True)

with st.spinner("Searching..."):
    query_embedding = extract_embedding(backbone, query_img)
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=["metadatas", "distances", "uris"],
    )

uris = results["uris"][0]
distances = results["distances"][0]
categories = [m.get("category", "?") for m in results["metadatas"][0]]

kept = [(u, d, c) for u, d, c in zip(uris, distances, categories) if d <= threshold]

with right:
    if not kept:
        st.warning(
            f"No similar items found within the current threshold "
            f"(best match distance was {min(distances):.2f}, threshold is {threshold:.2f}). "
            f"Try raising the threshold in the sidebar, or this may just not be a jewelry photo."
        )
    else:
        st.subheader(f"Top {len(kept)} matches")
        cols_per_row = 5
        for row_start in range(0, len(kept), cols_per_row):
            row = kept[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            for col, (uri, dist, cat) in zip(cols, row):
                with col:
                    st.image(uri, use_container_width=True)
                    similarity = 1 - dist
                    st.caption(f"{cat} · similarity {similarity:.2f}")

        if len(kept) < len(uris):
            st.caption(
                f"{len(uris) - len(kept)} further match(es) from the raw top-{top_k} were "
                f"below the similarity threshold and hidden."
            )
