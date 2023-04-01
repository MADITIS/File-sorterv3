import re
import list_files
import info

FIRST_REGEX = "(.*?)[. ]\(?([(0-9]{4})\)?[. ]([\w]*?)[. ](.*?)-?[A-Za-z]*?"
SECOND_REGEX = "(.*?) \(([0-9]{4})\) ([A-Z]*?) ?\([0-9p]{4,5}(.*?)(x265)? ([0-9a-z]{4})(.*?)\)"
THIRD_REGEX = "(.*?)[. ]\(?([(0-9]{4})\)?(.*?)([\w-]*?)[. ](.*?)-?[A-Za-z]*?"
patterns = [FIRST_REGEX,SECOND_REGEX,THIRD_REGEX]

movie_info = info.GetInfo()
file_obj = list_files.Files()
DESTINATION_FOLDER = file_obj.DESTINATION_FOLDER
SOURCE_FOLDER = file_obj.SOURCE_FOLDER
all_files = file_obj.get_folders(SOURCE_FOLDER)
print(all_files)


def create_parent(parent_folder_meta_data,folder_meta_data):
    parent_id = file_obj.create_folder(parent_folder_meta_data)
    folder_meta_data["parents"] = [parent_id]
    return file_obj.create_folder(folder_meta_data)


for file in all_files:
    original_name = file["name"]
    if "\u200b" in original_name:
        original_name = original_name.replace("\u200b","")
    previous_parent = file["parent"][0]
    file_id = file["id"]
    # web_link = file["webContentLink"]
    # print(original_name)
    for pattern in patterns:
        matched_name = re.match(pattern, original_name)
        if matched_name != None:
            break

    if matched_name != None:
        #get the movie folder name  
        
        # print(movie_info.inter_info(matched_name))
        folder_name = movie_info.inter_info(matched_name)
        if folder_name != None and "S0" not in folder_name:
            # print(folder_name)
            first_letter = folder_name[0]
            if "REPACK" in folder_name:
                f = folder_name.replace("REPACK","")
                folder_name = " ".join(f.split())

            if first_letter.islower():
                folder_name = folder_name.title()
                first_letter = folder_name[0]

            elif first_letter.isdigit():
                parent_movie_folder = 'Cinema • # • Part'
            elif first_letter =="[":
                continue
            else:
                parent_movie_folder =  f'Cinema • {first_letter} • Part'
            mimetype = "application/vnd.google-apps.folder"
            # print(parent_movie_folder) 
            parent_folder = file_obj.check_folder_exist(parent_movie_folder,mimetype,DESTINATION_FOLDER)

            parent_folder_meta_data = {
            "name" : parent_movie_folder,
            "mimeType" : 'application/vnd.google-apps.folder',
            "parents" : [DESTINATION_FOLDER]
            }        

            folder_meta_data = {
            "name" : folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            "parents"  :""

                }

            if parent_folder == []:
                file_obj.move_file(previous_parent,create_parent(parent_folder_meta_data,folder_meta_data),file_id,folder_name)

            else:
                def main():  
                    count = 0
                    for i in parent_folder:
                        count += 1
                        if parent_movie_folder in i.values():
                            new_parent_top = i["id"]
                            movie_folder_check = file_obj.check_folder_exist(folder_name,mimetype,new_parent_top)
                            if movie_folder_check == []:
                                folder_meta_data["parents"] = [new_parent_top]
                                movie_folder_id = file_obj.create_folder(folder_meta_data)
                                file_obj.move_file(previous_parent,movie_folder_id,file_id,folder_name)
                                return

                            else: 
                                count2 = 0
                                for j in movie_folder_check:
                                    count2 += 1
                                    if folder_name in j.values():  
                                        new_parent = j["id"]
                                        new_minetype = "video/x-matroska"
                                        existing_movie_id = file_obj.check_folder_exist(original_name,new_minetype,new_parent)
                                        if existing_movie_id != []:
                                            count3 = 0
                                            for k in existing_movie_id:
                                                count3 += 1
                                                if original_name not in k.values():
                                                    file_obj.move_file(previous_parent,new_parent,file_id,folder_name)
                                                    return

                                                elif count3 < len(existing_movie_id):
                                                    continue    
                                                else:
                                                    file_obj.update(file_id)
                                                    print("duplicate deleted")
                                                    return

                                        else:     
                                            file_obj.move_file(previous_parent,new_parent,file_id,folder_name)
                                            return            
                                    elif count2 < len(movie_folder_check):
                                        continue
                                    else:
                                        folder_meta_data["parents"] = [new_parent_top]
                                        movie_folder_id = file_obj.create_folder(folder_meta_data)
                                        file_obj.move_file(previous_parent,movie_folder_id,file_id,folder_name)                                        
                                        return                
                                        
                            # else create the folder
                        elif count < len(parent_folder):
                            continue
                        else:  
                            file_obj.move_file(previous_parent,create_parent(parent_folder_meta_data,folder_meta_data),file_id,folder_name)
                            return
                main()
