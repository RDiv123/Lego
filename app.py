import streamlit as st
import json
import requests
import base64
from PIL import Image
import io


#these are main classes your image is trained on
#you can define the classes in alphabectical order
PREDICTED_LABELS = ["Starwars", "Marvel","Jurassic world","Harry potter"]


def get_prediction(image_data):
  #replace your image classification ai service URL
  url = 'https://askai.aiclub.world/0dab0b7f-86dc-45dd-8d06-6696b57802b9'
  r = requests.post(url, data=image_data)
  response = r.json()['predicted_label']
  score = r.json()['score']
  #print("Predicted_label: {} and confidence_score: {}".format(response,score))
  return response, score
  
def set_background_color(color):
    hex_code = '#%02x%02x%02x' % color
    page_bg_img = '''
    <style>
    body {
    background-color: %s;
    }
    </style>
    ''' % hex_code
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the background color
set_background_color((173, 216, 230))  # Light blue background color



#creating the web app

#setting up the title
st.title("Legofigurine Image Classifier")#change according to your project
st.image("https://www.vecteezy.com/vector-art/226355-two-plastic-toy-men-standing-side-by-side",caption="Legos")
#setting up the subheader
st.subheader("File Uploader")#change according to your project


#file uploader
image = st.file_uploader(label="Upload an image",accept_multiple_files=False, help="Upload an image to classify them")
if image:
    #converting the image to bytes
    img = Image.open(image)
    buf = io.BytesIO()
    img.save(buf,format = 'JPEG')
    byte_im = buf.getvalue()

    #converting bytes to b64encoding
    payload = base64.b64encode(byte_im)

    #file details
    file_details = {
      "file name": image.name,
      "file type": image.type,
      "file size": image.size
    }

    #write file details
    st.write(file_details)

    #setting up the image
    st.image(img)

    #predictions
    response, scores = get_prediction(payload)

    #if you are using the model deployment in navigator
    #you need to define the labels
    response_label = PREDICTED_LABELS[response]

    col1, col2 = st.columns(2)
    with col1:
      st.metric("Prediction Label",response_label)
    with col2:
      st.metric("Confidence Score", max(scores))



