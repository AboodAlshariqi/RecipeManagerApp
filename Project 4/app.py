import numpy as np
import streamlit as st
import tensorflow as tf

# copied from the notebook (the folders are read in alphabetical order)
class_names = ['0.5 BHD', '1 BHD', '10 BHD', '20 BHD', '5 BHD']

IMG_SIZE = (64, 64)


@st.cache_resource
def get_model():
    return tf.keras.models.load_model("currency_model.keras")


def prepare(data):
    """Same steps as the notebook: decode the picture, resize it to 64x64,
    turn it back into whole numbers, then divide by 255."""
    img = tf.io.decode_image(data, channels=3, expand_animations=False)
    img = tf.image.resize(img, IMG_SIZE, method='bilinear')
    return np.array(img.numpy(), dtype='uint8') / 255


st.title("Bahraini Banknote Recognition")
st.write("Take a photo of a banknote or upload one, and the model will say which it is.")

# I tested the model on banknotes it had never seen before. When the note
# filled most of the picture it got 4 out of 5 right, but when the note was
# small in the picture it was no better than guessing, because then most of
# the picture is background. So the most useful thing the app can do is tell
# people to hold the note close.
st.info("Hold the note close so it fills most of the picture. "
        "If the note is small the answer will probably be wrong.")

photo = st.camera_input("Take a photo")
file = st.file_uploader("Or choose a picture", type=["jpg", "jpeg", "png"])

data = None
if photo is not None:
    data = photo.getvalue()
elif file is not None:
    data = file.getvalue()
    st.image(data, width=300)

if data is not None:
    x = prepare(data)
    pred = get_model().predict(np.expand_dims(x, axis=0), verbose=0)[0]

    order = np.argsort(pred)[::-1]
    best, second = order[0], order[1]

    st.header(class_names[best])
    st.write(f"Confidence: {pred[best] * 100:.1f}%")

    # if the top two are close together the model is really just guessing
    if pred[best] < 0.6 or (pred[best] - pred[second]) < 0.2:
        st.warning("Not sure about this one. Try better light, hold the note "
                   "flatter, or fill more of the picture with the note.")

    for i in order:
        st.write(f"{class_names[i]} - {pred[i] * 100:.1f}%")
