from __future__ import print_function
from database import FireBase
import csv
import os
import json
import requests
import subprocess
import sys
import pickle
import os.path
import json
import curses
from PIL import Image
from io import BytesIO
import io
import time

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from apiclient.http import MediaFileUpload
from resizeimage import resizeimage
from urllib.request import urlopen
import shutil

from database import FireBase

# wak = ""

def exchange_refresh_token(refresh_token):
    refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + wak
    refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
    refresh_req = requests.post(refresh_url, data=refresh_payload)

    if refresh_req.ok:
        local_id = refresh_req.json()['user_id']
        id_token = refresh_req.json()['id_token']
        return id_token, local_id
    else:
        print(refresh_req.json())
        return False

with open("refresh_token.txt", "r") as f:
    refresh_token = f.read()
idToken, localId = exchange_refresh_token(refresh_token)


def update_db(upc, new_desc, ghost, drive_url):
    #url = ""
    result = json.dumps({
        'desc': new_desc,
        'img': drive_url,
        'ghost': ghost})
        # Change edited by in upc_data
    return (requests.patch(url + 'Upc_data' + '/' + upc + '/' + ".json?auth=" + idToken, data=result))

def drive_connect_service():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'old_credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def post_to_drive(service, description, parent_id, mime_type, filename):
    
    """Insert new file.

    Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
    Returns:
    Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
    'name': description,
    'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]


    file = service.files().create(
        body=body,
        media_body=media_body).execute()

    # Uncomment to print the File ID
    # print 'File ID: %s' % file['id']
    os.remove("temp.jpg")
    return file['id']

def resize_image(url):
    # set to less than 10 kb

    basewidth = 200
    response = requests.get(url, stream=True)
    with open('my_image.png', 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response
    img = Image.open('my_image.png')
    img = img.convert('RGB')
    #response = requests.get(url)
    #img = Image.open(requests.get(url, stream=True).raw)
    #img = Image.open(BytesIO(response.content))
    #img = Image.open(urlopen(url))
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save('temp.jpg')
    return 'temp.jpg'


if __name__ == "__main__":
    service = drive_connect_service()
    parent_id = 'Images'
    mime_type ='image/jpeg'
    while True:
        ghost = bool(input("Ghost"))

        upc = input("Enter the upc :")
        desc = input("Enter the description :")
        
        url = input("Enter the image_url :")

        img_file = resize_image(url)

        url_id = post_to_drive(service, upc, parent_id, mime_type, img_file)

        drive_url = "https://docs.google.com/uc?id=%s" % url_id

        req = update_db(upc, desc, ghost, drive_url)
        print("Uploaded ? = ", req.ok)