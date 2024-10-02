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
        data = f.read()
    # Instantiate an Azure AI client
    az_client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    
    