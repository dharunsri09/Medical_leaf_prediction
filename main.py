import streamlit as st
import numpy as np
from PIL import Image
import base64
import requests
import random

API_URL = "https://api-inference.huggingface.co/models/NonoBru/leaf-classifier"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open("D:/kongu/Downloads/"+filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def generate_herbal_leaf_details():
    herbal_leaves = [
        {"benefits": "Antibacterial, antifungal, antiviral"},
        {"benefits": "Antioxidant, adaptogenic, immune boosting"},
        {"benefits": "Wound healing, anti-inflammatory, moisturizing"},
        # Add more herbal leaves as needed
    ]
    return random.choice(herbal_leaves)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

contnt = "<p>Herbal medicines are preferred in both developing and developed countries as an alternative to " \
         "synthetic drugs mainly because of no side effects. Recognition of these plants by human sight will be " \
         "tedious, time-consuming, and inaccurate.</p> " \
         "<p>Applications of image processing and computer vision " \
         "techniques for the identification of the medicinal plants are very crucial as many of them are under " \
         "extinction as per the IUCN records. Hence, the digitization of useful medicinal plants is crucial " \
         "for the conservation of biodiversity.</p>"

if __name__ == '__main__':
    add_bg_from_local("artifacts/Background.jpg")
    new_title = '<p style="font-family:sans-serif; color:White; font-size: 42px;">Medicinal Leaf Classification</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.markdown(contnt, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img = img.resize((300, 300))
        st.image(img)
        if st.button("Predict"):
            output = query(uploaded_file.name)
            selected_leaf = generate_herbal_leaf_details()
            result = '<p style="font-family:sans-serif; color:White; font-size: 16px;">Model prediction ' \
                        'is '+str(output)+'<br><br>' \
                        'Selected Herbal Leaf:<br>' \
                        f'Name: {output[0]["label"]}<br>' \
                        f'Benefits: {selected_leaf["benefits"]}</p>'
            st.markdown(result, unsafe_allow_html=True)
