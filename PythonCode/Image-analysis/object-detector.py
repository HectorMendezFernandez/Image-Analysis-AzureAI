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
    #Load the environment variables
    load_dotenv()
    #Get the endpoint and key from the environment variables
    endpoint = os.getenv('ENDPOINT')
    key = os.getenv('KEY')
    
    #get the image file from the command line arguments
    image_file = "images/image-1.jpg"
    if len(sys.argv) == 2:
        image_file = sys.argv[1]
    # Reads the specified image file into a byte array.
    with open(image_file, "rb") as f:
        img_data = f.read()
    # Instantiate an Azure AI client
    az_client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    
    # Analyze image
    AnalyzeImage(image_file, img_data, az_client)

# Display the image and overlay it with the extracted features
def AnalyzeImage(image_file, img_data, az_client):
    try:
        # Call the Azure AI to analyze the image with specified visual features
        result = az_client.analyze(
            image_data = img_data, 
            visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE],
        )
        # Display the image and overlay it with the extracted features
        #display_image(img_data, result)
    except HttpResponseError as e:
        print(f"Status code: {e.status_code}")
        print(f"Reason: {e.reason}")
        print(f"Message: {e.error.message}")
    
    #Get Image Captions
    ImageCaptions(result)
    
    #Get Image Tags
    ImageTags(result)
    
#Get Image Captions
def ImageCaptions(result):
    if(result.caption):
        print('=================================CAPTIONS==================================')
        print('Description:', result.caption.text, 'Confidence:', result.caption.confidence)
        print('============================================================================\n')
        
#Get Image Tags
def ImageTags(result):
    if(result.tags):
        print('=================================TAGS==================================')
        for tag in result.tags.list:
            print('Tag:', tag.name, 'Confidence:', tag.confidence)
        print('============================================================================\n')
    
    
  
if __name__ == "__main__":
    main()

# def display_image(img_data, result):
#     # Open the image file
#     image = Image.open(io.BytesIO(img_data))
#     plt.figure(figsize=(10, 10))
#     # Display the image
#     plt.imshow(image)
#     ax = plt.gca()
#     # Display the image and overlay it with the extracted features
#     for obj in analysis.objects:
#         # Draw a rectangle around the object
#         ax.add_patch(plt.Rectangle((obj.rectangle.x, obj.rectangle.y),
#                                    obj.rectangle.w, obj.rectangle.h,
#                                    fill=False, edgecolor='red', lw=3))
#         # Display the object's name and confidence
#         ax.text(obj.rectangle.x, obj.rectangle.y, f'{obj.object_property} {obj.confidence*100:.2f}%', 
#                 fontsize=12, bbox=dict(facecolor='red', alpha=0.5))
#     plt.axis('off')
#     plt.show()