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
    
    #Get and draw Image Objects
    ImageObjects(result, image_file)
    
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
        
#Get and draw Image Objects
def ImageObjects(result, image_filename):
    if result.objects is not None:
        print("\nObjects in image:")

        # Prepare image for drawing
        image = Image.open(image_filename)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for detected_object in result.objects.list:
            # Print object name
            print(" {} (confidence: {:.2f}%)".format(detected_object.tags[0].name, detected_object.tags[0].confidence * 100))
            
            # Draw object bounding box
            r = detected_object.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(detected_object.tags[0].name,(r.x, r.y), backgroundcolor=color)

        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        # add the name of the original image file
        image_filename = image_filename.split('/')[-1]
        outputfile = 'objects-'+image_filename
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)
    
    
  
if __name__ == "__main__":
    main()