import os.path
import random
from PIL import Image
import io
import mimetypes

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

# This class requires authentication! 
# The config must point to a file containing a json blob of drive credentials downloaded from google's cert manager
TokenFileName = 'DriveTokenAutogenerated.txt'

class DriveImageManager:
    def __init__(self, config, alertService=None):
        self.config = config
        self.alertService = alertService

        try:
            # Do Authorization 
            Scopes = self.config["DriveScopes"]
            creds = None

            if os.path.exists(TokenFileName):
                creds = Credentials.from_authorized_user_file(TokenFileName, Scopes)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.config["DriveSecretsFilePath"], Scopes)
                    creds = flow.run_local_server(port=0)
                with open(TokenFileName, 'w') as token:
                    token.write(creds.to_json())

            self.service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            if alertService:
                alertService.SendMessage(f"Fatal Error Authenticating Google Drive with Excpetion: {e}")
            raise Exception(e) 

    def GetListOfAllImageInfo(self):
        resource = self.service.files()
        pageToken = None
        result = []
        while True:
            response = resource.list(q=f"'{self.config['SourceDriveFolder']}' in parents", pageSize=100, fields="nextPageToken, files(id, name)", pageToken=pageToken).execute()
            result += response.get('files', [])
            pageToken = response.get('nextPageToken', None)
            if pageToken is None:
                break
        
        # filter to only supported file types
        result = [img for img in result if any(fileType in img['name'] for fileType in self.config["SupportedFileTypes"])]

        return result

    # Downloads a random image from drive and saves it in the local cache
    # returns a path to the downloaded image and the drive image info
    def DownloadRandomImage(self):
        imageInfo = self.GetListOfAllImageInfo()
        r = random.randrange(0, len(imageInfo))

        request = self.service.files().get_media(fileId=imageInfo[r]['id'])
        fileHandler = io.BytesIO()
        downloader = MediaIoBaseDownload(fileHandler, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        img = Image.open(fileHandler)
        path = f"{self.config['DriveImageCachePath']}\\{imageInfo[r]['name']}"
        img.save(path)
        return path, imageInfo[r]

    # This function uses the above function to download an image 
    # it then remove that image from the source drive folder and puts it into the sink
    # returns the local filepath to the image
    def DownloadAndMoveRandomImage(self):
        localPath, driveImgInfo = self.DownloadRandomImage()
        
        self.service.files().delete(fileId=driveImgInfo['id']).execute()

        fileMetadata = {
            'name' : driveImgInfo['name'],
            'parents' : [self.config["SinkDriveFolder"]]
        }

        media = MediaFileUpload(localPath, mimetype=mimetypes.guess_type(localPath)[0], resumable=True)
        newImgId = self.service.files().create(body=fileMetadata, media_body=media, fields='id').execute()
        return localPath

    # gets the name of the file
    def GetFileNameFromPath(self, path):
        filename = os.path.basename(path)

        # strip file extention
        for x in self.config["SupportedFileTypes"]: 
            filename = filename.replace(x, "")

        return filename