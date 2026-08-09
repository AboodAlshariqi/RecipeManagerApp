import os

import numpy as np
import streamlit as st
import tensorflow as tf

# copied from the notebook (the folders are read in alphabetical order)
class_names = ['0.5 BHD', '1 BHD', '10 BHD', '20 BHD', '5 BHD']

# how much each note is worth, for adding up the total
values = {'0.5 BHD': 0.5, '1 BHD': 1.0, '5 BHD': 5.0,
          '10 BHD': 10.0, '20 BHD': 20.0}

IMG_SIZE = (64, 64)

# Look for the model next to this file. Streamlit Cloud starts the app from
# the top of the repository, not from this folder, so a plain file name fails.
HERE = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def get_model():
    return tf.keras.models.load_model(os.path.join(HERE, "currency_model.keras"))


def prepare(data):
    """Same steps as the notebook: decode the picture, resize it to 64x64,
    turn it back into whole numbers, then divide by 255."""
    img = tf.io.decode_image(data, channels=3, expand_animations=False)
    img = tf.image.resize(img, IMG_SIZE, method='bilinear')
    return np.array(img.numpy(), dtype='uint8') / 255


# Streamlit runs this whole file again every time you click something, so a
# normal list would be emptied each time. session_state is remembered.
if "history" not in st.session_state:
    st.session_state.history = []


st.title("Bahraini Banknote Counter")
st.write("Take a photo of each note. The app adds them up for you.")

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

    # The model is right about 9 times out of 10, so let the person fix it
    # before it goes into the total. A wrong note makes the whole sum wrong.
    st.write("---")
    choice = st.selectbox("Add this note as:", class_names, index=int(best))

    if st.button("Add to the total"):
        st.session_state.history.append(choice)


# ---- the running total ---------------------------------------------------
st.write("---")
st.subheader("Notes counted so far")

if len(st.session_state.history) == 0:
    st.write("Nothing counted yet.")
else:
    total = sum(values[name] for name in st.session_state.history)

    st.metric("Total", f"{total:.2f} BHD")
    st.write(f"{len(st.session_state.history)} notes")

    # how many of each note, in the order they appear on screen
    st.write("**How many of each:**")
    for name in ['0.5 BHD', '1 BHD', '5 BHD', '10 BHD', '20 BHD']:
        n = st.session_state.history.count(name)
        if n > 0:
            st.write(f"{n} x {name} = {n * values[name]:.2f} BHD")

    st.write("**In the order I counted them:**")
    st.write(", ".join(st.session_state.history))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Remove the last one"):
            st.session_state.history.pop()
            st.rerun()
    with col2:
        if st.button("Start again"):
            st.session_state.history = []
            st.rerun()
