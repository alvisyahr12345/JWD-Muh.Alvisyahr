from flask import Flask,render_template,request, redirect, url_for
from models import *
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash


app=Flask(__name__)
app.config['SECRET_KEY']='085828548757845'
app.config['UPLOAD_FOLDER'] = "static/uploads"

@app.route("/", methods=['POST','GET'])
def index():
    return render_template('beranda.html')

@app.route("/pendaftaran", methods=['POST','GET'])
def pendaftaran():
    model=Crud_pendaftaran()
    if request.method == 'POST':
        name = request.form['nama']
        nik = request.form['nik']
        wa = request.form['wa']
        email = request.form['email']
        pelatihan = request.form['pelatihan']

        data=(name,nik,wa,email,pelatihan)

        model.insert(data)
        return render_template('pendaftar.html')
    
    return render_template('pendaftaran.html')

@app.route("/pendaftar", methods=['POST','GET'])
def pendaftar():
    model=Crud_pendaftaran()

    pendaftar=model.select()

    return render_template('pendaftar.html', pendaftar=pendaftar)

@app.route("/update_pendaftar/", methods=['POST','GET'])
def update_pendaftar():
    print("ini id:",id)
    id_tes=1

    model=Crud_pendaftaran()
    if request.method == 'POST':
        name = request.form['nama']
        nik = request.form['nik']
        wa = request.form['wa']
        email = request.form['email']
        pelatihan = request.form['pelatihan']

        data=(name,nik,wa,email,pelatihan,id_tes)

        model.update_pendafar(data)

        return redirect(url_for('pendaftar'))

    model=Crud_pendaftaran()
    pendaftar=model.get_id_pendaftar()

    print(pendaftar)

    return render_template('update_pendaftar.html', pendaftar=pendaftar)


@app.route("/delete_pendaftar/", methods=['POST','GET'])
def delete_pendaftar():
    print("ini id:",id)
    id_tes=3

    model=Crud_pendaftaran()

    model.delete(id_tes)
    
    return redirect(url_for('pendaftar'))








@app.route("/dashboard", methods=['POST','GET'])
def dashboard():
    if 'Login' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route("/product", methods=['POST','GET'])
def product():
    model=Crud()

    if request.method == 'POST':
            f = request.files['image']  
            filename = str(uuid.uuid4()) + secure_filename(f.filename) # mengacak nama
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            img=str(filename)
            print("ini imgggg:",img)

            produk = request.form['produk']
            kategori = request.form['kategori']
            harga = request.form['harga']

            data=(img,produk,kategori,harga)

            model.insert(data)

    produk=model.select_produk()

    if 'Login' in session:
        return render_template('product.html',produk=produk)
    return redirect(url_for('login'))

@app.route("/delete/<int:id>", methods=['POST','GET'])
def delete(id):
    print("ini id:",id)

    model=Crud()

    model.delete(id)
    
    return redirect(url_for('product'))

@app.route("/update/<int:id>", methods=['POST','GET'])
def update(id):
    print("ini id:",id)

    model=Crud()
    if request.method == 'POST':
        produk_name = request.form['produk']
        kategori = request.form['kategori']
        harga = request.form['harga']
        
        if 'image' in request.files:
            f = request.files['image']
            filename = str(uuid.uuid4()) + secure_filename(f.filename) # Mengacak nama
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("Image uploaded:", filename)
            img=str(filename)

            data=(img,produk_name,kategori,harga,id)
            model.update_with_img(data)
        
        data=(produk_name,kategori,harga,id)
        model.update(data)
        return redirect(url_for('product'))

    produk=model.get_id_update(id)
    print("ini produklllll:",produk)
    
    return render_template('update.html',produk=produk)

@app.route("/register",methods=['GET','PoST'])
def register():
    if request.method =='POST':
        firstname=request.form['firstName'] 
        lastname=request.form['lastName']
        email=request.form['email']
        password=request.form['password']
        data=firstname,lastname,email,generate_password_hash(password)
        model=Db()
        model.OpenDB()
        cursor = model.cursor()
        cursor.execute("INSERT INTO user(first_name,last_name,email,password) VALUES('%s','%s','%s','%s')"%data )
        model.closeDB()
    return render_template("register.html") 

@app.route("/login",methods=['GET','POST'])
def login():
    if 'Login' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email=request.form['email'] 
        password=request.form['password']      
        print("masukkkkk")
        model=Db()
        model.OpenDB()
        cursor = model.cursor()
        cursor.execute('SELECT * FROM user WHERE email=%s',(email,))
        akun = cursor.fetchone()
        if akun is None:
            print('Akuntidak adaaaaa')
        elif not check_password_hash(akun[4], password):
            print('Passwordsalahhhhhhhhhh')
        else:
            session['Login'] = True
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('Login', None)
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)
