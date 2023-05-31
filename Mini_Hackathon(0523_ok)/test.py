# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 20:28:50 2023

@author: Leo
"""

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = "b9e345f19fc64b31a67332059b32ce56"
endpoint = "https://test202304240802.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''
'''
Tag an Image - local
This example returns a tag (key word) for each thing in the image.
'''
print("===== Tag an image - local =====")
# Call API with local image
local_image_path = "https://i.imgur.com/63oXVUb.jpeg"
with open(local_image_path, "rb") as image_stream:
    tags_result_local = computervision_client.tag_image_in_stream(image_stream)

# Print results with confidence score
print("Tags in the local image: ")
if len(tags_result_local.tags) == 0:
    print("No tags detected.")
else:
    for tag in tags_result_local.tags:
        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
print()
'''
END - Tag an Image - local
'''
print("End of Computer Vision quickstart.")
"""



subscription_key = "b9e345f19fc64b31a67332059b32ce56"
endpoint = "https://test202304240802.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


'''
Quickstart variables
These variables are shared by several examples
'''
# Images used for the examples: Describe an image, Categorize an image, Tag an image, 
# Detect faces, Detect adult or racy content, Detect the color scheme, 
# Detect domain-specific content, Detect image types, Detect objects
images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
remote_image_url = "https://image-cdn-flare.qdm.cloud/q6d7d47a2f64f1/image/cache/data/126863009_5288902777790350_5675222426795306123_o_1-max-w-1024.jpg"
'''
END - Quickstart variables
'''


'''
Tag an Image - remote
This example returns a tag (key word) for each thing in the image.
'''
print("===== Tag an image - remote =====")
# Call API with remote image
tags_result_remote = computervision_client.tag_image(remote_image_url )

detect_list = ['bread','dessert']
# Print results with confidence score
print("Tags in the remote image: ")

for tag in tags_result_remote.tags:
    for i in range(0,2):
        if('{}'.format(tag.name) == detect_list[i]):
            print('yes')
        #print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
print()
'''
END - Tag an Image - remote
'''
print("End of Computer Vision quickstart.")