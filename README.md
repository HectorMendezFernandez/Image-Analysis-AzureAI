# Object-detection-AzureAI
 Project that will use the AZURE AI service to detect objects in an image

 This Python script leverages Azure Computer Vision to analyze images and detect objects within them.

Prerequisites:

Azure Account: You'll need an active Azure account.
Azure Computer Vision Subscription: Create an Azure Computer Vision resource in the Azure portal.
Python: Ensure Python is installed on your system.
Packages: Install the required dependencies using pip install -r requirements.txt.
Setup:

Create an Azure Computer Vision resource:

Log in to the Azure portal.
Create a new resource and search for "Computer Vision".
Follow the instructions to create the resource and obtain the access keys.
Create a .env file:

Create a file named .env in the same directory as the script.
Add the following lines, replacing your_endpoint and your_key with the values obtained from your Azure Computer Vision resource:
ENDPOINT=your_endpoint
KEY=your_key
Example:

ENDPOINT=https://your-resource.cognitiveservices.azure.com/
KEY=your_access_key
Run the script:

Open a terminal and navigate to the directory containing the script.
Execute the script: python object-detector.py
Additional options:

Specify an image: Provide a path to an image as an argument when running the script: python object-detector.py images/my_image.jpg
Customize detection: Modify the visual_features list in the AnalyzeImage function to tailor the detection to your specific needs.
Code explanation:

load_dotenv(): Loads environment variables from the .env file.
ImageAnalysisClient: Creates a client to interact with the Azure Computer Vision service.
analyze_image_in_stream: Sends the image to the service for analysis.
ImageCaptions, ImageTags, ImageObjects: Functions to process the analysis results and display captions, tags, and detected objects.


![image](https://github.com/user-attachments/assets/0848ffe5-c005-482d-b51b-1b5bd7b18ce2)
