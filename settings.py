import os,platform

upload_path = os.path.join(os.path.dirname(__file__), "img")
static_path = os.path.join(os.path.dirname(__file__), "static")

APP_ID = '18771025'
API_KEY = '8BIx1GW9fuY9ifIGz3Gsoh64'
SECRET_KEY = 'GEibugw0IPpi8kp7dUQG5qF0rAqLnFzR'

IP = '127.0.0.1'
if(platform.system() == 'Linux'):
    IP = '0.0.0.0'
PORT = 9999