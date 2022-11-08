import telepot
import random
import omdb

OMDB_API_END_POINT = "http://www.omdbapi.com"
OMDB_API = ["53aaf0b3", "14f9ea72"]
omdb.set_default('apikey', random.choice(OMDB_API))
user_id = -1001652348587
telegram_token = "1724110863:AAFyJr9ztRytYliLrNaEDrg5fzYSF3tu-iY" 
bot = telepot.Bot(telegram_token)


class GetInfo:
    infos = []

    def __init__(self):
       pass
    
    @staticmethod
    def inter_info(matched_name):
        year = ""
        tomato = "N/A"
        name = matched_name.group(1)
        year = matched_name.group(2) 
        movie_name = name.replace(".", " ").rstrip() 
        if "veto" in movie_name:
            movie_name = movie_name.replace("veto-","").rstrip()
        elif "freeman" in movie_name:
            movie_name = movie_name.replace("freeman-","").rstrip()
        elif "getit" in movie_name:
            movie_name = movie_name.replace("getit-","").rstrip()
        elif "gua" in movie_name:
            movie_name = movie_name.replace("gua-","").rstrip()
        elif "Gua" in movie_name:
            movie_name = movie_name.replace("Gua-","").rstrip() 
        elif "fm" in movie_name:
            movie_name = movie_name.replace("fm-","").rstrip()            
        search = omdb.request(t = movie_name, y = year)
        result = search.json()
        if search.status_code == 200 and result["Response"] != "False":
            title = result["Title"]
            movie_year = result["Year"]
            genre = result["Genre"]
            director = result["Director"]
            plot = result["Plot"]
            poster = result["Poster"]
            try:
                for i in result["Ratings"]:
                    if i["Source"] == "Rotten Tomatoes":
                        tomato = i["Value"]
                        break

            except:
                tomato = "N/A"
                print("RT does not exist")   

            meta = result["Metascore"] 
            imdb = result["imdbRating"]  
            imdb_votes =  result["imdbVotes"]
            imdb_id = result["imdbID"] 
            category = result["Type"] 
            GetInfo.infos = [genre,director,plot,poster,tomato,meta,imdb,imdb_votes,imdb_id,category]

            movie_folder_name = f"{title} ({movie_year})"
  
        else:
            if year == "1080":
                year = ""
                movie_folder_name = f"{movie_name}"  

            else:
                movie_folder_name = f"{movie_name} ({year})"                        
        return movie_folder_name
        
    @staticmethod
    def get_size(size):
        if size > 0:
            if size > 1073710000:
            
                file_size = f"{round(size / (1024**3), 2)}GB"   # size In GB   

            else:
                file_size =  f"{round(size / (1024**2), 2)}MB"  #size in MB         

        return file_size


    def sendinfo(self,folder_name_movie, file_name, folder_id,size):
        # bot = telepot.Bot(telegram_token)
        location_link = f"https://drive.google.com/folderview?id={folder_id}"
        # web_link = f"{GOOGLE}{fileid}?key={KEY}&alt=media"
        poster = ""
        if GetInfo.infos != [] :   
         # infos = [genre,director,plot,poster,tomato,meta,imdb,imdb_votes,imdb_id,category] 
            genre = self.infos[0]
            director = self.infos[1]
            plot = self.infos[2]
            poster = self.infos[3]
            tomato = self.infos[4]
            meta = self.infos[5]
            imdb = self.infos[6]
            imdb_votes = self.infos[7]
            imdb_id = self.infos[8]
            category = self.infos[9]     
            imdb_link = "https://www.imdb.com/title/" + imdb_id     
            msg_object ="<strong>"+folder_name_movie+"</strong>\n\n<b>Director: "+"</b>"+"<i>"+director+"</i>\n\n--------------------------------------------------"\
            +"<u><strong>" + "\nPlot:" "</strong></u>" + "<em>"+"  "+plot+"</em>   \n\n✪ "+imdb+"       📊"+imdb_votes+"      🍅"+tomato+"      📈"+meta+"\n\n<strong>Genre: </strong><i>"+genre+"</i>\n\n"+imdb_link+\
            "\n\n--------------------------------------------------" \
            "<b>"+ "\n\n📁Filename: " +   "</b> <code>" + file_name + "</code> <b>\n\nSize: </b><i>" + \
                        size + "</i><b>\n\n🗂️Location:  </b><i>" \
                        + location_link+ "</i><b>" + "\n\n📄Category: " + "</b>" + "<i>"+category+"</i>"        
        else:
            msg_object ="<strong>"+file_name+"</strong>" \
            +"<b>"+ "\n\n📁Filename: " +   "</b> <code>" + file_name + "</code> <b>\n\nSize: </b><i>" + \
                        size + "</i><b>\n\n🗂️Location:  </b><i>" \
                        + location_link+ "</i>" + "<b>" + "\n\n📄Category: " + "</b>" + "<i>"+"Movie"+"</i>"

        GetInfo.infos = []
        print(GetInfo.infos)
        try:
            bot.sendPhoto(chat_id = user_id, photo = poster,caption = msg_object, parse_mode = 'HTML')
        except:
            bot.sendMessage(chat_id = user_id, text = msg_object, parse_mode ="HTML") 



         
                     



