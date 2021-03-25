import requests
import pickle
import hashlib 
import secrets
import pandas as pd
from datetime import datetime
import re
from data import npm,nama,kelas,token_user,nama_matkul,token_matkul,key


# generated_key = secrets.token_urlsafe(16)
# generated_key.replace("-","")
# token = "14117220" + generated_key
# print(generated_key)
# print("token",token)

# password = npm+token
# result = hashlib.md5(password.encode())

# print("password",result.hexdigest())


base = "http://127.0.0.1:5000/"
# base = "https://bot-um.herokuapp.com/"

data = {
    "npm_user" : "14117220",
    "admin_token" : "PHBzPlMI2JdWVyrRzdbZg",
    "login_token" : "",
    "soal" : '"Do you know what she is going ?" He asked me if .......',
    "kode" : "KD021216"
}

data2= {
    "nama": nama,
    "kelas" : kelas,
    "npm" : npm
}

data3={
    "npm_admin": "14117220",
    "admin_token" : "PHBzPlMI2JdWVyrRzdbZg",
    "npm_user" : "14117220",
    "nama_user" : "Muhammad Rizdalah Agisa",
    "kelas_user" : "4ka13",
    "kode_matkul" : "KK011321",
    "matkul" : "SISTEM IMPLEMENTASI"
}
data = {
    "npm" : "14117220",
    "token_user" : "PHBzPlMI2JdWVyrRzdbZg",
    "soal" : '"Do you know what she is going ?" He asked me if .......',
    "token_matkul" : "QZflwT0ef0DBlHv1tuGKTw",
    "path" : "D:/rizda"
}

# result = requests.post(base+"kunci",json=data)
data = {"npm" : npm, "nama":nama, "kelas": kelas, "token_user" : token_user,"nama_matkul":nama_matkul}
result = requests.post(base+"login",json=data)
# data['login_token'] = "6MfR5pkGvHLp09YhTnA3lg"
# print(data)
# result = requests.post(base+"/kunci/",data=data)
# print(data2)
# result = requests.post(base+"/create_user/",data=data2)

print(result.json())