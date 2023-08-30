from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class MyDrive():

    def __init__(self, api_name, api_version, scopes):

        API_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scopes]

        """Shows basic usage of the Drive v3 API.
            Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # create drive api client
        self.service = build(API_NAME, API_VERSION, credentials=creds)

    def list_files(self, page_size=10):
        try:
            # Call the Drive v3 API
            results = self.service.files().list(
                pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def upload_basic(self, folder_id, path):
        """Insert new file.
        Returns : Id's of the file uploaded

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        FOLDER_ID = folder_id
        PATH = path

        try:
            files = os.listdir(PATH)
            for file in files:
                media = MediaFileUpload(f'{PATH}\{file}')
                # consultar si el archivo ya existe dentro de una directorio
                response = self.service.files().list(
                    q=f"name='{file}' and parents='{FOLDER_ID}'",  # query
                    spaces="drive",  # indicamos que buscamos en googedrive
                    fields="nextPageToken, files(id, name)",
                    pageToken=None
                ).execute()
        
                # obtenemos el array de el o los archivos con mismo nombre y formato y lo almacenamos en la variable items sino le aasignamos una array vacio
                items = response.get('files', [])

                # si existe actualizamos el o los archivos sino creamos una nuevo
                if not items:
                    file_metadata = {
                        "name": file,  # nombre archivo
                        "parents": [FOLDER_ID]  # carpeta donde se guardara archivo
                    }
                
                    upload_file = self.service.files().create(
                        body=file_metadata,  # asignamos la metada(nombre, carpeta)
                        media_body=media,  # archivo que se guardara
                        fields='id'
                    ).execute()

                    print(F'File ID: {upload_file.get("id")}')
                else:
                    for file in items:
                        update_file = self.service.files().update(
                            fileId=file.get('id'),  # seleccionamos el archivo existente por su id
                            media_body=media,
                        ).execute()
                        print(F'File ID: {update_file.get("id")}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None


def main():

    my_drive = MyDrive('drive', 'v3', 'https://www.googleapis.com/auth/drive')

    path = r"C:\Users\NieLi26\Downloads\Code\Projects\personal-inmobiliario\backup"
    folder_id = '1HoY4yaV5RVGyrRqJka9HQAibcrRDiMVn'
    my_drive.upload_basic(folder_id, path)


if __name__ == '__main__':
    main()

