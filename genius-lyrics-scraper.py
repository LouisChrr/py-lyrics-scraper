import random 
import requests
import sys
from bs4 import BeautifulSoup

#Insensible à la casse et accents | Sensible à l'orthographe
#Liste des artistes ['artiste1', 'artiste2']
ARTISTS = ['Lomepal', 'Roméo Elvis']
    
#Liste des albums ['artiste1 - album1', 'artiste2 - album2]
ALBUMS = ['Orelsan - La fête est finie épilogue']


def prompt():
    print("--- Lyrics Generator -- Genius Lyrics Scraper v1.0 -- by LouisChrr ---")
    print("--- Spelling Sensitive -- Case Insenstive ---")
    print("-------------------------------------------------------------------------------------------")
    artist=input("Précisez l'artiste - laissez vide pour choix par défaut:\n")
    album=""
    song=""
    if(artist!=""):
        album=input("Album ? - laissez vide pour son ou choix parmis les plus populaires:\n")
        if(album==""):
            song=input("Son ? - laissez vide pour choix parmis les plus populaires:\n")
    print("-------------------------------------------------------------------------------------------")
    punch(artist=artist,album=album,song=song)


def format(string):
    return string.strip().replace(" ", "-").replace("'", "").replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a").replace("î", "i")

TRIES = 1

def punch(artist="",album="",song=""):
    
    global TRIES
    global ALBUMS
    global ARTISTS
    baseartist = artist
    basesong = song    
    basealbum = album
    album_format = ""
    forced=False

    if song!="" or album!="":
        if artist!="":
            forced = True
        else:
            sys.exit("Veuillez préciser l'artiste si vous spécifiez un son ou un album. Exiting.")
    elif artist!="":
        forced = True       
    
    #Choix forced ?
    if forced==True:
        
        #Force l'artiste
        if artist!="" and song=="" and album=="":
            print("Artiste: " + artist.capitalize() + ". Récupération d'une chanson permis ses plus populaires..")
            #Scraping des meilleurs son de l'artiste
            page = requests.get('https://genius.com/artists/' + format(artist).capitalize())
            if page.status_code==200:
                print("Artiste " + format(artist).capitalize() + " trouvé!") 
            elif page.status_code==404:
                sys.exit("Artiste '" + artist.capitalize() + "' non trouvé. Veuillez vérifier l'orthographe.\nExiting..")
            else:
                sys.exit("Erreur HTTP: " + str(page.status_code))
                         
            soup = BeautifulSoup(page.content, 'html.parser')
            #Choix du son
            pop_songs = soup.find_all('a', class_='mini_card')
            song = random.choice(pop_songs).get('href')
            
            
        #Force le song
        elif artist!="" and song!="":
            print("Son: " + song.capitalize() + " par " + artist.capitalize() + ". Récupération des paroles..")
            song = 'https://genius.com/' + format(artist).capitalize() + '-' + format(song).lower() + '-lyrics'
            
        #Force l'album
        elif artist!="" and album!="":
            print("Album: " + album.capitalize() + " par " + artist.capitalize() + ". Récupération des paroles d'une chanson de l'album..")
            album_format = format(album).capitalize()
            
            #Scraping des sons de l'album
            page = requests.get('https://genius.com/albums/' + format(artist).capitalize() + '/' + album_format)
            if page.status_code==200:
                print("Album '" + basealbum.capitalize() + "' par '" + baseartist.capitalize() + "' trouvé!") 
            elif page.status_code==404:
                sys.exit("Album '" + basealbum.capitalize() + "' par '" + baseartist.capitalize() + "' non trouvé. Veuillez vérifier l'orthographe.\nExiting..")
            else:
                sys.exit("Erreur HTTP: " + str(page.status_code))
                
            soup = BeautifulSoup(page.content, 'html.parser')

            #Choix du son
            songs = soup.find_all('a', class_='u-display_block')
            song = random.choice(songs).get('href')
            
    #Pas de choix
    else:    
        if '' in ALBUMS or '' in ARTISTS:
            sys.exit("Entrée vide détectée dans une liste par défaut ALBUMS/ARTISTS..\nExiting.")            
        
        print("Sélection aléatoire parmis les artistes et albums de la liste par défaut..")        
        #Artiste ou album ?
        if len(ARTISTS)!=0 and (random.randint(0,1) == 0 or len(ALBUMS)==0):    
            #Choix de l'artiste
            artist = random.choice(ARTISTS).strip()
            print("Artiste: " + artist.capitalize()+"..")
            
            #Scraping des meilleurs son de l'artiste
            page = requests.get('https://genius.com/artists/' + format(artist).capitalize())
            if page.status_code==200:
                print("Artiste '" + artist.capitalize() + "' trouvé!")
                baseartist = artist
            elif page.status_code==404:
                sys.exit("Artiste '" + artist.capitalize() + "' non trouvé. Veuillez vérifier l'orthographe.\nExiting..")
            else:
                sys.exit("Erreur HTTP: " + str(page.status_code))
                
            soup = BeautifulSoup(page.content, 'html.parser')
            #Choix du son
            pop_songs = soup.find_all('a', class_='mini_card')
            song = random.choice(pop_songs).get('href')
        
        elif len(ALBUMS) != 0:
            #Choix de l'album
            album = random.choice(ALBUMS)
            artist = album[0:album.find("-")-1].strip().capitalize()
            print("Artiste: " + artist)
            album = album[album.find("-")+2:].strip().capitalize()
            print("Album: " + album)
            album_format = format(album).capitalize()

            #Scraping des sons de l'album
            page = requests.get('https://genius.com/albums/' + format(artist).capitalize() + '/' + album_format)
            if page.status_code==200:
                print("Album '" + album.capitalize() + "' par '" + artist.capitalize() + "' trouvé!")
                baseartist = artist
                basealbum = album
            elif page.status_code==404:
                sys.exit("Album '" + album.capitalize() + "' par '" + artist.capitalize() + "' non trouvé. Veuillez vérifier l'orthographe.\nExiting..")
            else:
                sys.exit("Erreur HTTP: " + str(page.status_code))
            
            soup = BeautifulSoup(page.content, 'html.parser')

            #Choix du son
            songs = soup.find_all('a', class_='u-display_block')
            song = random.choice(songs).get('href')
            
        else:
            sys.exit("Veuillez ajouter un artiste/album à la liste par défaut OU préciser un choix.\nExiting...")

    #Scraping du son
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.40 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language' : "en;q=0.8", 'Accept': '*/*', 'Connection': 'keep-alive'}
    song_page = requests.get(song)
    
    tmpsong=""
    if basesong!="":
        tmpsong=basesong.capitalize()
    else: #Si sous forme URL
        tmpsong=song.lower()
        if tmpsong.find('https')!=-1:
            tmpsong=tmpsong[tmpsong.find(format(baseartist.lower()))+len(baseartist)+1:tmpsong.find('lyrics')-1].capitalize().replace("-"," ")
    
    if song_page.status_code==200:
        print("Son '" + tmpsong + "' par '" + baseartist.capitalize() + "' trouvé! -- URL: " + song)            
        basesong = tmpsong
    elif song_page.status_code==404:
        sys.exit("Son '" + tmpsong + "' par '" + baseartist.capitalize() + "' non trouvé. Veuillez vérifier l'orthographe.\nExiting..")
    else:
        sys.exit("Erreur HTTP: " + str(page.status_code))
    
    song_soup = BeautifulSoup(song_page.content, 'html.parser')


    #Scraping des lyrics
    lyrics = ""

    [h.extract() for h in song_soup('script')]
    for lyric in song_soup.find_all(class_='Lyrics__Container-sc-1ynbvzw-2 jgQsqn'):
        lyrics += lyric.get_text(separator="\n")

    if len(lyrics) < 4:
        TRIES += 1
        if TRIES < 11:
            print("/!\ Scraping détecté /!\ Retrying.. try number #" + str(TRIES) + " (10 max)\n-------------------------------------------------------------------------------------------")            
            sys.exit(punch(artist=baseartist,song=basesong,album=basealbum))
        else:
            sys.exit("Too many tries. Wait a bit then retry!\n")
    #Scraping du titre, vide si null
    title=""
    title=song_soup.find('title').get_text()
    if title.count("–") > 0:
        tmp=title.find("–")
        title=title[tmp+2:]
        tmp=title.find(" Lyrics")
        title=title[:tmp]    

    
    
    #Remove des [Intro], [Refrain], etc..
    ite = 0
    while(lyrics.count("[") > 0 and lyrics.count("]") > 0 and ite < 15):
        ite += 1
        #tmp = lyrics.find("[")
        #tmp2 = lyrics.find("]")
        #print("found at " + str(tmp) + " - " + str(tmp2))
        lyrics = lyrics[:lyrics.find("[")] + lyrics[lyrics.find("]")+1:]

    content = lyrics.splitlines()

    #Scraping de 4<X<8 lignes aléatoire
    lines = random.randint(4,8)

    if len(lyrics) > 2:
        if title!="":
            if album!="":
                print("Artiste: " + artist.capitalize() + " | Album: " + album.capitalize() + " | Titre: " + title.capitalize() + " ---- " + str(lines) + " lignes de paroles recupérées avec succès!")
            else:
                print("Artiste: " + artist.capitalize() + " | Titre: " + title.capitalize() + ": Paroles recupérées avec succès!")
        print("-------------------------------------------------------------------------------------------")
        if len(content) < lines:
            lines = len(content)
            start = 0
        else:
            start = random.randint(0,len(content)-lines)
            
        tts_content = ""        
        it=1
        for el in range(lines):
            if start<len(content) and (content[start]!="" and content[start]!=" "):
                tts_content+=content[start]
            elif start<len(content):
                start+=1
                tts_content+=content[start]
            if start+1<len(content) and (content[start+1].startswith(",") or content[start+1].startswith("(") or content[start+1].startswith("?") or content[start+1].startswith(")") or content[start+1].startswith(";") or content[start].endswith(",")):
                start+=1
                tts_content+=content[start]
            elif it<lines:
                tts_content+=", "
            elif it>=lines:
                tts_content+="."
            start+=1
            it+=1
            
        
        if len(title) > 2:
                msg = "Comme dirait " + str(artist.capitalize()) + " dans " + str(title.capitalize()) + ": " + str(tts_content)
        else:
                msg = "Comme dirait " + str(artist.capitalize()) + ": " + str(tts_content)
        # -------- RESULT --------
        print(msg)
    else:
        sys.exit("Erreur - réessayez.")
        
prompt()
