import pymysql
import config
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import InputRequired,Length,Email,URL
import os
from flask import flash,session
from werkzeug.security import check_password_hash
db=cursor=None

class Db():
    def OpenDB(self):
        global db,cursor
        self.db=pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor=self.db.cursor()
    def closeDB(self):
        global db,cursor
        self.db.close()
    def cursor(self):
        return self.db.cursor()
    
class Crud(Db):
    def select_produk(self):
        self.OpenDB()
        cursor.execute("SELECT * FROM produk")
        data=cursor.fetchall()
        self.closeDB()
        return data
    def insert(self,data):
        self.OpenDB()
        print(data)
        cursor.execute("INSERT INTO produk(thumnail,produk,kategori,harga) VALUES('%s','%s','%s','%s')" %data)
        self.db.commit()
        self.closeDB() 
    def delete(self,id):
        self.OpenDB()
        # hapus img 
        cursor.execute("SELECT thumnail FROM produk WHERE id='%s'"%id)
        data_img=cursor.fetchone()[0]
        print('ini data imggg',data_img)
        folder='static/uploads/'
        file_path = os.path.join(folder, data_img)
        if os.path.isfile(file_path):
            os.remove(file_path)
        # hapus dosen
        cursor.execute("DELETE from produk WHERE id='%s'" %id)
        self.db.commit()
        self.OpenDB()
    def get_id_update(self,id):
        self.OpenDB()
        cursor.execute("SELECT * FROM produk WHERE id='%s'"%id)
        data=cursor.fetchone()
        self.closeDB()
        return data
    def update_with_img(self,data):
        self.OpenDB()
        print(data)
        cursor.execute("UPDATE produk SET thumnail='%s', produk='%s',kategori='%s',harga='%s' WHERE id='%s'" %data)
        self.db.commit()
        self.closeDB()
    def update(self,data):
        self.OpenDB()
        print(data)
        cursor.execute("UPDATE produk SET produk='%s',kategori='%s',harga='%s' WHERE id='%s'" %data)
        self.db.commit()
        self.closeDB()

class Crud_pendaftaran(Db):
    def select(self):
        self.OpenDB()
        cursor.execute("SELECT * FROM pendaftaran")
        data=cursor.fetchall()
        self.closeDB()
        return data
    def insert(self,data):
        self.OpenDB()
        print(data)
        cursor.execute("INSERT INTO pendaftaran(nama,nik,wa,email,pelatihan) VALUES('%s','%s','%s','%s','%s')" %data)
        self.db.commit()
        self.closeDB() 
    def get_id_pendaftar(self):
        self.OpenDB()
        cursor.execute("SELECT * FROM pendaftaran WHERE id='1'")
        data=cursor.fetchone()
        self.closeDB()
        return data
    def update_pendafar(self,data):
        self.OpenDB()
        print(data)
        cursor.execute("UPDATE pendaftaran SET nama='%s',nik='%s',wa='%s',email='%s',pelatihan='%s' WHERE id='%s'" %data)
        self.db.commit()
        self.closeDB()
    def delete(self,id):
        self.OpenDB()
        cursor.execute("DELETE from pendaftaran WHERE id='%s'" %id)
        self.db.commit()
        self.OpenDB()