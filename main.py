
from flask import Flask, render_template, request, flash, redirect, get_flashed_messages
import urllib.request

from yt_dlp import YoutubeDL

# import os

import datetime as datetime

import shutil

app = Flask(__name__)


### esto es para el Flask, sin esto genera error
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'





def check_response(URL):
    try:
        response = urllib.request.urlopen(URL)

        if len(response.read()) > 0:
            # print(f"La URL {URL} tiene contenido")
            return True
    except:
        return False
 

def download_file(URL):

    ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # 'format': 'mp4/bestvideo/best',
    # 'format': 'mp3/bestaudio/best',
    # 'format': "mp4/bestaudio"

    'noplaylist': 'no',
    # 'download_archive': '/Users/rodrigogalvis/Documents/Python/Bootcamp/Day95_My_API_SERVICE/downloads'
    # 'download_archive': '',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # print("ANtes del ejecutar el info")
            # print(ydl['paths'])
            # print(ydl.format_sort())
            info = ydl.extract_info(URL, download=True)

            # error_code = ydl.download(URL)
        

      
        
        
        # print()
        # print("Despues de ejecutar el info")
        # print(info)
        # print("ERROR ", error_code)
        return "Suceed", info
    except Exception as e:
        # print("Exception  psitn ", e)
        return str(e), "Info Null"

    return "Failed"


@app.route("/download")
def download():
    global info_return

    name = info_return['title'] + " [" + info_return['id'] + '].m4a'

      #### move the file to static

    shutil.copy(name, "./static/")

    print(name)

    return render_template("download.html", info_return=info_return, name= name)






@app.route("/", methods=['GET', 'POST'])
def home():
    global info_return

    if request.method == 'POST':
        
        # print(request.form.get('url_link'))
        URL = request.form.get('url_link')

        #### verificar si la URL ingresada tiene respuesta en servidor
        if not check_response(URL):
            # print("La URL TIENE CONTENIDO")
            flash("URL Not valid")
            return redirect(request.url)

        download_file_return, info_return = download_file(URL)

        if download_file_return == "Suceed":
            current_time = datetime.datetime.now()

            print(info_return['title'])
            print(info_return['id'])
            return redirect ("download")
        else:

            flash(download_file_return)
            print(" mi prienttt ",download_file_return)
            return redirect(request.url)
    





    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)







