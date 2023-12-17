from cloud import app,db
from cloud.model import User,Upload
from flask import Flask,render_template,redirect,send_file,request,flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_login import LoginManager,logout_user,login_required,login_user,login_manager,current_user
from io import BytesIO



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>/Home')
@login_required
def Home(name):
    return render_template('home.html',name=name,Upload=Upload.query.filter_by(owned_user=User.query.filter_by(username=name).first().id).limit(5).all())


@app.route('/<name>/AllFiles')
@login_required
def allfiles(name):
    return render_template('allfiles.html',name=name,Upload=Upload.query.filter_by(owned_user=User.query.filter_by(username=name).first().id).all())


@app.route('/<name>/upload',methods=['GET','POST'])
# @login_required
def upload(name):
    if request.method == 'POST':
            try:
                file = request.files['file']
                if file.filename == '':
                    flash("Please Select File To Upload")
                else:
                
                    upload = Upload(filename= secure_filename(file.filename), data=file.read(),owned_user=User.query.filter_by(username=name).first().id)
                    db.session.add(upload)
                    db.session.commit()
                    flash(f'Uploaded: {file.filename}')
            except RequestEntityTooLarge:
                flash("File Greater Than 50 MB Can't Uploaded")
         
    return redirect(f'/{name}/Home')

@app.route('/<name>/download/<int:id>',methods=['GET','POST'])
@login_required
def download(id,name): 
    upload = Upload.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)

@app.route('/<name>/remove/<int:id>',methods=['GET','POST'])
@login_required
def remove(id,name): 
    upload = Upload.query.filter_by(id=id).first()
    db.session.delete(upload)
    db.session.commit()
    flash("File Deleted Permanently")
    return redirect(f"/{name}/AllFiles")



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = User(username=username,password=password)
            db.session.add(user)
            db.session.commit()
            flash("Account Successfully Created ")
            return redirect('/login')
        except:
            flash("Username Already Exist , Please Select Unique Username")
    return render_template('signup.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usernameverify = User.query.filter_by(username=username).first()
        passwordverify = User.query.filter_by(password=password).first()
        if usernameverify and passwordverify:
            login_user(usernameverify)
            flash("Login Successful")
            return redirect(f"/{username}/Home")
        else:
            flash("Invalid Username And Password")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful")
    return redirect('/login')

