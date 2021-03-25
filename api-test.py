import requests
import pickle
import hashlib 
import secrets
import pandas as pd
from datetime import datetime
import re,os

path = os.path.dirname(__file__)
path = path.replace("\\","/")
print(path)
# generated_key = secrets.token_urlsafe(16)
# generated_key.replace("-","")
# token = "14117220" + generated_key
# print(generated_key)
# print("token",token)

# password = npm+token
# result = hashlib.md5(password.encode())

# print("password",result.hexdigest())


base = "http://127.0.0.1:5000/"
base = "https://bot-um.herokuapp.com/"

nama = "Muhammad Rizdalah Agisa"
npm = "14117220"
kelas = "4ka13"
key = "56212152172004422125" # Key UM yang ada di studentsite
token_user = "PHBzPlMI2JdWVyrRzdbZg" #token yang diberikan dari owner

nama_matkul = "Pendidikan Pancasila"  #nama matkul yang akan di kerjakan
token_matkul = "" #token matkul yang ada di daftar matkul

def kunci():
    data = {
        "npm" : "14117220",
        "token_user" : "PHBzPlMI2JdWVyrRzdbZg",
        "soal" : '"Do you know what she is going ?" He asked me if .......',
        "token_matkul" : "QZflwT0ef0DBlHv1tuGKTw",
        "path" : "D:/rizda"
    }
    result = requests.post(base+"kunci",json=data)
    print(result.json())


def login():
    data = {"npm" : npm, "nama":nama, "kelas": kelas, "token_user" : token_user,"nama_matkul":nama_matkul}
    result = requests.post(base+"login",json=data)
    print(result.json())

def create():
    data = {"npm" : npm, "nama":nama, "kelas": kelas}
    result = requests.post(base+"create_user",json=data)
    print(result.json())

# create()