import json
import info
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import random

# with open("Projects\\Movie-Sorter v2\\config.json") as config:
#         file = json.load(config)
# DESTINATION_FOLDER = file[0]["Destination_folder"]
# SOURCE_FOLDER = file[0]["Source_Folder"]
# TEAM_DRIVE_ID = file[0]["Team_drive"]
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = f"{random.randint(0,2)}.json"

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials= credentials)

class Files:
    with open("config.json") as config:
        file = json.load(config)
        DESTINATION_FOLDER = file[0]["Destination_folder"]
        SOURCE_FOLDER = file[0]["Source_Folder"]
        TEAM_DRIVE_ID = file[0]["Team_drive"]

    def __init__(self):
        self.files = 0
        self.all_files = []

    @staticmethod
    def update(parent_id):
        body = {'trashed': True}
        updated_file = service.files().update(
                        fileId = parent_id,
                        body = body,
                        supportsAllDrives = True

                        ).execute()

        print("file deleted")                

    def get_folders(self,folder_id):
        token = ""
        while token is not None:
            file = service.files().list(
                                    driveId = Files.TEAM_DRIVE_ID,
                                    q = "parents in '"+folder_id+"' and trashed = false",
                                    supportsAllDrives = True,
                                    pageSize = 500,
                                    pageToken = token,
                                    includeItemsFromAllDrives = True,	
                                    corpora = 'teamDrive',
                                    fields='nextPageToken, files(id,name,mimeType,parents)',
                                    ).execute()
            files = file.get("files", [])
            print(files)
            if files == [] and folder_id != Files.SOURCE_FOLDER:
                Files.update(folder_id)
            
            else:
                for i in files:
                    mimetype = i['mimeType']
                    file_id = i["id"]
                    file_name = i["name"]
                    parnet_id = i["parents"]
                    if mimetype == 'video/x-matroska' or mimetype == "video/mp4":
                        new = {"id": file_id , "name" : file_name,"parent":parnet_id}
                        self.all_files.append(new)
                        
                    elif mimetype == 'application/vnd.google-apps.folder' and file_name == "Featurettes":
                        print("deletes",file_name)
                        Files.update(file_id)

                    elif mimetype == 'application/vnd.google-apps.folder':
                        self.get_folders(file_id)
                    else:
                        if file_id != Files.SOURCE_FOLDER: 
                            Files.update(file_id)

            token = file.get("nextPageToken") 
        return self.all_files


    def check_folder_exist(self,folder,mimetype,alphabet_folder):
        if "'" in folder:
            s = folder.split("'")
            folder = s[0] +"\\'"+s[-1]    
        token = ""
        while token is not None:
            checking_parent_folder = service.files().list(
                                    driveId = Files.TEAM_DRIVE_ID,
                                    q=f"fullText contains '{folder}' and mimeType='{mimetype}' and '{alphabet_folder}' in parents and trashed=false",
                                    corpora = 'teamDrive',
                                    supportsAllDrives = True,
                                    pageSize =100,
                                    includeItemsFromAllDrives  = True,	
                                    fields='nextPageToken, files(id,name,mimeType)').execute()
            token = checking_parent_folder.get("nextPageToken")
        return checking_parent_folder.get("files",[])


    @staticmethod
    def create_folder(metadata):
        create = service.files().create(
            supportsAllDrives = True,
            body = metadata,
            fields = "id",
        ).execute()

        return create.get("id")    

    @staticmethod    
    def move_file(previous_parent,new_parent,file_id,folder_name):
        try:
            move = service.files().update(
                supportsAllDrives = True,
                fileId = file_id,
                addParents= new_parent,
                removeParents = previous_parent,
                fields='id, parents, name, size',
                        ).execute() 

            moved_folder_id = move.get("parents")[0]
            name = move.get("name")
            size = int(move.get("size"))
            fileid = move.get("id")
            info_side = info.GetInfo()
            move_size = info_side.get_size(size)
            info_side.sendinfo(folder_name,name,moved_folder_id,move_size)

        except HttpError as err:
            pass                


        
 
