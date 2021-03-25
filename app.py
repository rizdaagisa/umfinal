from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pandas as pd
import csv
import hashlib
import secrets
from datetime import datetime
import re,os,sys
import shutil

# file_path = "odbc"
# sys.path.append(os.path.dirname(file_path))

# https://stackoverflow.com/questions/51122790/install-odbc-driver-heroku
# https://elements.heroku.com/buildpacks/matt-bertoncello/python-pyodbc-buildpack
# https://github.com/matt-bertoncello/python-pyodbc-buildpack

app = Flask(__name__)


def create_user(nama,kelas,npm):
    try:
        with open(r'DB_admin.csv', 'a', newline='') as csvfile:
            generated_key = secrets.token_urlsafe(16)
            token = generated_key.replace("-","").replace("_","")
            password = hashlib.md5((str(npm)+token).encode()).hexdigest()
            fieldnames = ['nama','npm', 'kelas', 'password','token']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'nama': nama,
                            'npm': npm,
                            'kelas': kelas,
                            'password': password,
                            'token': token
                        })
            return {"npm":npm,"user_token" : token, "status": "sukses"}
    except:
        return {'status' : 'failed create user'}

def cek_user(npm,token):
    df = pd.read_csv("DB_admin.csv")
    # try:
    password = df.loc[df["npm"]  == npm]['password'][0]
    # password = (df['password'].where(df['npm'] == npm))[0]
    # token = (df['token'].where(df['npm'] == npm))[0]
    # credit = df.loc[df["npm"]  == npm]['credit'][0]
    # print("credit",credit)
    cek = str(npm)+token
    valid = hashlib.md5(cek.encode()).hexdigest()
    if valid == password:
        return True
    else:
        return False

def kuncijawaban(soal,token,path):
    df = pd.read_csv("DB_matkul.csv", index_col=0)
    kode = df.loc[df["token_matkul"]  == str(token)]['KD_matkul'][0]
    file = df.loc[df["token_matkul"]  == str(token)]['nama_file'][0]
    driver = r"Driver={MICROSOFT ACCESS DRIVER (*.mdb)};"
    dbq = "Dbq="+path+"/configuration/" + file + ".mdb;"
    cons = driver + dbq
    # dbq = "Dbq=D:/rizda/note/api-botum/" + kode + ".mdb;"
    # try:
    if ('"' in soal):
        try:
            starind = soal.find('\"')
            endind= soal.find('\"',starind+1)
            soal1= soal[starind+1:endind]
            try:
                soal2= re.findall('"(.*?)"', soal)[0]
            except:
                soal2= ""
            soal3=  soal[endind+2:]
            query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal1 + "%'" + " and soal like '%" + soal2 +"%'" + " and soal like '%" + soal3 +"%'"
        except:
            soal = soal.split('"')
            soal1= soal[0]
            soal2= soal[1]
            soal3=soal[3]
            query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal1 + "%'" + " and soal like '%" + soal2 +"%'" + " and soal like '%" + soal3 +"%'"
        finally:
            soal = soal.split('"')
            soal1= soal[0]
            soal2= soal[1]
            query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal1 + "%'" + " and soal like '%" + soal2 +"%'"
    elif("'" in soal):
        try:
            starind = soal.find("'")
            endind= soal.find("'",starind)
            soal1= soal[0:starind]
            soal2= soal[starind+1:-1]
            query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal1 + "%'" + " and soal like '%" + soal2 +"%'"
        except:
            soal = soal.split("'")
            soal1= soal[0]
            soal2= soal[1]
            query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal1 + "%'" + " and soal like '%" + soal2 +"%'"
        finally:
            soal = soal.split("'")
            soal1= soal[0]
            query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal1 + "%'"
    else:
        query = "SELECT soal,A,B,C,D,kunci FROM " + kode + " WHERE soal like '%" + soal + "%'"
    return query, cons    
    # except:
    #     print("error")
    
    # try:
    #     cur.tables()
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #     print(rows)
    #     kunci = rows[0]['kunci']
    #     if rows[0][kunci] == None:
    #         jawaban = rows[0][kunci.lower()]
    #     else:
    #         jawaban = rows[0][kunci]
    #     return (jawaban)
    # except:
    #     return ("Pass / Tidak menjawab")

@app.route('/',methods=['GET'])
def index():
    return 'Upss mau iseng ya? Silakan hubungi admin untuk membeli program bot UM'

@app.route('/create_user',methods=['POST'])
def user():
    result = request.get_json()
    npm = result['npm']
    nama = result['nama']
    kelas = result['kelas']
    df = pd.read_csv("DB_admin.csv")
    np = df.loc[df['npm'] == str(npm)]
    print(np)
    if(np.empty):
        data = create_user(nama,kelas,npm)
        return data
    else:
        return {'status' : 'User sudah ada didalam database'}

@app.route('/kunci',methods=['POST'])
def kunci():
    result = request.get_json()
    npm = result['npm']
    soal = result['soal']
    token = result['token_matkul']
    api_key = result['token_user']
    path = result['path']
    password = cek_user(int(npm),api_key)
    if password == True:
        query,driver  = kuncijawaban(soal,token,path)
        return {'driver' : driver, 'key':query, 'status':'ok'}
    else:
        return {'status' : 'User tidak valid, silakan lakukan pembelian token di instagram @jokiambis'}

@app.route('/login',methods=['POST'])
def login_request():
    result = request.get_json()
    nama = result['nama']
    npm = result['npm']
    kelas = result['kelas']
    matkul = result['nama_matkul']
    api_key = result['token_user']
    password = cek_user(int(npm),api_key)
    tanggal= datetime.now().strftime("%d %B %Y:%H.%M")
    if password == True:
        fieldnames = ['npm_user','nama_user','kelas_user','matkul','tanggal']
        with open(r'DB_user.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'npm_user':npm,'nama_user':nama,'kelas_user':kelas,'matkul':matkul,'tanggal':tanggal})
        return {'status':'Sukses'}
    else:
        return {'status' : 'Token user salah, silakan lakukan pembelian token di instagram @jokiambis'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)