import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import sqlite3
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType






			


KEY = 'bc24b9e0e54e4c96b4c59ccc5adfdea3'
ENDPOINT = 'https://itprojectcbt.cognitiveservices.azure.com/'  # Replace with your regional Base URLL

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

group_photo = 'test.jpg'
image = open('G:\\projects\\healthcare\\images\\test.jpg', 'r+b')

# Detect faces
face_ids = []
faces = face_client.face.detect_with_stream(image)
for face in faces:
    face_ids.append(face.face_id)

print(face_ids)
# Identify faces
results = face_client.face.identify(face_ids, 'test2')
print('Identifying faces in {}'.format(os.path.basename(image.name)))
if not results:
    print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
res=0
for person in results:
    print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
    print(person.candidates[0].person_id)
    res=person.candidates[0].person_id



