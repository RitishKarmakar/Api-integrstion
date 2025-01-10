from flask import *
from forms import *
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin , login_user , logout_user,current_user,login_required
from email_validator import *
from flask_sqlalchemy import *

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
posts={}
repost={"Post Title":"","Post Content":"","img":""}
reposts=[]
app.config['SECRET_KEY'] = 'c3cd2ebbf3ec8769038812e04a81e574a0aa9461601dc198'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True , nullable = False)
    email = db.Column(db.String(120), nullable = False)
    image_file = db.Column(db.String(120) , nullable = False ,default = "download.png")
    password = db.Column(db.String(60),nullable = False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
@app.route('/Signin', methods = ["GET","POST"])
def SignIn():
    if current_user.is_authenticated:
        return redirect('Dash')
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        with app.app_context():
            user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user( user,remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Dash'))
            flash(f'The account is sucessfully Logged in {form.email.data}!','sucess')
        #print(form.password.data)
        
    else:
        flash(f'The account is Unsucessfull Logged {form.email.data}!','sucess')
    return render_template("signin.html",title ='signin' , form =form)
@app.route('/')
def Home():

    return render_template("home.html")
@app.route('/Dash')
@login_required
def Dash():
    
    image_file = url_for('static',filename='profilepics/'+current_user.image_file)
    return render_template('Dash.html',image_file =image_file)
@app.route('/signup', methods = ["GET","POST"])
def Signup():
    # if request.method=="POST":
    #     Name=request.form.get("user_name")
    #     print(Name)
    #     return render_template("Data_Form.html")
    if current_user.is_authenticated:
        return redirect('Dash')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf -8')
        user = User(username = form.username.data,email = form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'The account is sucessfully created for {form.username.data}!','sucess')
        print(form.username.data)
        print(form.password.data)
        return redirect(url_for('SignIn'))
    return render_template("signup.html",title ='signup' , form =form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Home'))
@app.route("/form1",methods=['GET', 'POST'])
def Form1():
    if request.method == 'POST':
        # Get general data
        name = request.form['name']
        quote = request.form['Quote']
        contact = request.form['contact']
        summary = request.form['summary']
        service_brief = request.form['ServiceBrief']
        service_data = {
            'service1': request.form['service1'],
            's1d': request.form['s1d'],
            'service2': request.form['service2'],
            's2d': request.form['s2d'],
            'service3': request.form['service3'],
            's3d': request.form['s3d'],
            'service4': request.form['service4'],
            's4d': request.form['s4d'],
            'service5': request.form['service5'],
            's5d': request.form['s5d'],
            'service6': request.form['service6'],
            's6d': request.form['s6d']
        }

        # Store general data
        # You can store the data in a database or any other storage mechanism
        # For simplicity, let's just print it for now
        print("General Data:")
        print("Name:", name)
        print("Quote:", quote)
        print("Contact:", contact)
        print("Summary:", summary)
        print("Service Brief:", service_brief)
        print("Service Data:", service_data)
        print(request.files)
        # Get and store posts data with uploaded images
        for key in request.files:
            
            if key.startswith('post-image-'):
                post_title = request.form.get('Post_title-' + key.split('-')[-1])
                post_content = request.form.get('post-content-' + key.split('-')[-1])
                image_file = request.files[key]
                repost["Post Title"]=post_title
                repost["Post Content"]=post_content
                if image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print("Post Title:", post_title)
                    print("Post Content:", post_content)
                    print("Image File Saved as:", filename)

                    # Add post to the dictionary if the title is unique
                    if post_title not in posts:
                        posts[post_title] = {
                            'content': post_content,
                            'image': filename
                        }
                    else:
                        print("Post title already exists, skipping.")

        return redirect()

    return render_template('Form.html')
@app.route("/form2",methods=['GET', 'POST'])
def Form2():
    if request.method == 'POST':
        # Get general data
        name = request.form['name']
        quote = request.form['Quote']
        contact = request.form['contact']
        summary = request.form['summary']
        service_brief = request.form['ServiceBrief']
        service_data = {
            'service1': request.form['service1'],
            's1d': request.form['s1d'],
            'service2': request.form['service2'],
            's2d': request.form['s2d'],
            'service3': request.form['service3'],
            's3d': request.form['s3d'],
            'service4': request.form['service4'],
            's4d': request.form['s4d'],
            'service5': request.form['service5'],
            's5d': request.form['s5d'],
            'service6': request.form['service6'],
            's6d': request.form['s6d']
        }

        # Store general data
        # You can store the data in a database or any other storage mechanism
        # For simplicity, let's just print it for now
        print("General Data:")
        print("Name:", name)
        print("Quote:", quote)
        print("Contact:", contact)
        print("Summary:", summary)
        print("Service Brief:", service_brief)
        print("Service Data:", service_data)
        print(request.files)
        General_data = {
            "Name:":name
            ,"Quote:": quote
            ,"Contact:": contact
            ,"Summary:":summary
            ,"Service Brief:":service_brief
            }
        # Get and store posts data with uploaded images
        repost={"Post Title":"","Post Content":"","img":""}
        post_titles_prop = request.form.getlist('Post_title')
        post_contents_prop = request.form.getlist('post-content')
        post_images_prop = request.files.getlist('post-image')

        repost["Post Title"]=post_titles_prop

        repost["Post Content"]=post_contents_prop
        
        
        for key in request.files:
            
            if key.startswith('post-image-'):
                post_title = request.form.get('Post_title-' + key.split('-')[-1])
                post_content = request.form.get('post-content-' + key.split('-')[-1])
                image_file = request.files[key]
                
                if image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print("Post Title:", post_title)
                    print("Post Content:", post_content)
                    print("Image File Saved as:", filename)
                    repost["img"]=filename
                    reposts.append(repost)
                    # Add post to the dictionary if the title is unique
                    if post_title not in posts:
                        posts[post_title] = {
                            'content': post_content,
                            'image': filename
                        }
                    else:
                        print("Post title already exists, skipping.")

        return render_template('Anger.html',reposts = reposts,GN = General_data,SD = service_data)

    return render_template('Form.html')


if __name__ == '__main__':
    while True:
        app.run(debug=True)
