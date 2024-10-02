from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests
#Import Azure SDK
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def main():
    # Load the environment variables
    load_dotenv()
    # Get the endpoint and key from the environment variables
    endpoint = os.getenv('ENDPOINT')
    key = os.getenv('KEY')
    
    #get the image file from the command line arguments
    image_file = "images/image1.jpg"
    if len(sys.argv) == 2:
        image_file = sys.argv[1]
    # Reads the specified image file into a byte array.
    with open(image_file, "rb") as f:
        img_data = f.read()
    # Instantiate an Azure AI client
    az_client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    
    # Analyze image
    AnalyzeImage(az_client, img_data, cv_client)

def AnalyzeImage(az_client, img_data, cv_client):
    try:
        # Call the Azure AI to analyze the image with specified visual features
        analysis = az_client.analyze_image(
            img_data, 
            visual_features=[
                VisualFeatures.OBJECTS,
                VisualFeatures.CATEGORIES,
                VisualFeatures.DESCRIPTION,
                VisualFeatures.FACES,
                VisualFeatures.COLOR,
                VisualFeatures.TAGS,
                VisualFeatures.ADULT,
                VisualFeatures.IMAGE_TYPE,
                VisualFeatures.DENSE_CAPTIONS
                ])
        # Display the image and overlay it with the extracted features
        #display_image(img_data, analysis)
    except HttpResponseError as e:
        print('Error code:', e.error.code, 'Message:', e.error.message)
    except Exception as e:
        print(e)
