import os, sys, re
import string
import pathlib
from pathlib import Path
from fnmatch import fnmatch
import argparse
import subprocess
import urllib.parse
import imdb

user = 'user'
password = 'password'
host = 'host'
port = 'port'

parser = argparse.ArgumentParser(description='Tworzenie listy m3u')
parser.add_argument('katalog', help="Podaj katalog do skanowania")
args = parser.parse_args()
pattern = ["*.mkv", "*.mp4"]

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def get_genre(title):
                try:
                        print(title)
                        ia = imdb.IMDb()
                        movies = ia.search_movie(title)
                        genre = ia.get_movie(movies[0].movieID)
                        wynik=genre['genres'][0]
                except IndexError:
                        wynik="Brak"
                except KeyError:
                        wynik="Brak"
                return wynik

if args.katalog == "/Seriale":

        plikM3u = open("/Seriale.m3u", "w")
        plikM3u.write("#EXTM3U\n")




        for path, subdirs, files in os.walk(args.katalog):
                for name in files:
                        if name.endswith(('.mkv', '.mp4', '.avi')):
                                print(name)
                                pathFile=(path.split(os.path.sep))
                                nazwaSerial=pathFile[3]
                                numerSezon=pathFile[4]
                                plikSerial=name
                                numerOdcinka=re.search('s[0-9]{2}(e[0-9]{2})', name.lower())[1]
                                sciezkaSerial=path+'/'+name
                                urlDoUruchomienia=('http://'+user+':'+password+'@'+host+':'+port+'/Seriale/'+urllib.parse.quote(nazwaSerial)+'/'+numerSezon+'/'+plikSerial)
                                czasTrwaniaPliku=(get_length(sciezkaSerial))
                                wpis=('#EXTINF:'+str(czasTrwaniaPliku).split('.')[0]+' group-title="'+nazwaSerial+'",'+nazwaSerial+" "+numerSezon.upper()+"/"+numerOdcinka.upper()+"\n\t\t"+urlDoUruchomienia+"\n")
                                plikM3u.write(wpis)
                                print(wpis)


elif args.katalog == "/Filmy":

        plikFm3u = open("/Filmy.m3u", "w")
        plikFm3u.write("#EXTM3U\n")

        for path, subdirs, files in os.walk(args.katalog):
                for name in files:
                        if name.endswith(('.mkv', '.mp4')):
                                print(name)
                                pathFile=(path.split(os.path.sep))
                                nazwaFilmu=pathFile[3]
                                plikFilm=name
                                sciezkaFilm=path+'/'+name
                                urlDoUruchomienia=('http://'+user+':'+password+'@'+host+':'+port+'//Filmy/'+urllib.parse.quote(nazwaFilmu)+'/'+plikFilm)
#                               print(get_genre(nazwaFilmu))
                                if not os.path.isfile(path+'/genre'):
                                        plikGenre = open(path+'/genre', "w")
                                        grupaFilmu=get_genre(nazwaFilmu)
                                        plikGenre.write(grupaFilmu)
                                else:
                                        grupaFilmu=Path(path+'/genre').read_text()
                                czasTrwaniaPliku=(get_length(sciezkaFilm))
                                wpis=('#EXTINF:'+str(czasTrwaniaPliku).split('.')[0]+' group-title="'+grupaFilmu.strip()+'",'+nazwaFilmu+"\n\t\t"+urlDoUruchomienia+"\n")
                                plikFm3u.write(wpis)



else:

        print("Blad")
