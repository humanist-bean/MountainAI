"""
streamlit_server.py

Description:
Incredibly simple web app that can be used to test .pkl models

Source (copied and pasted):
https://medium.com/@sumitredekar/deep-learning-image-classification-using-pytorch-fastai-v2-on-colab-c2ab4aa7fdbf
"""

import pathlib
from pathlib import Path

import streamlit as st
from fastai.vision.all import *
from fastai.vision.widgets import *

#BELOW 2 LINES MAY NEED TO BE UNCOMMENTED AND RUN IN WINDOWS
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath

learn_inf = load_learner('models/export.pkl')

st.header('MOUNTAIN AI ⛰️')
st.subheader('Classify Mountains from their images!')



class Predict:
    def __init__(self, filename):
        self.learn_inference = load_learner(Path()/filename)
        self.img = self.get_image_from_upload()
        if self.img is not None:
            self.display_output()
            self.get_prediction()

    @staticmethod
    def get_image_from_upload():
        uploaded_file = st.file_uploader(
            "Upload Files", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            return PILImage.create((uploaded_file))
        return None

    def display_output(self):
        st.image(self.img.to_thumb(500, 500), caption='Uploaded Image')

    def get_prediction(self):
        if st.button('Classify'):
            pred, pred_idx, probs = self.learn_inference.predict(self.img)
            st.write(f'**Prediction**: {pred}')
            st.write(f'**Probability**: {probs[pred_idx]*100:.02f}%')
        else:
            st.write(f'Click the button to classify')


if __name__ == '__main__':
    file_name = 'models/export.pkl'
predictor = Predict(file_name)
