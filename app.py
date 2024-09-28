#!/usr/bin/env python3

"""
This is the main web file, it handles how the app interacts with servers
and  loads necessary pages.
"""

import os
from flask import Flask, flash, send_from_directory, render_template, url_for, request, redirect
from flask_admin.form import FileUploadField
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError
from flask_admin.form.widgets import Select2Widget
from flask_admin.form import rules
from wtforms_sqlalchemy.fields import QuerySelectField

"""Configuration section."""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forest4life_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['UPLOAD_FOLDER'] = 'uploads/'


db = SQLAlchemy(app) #connecting the app to the database sqlalchemy
admin = Admin(app, name='Forest4life Admin', template_mode='bootstrap3')#Configuring the admin interface for app
login_manager = LoginManager()
migrate = Migrate(app, db)
login_manager.init_app(app) #Connecting the app to flask loginmanager


""" classes used for forest4life project."""

class Address(db.Model):
    """
    This class contains all address and
    contact information for the forest4life company.
    and it will be used to update them.
    """
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    instagram = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    facebook = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    location = db.Column(db.String(120),  default="Kigali-Rwanda", nullable=False)
    tel = db.Column(db.String(16), default="+250781650592", nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class Project(db.Model):
    """This class contains all information about ongoing projects."""
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Text, nullable=True)
    impact = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    uploads = db.relationship('Upload', backref='project', lazy=True)
    summary= db.Column(db.String(250), nullable=False, default='')

class Upload(db.Model):
    """This table stores all information about uploads image."""
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(120), nullable=True)
    post_description = db.Column(db.Text, nullable=False)
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)


class Us(db.Model):
    """This class stores every single profile information about forest4life."""
    id = db.Column(db.Integer, primary_key=True)
    mission = db.Column(db.Text, nullable=False)
    vision = db.Column(db.Text, nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    short_introduction = db.Column(db.Text, nullable=False)
    home_background_picture = db.Column(db.String(150), nullable=False)
    about_us_background_picture = db.Column(db.String(150), nullable=False)


class Partners(db.Model):
    """Contains all information about partners."""
    id = db.Column(db.Integer, primary_key=True)
    link_address = db.Column(db.String(150), nullable=True)
    logo = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=True)
    
class Founders(db.Model):
    """This contains our founders profile."""
    id = db.Column(db.Integer, primary_key=True)
    Full_name = db.Column(db.String(150), nullable=False, unique=True)
    profile = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(150), nullable=False)


class AdminUser(UserMixin, db.Model):
    """This class manages admins of this website."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, nullable=False)

class Service(db.Model):
    """This class defines all services provided by forest4life."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)    


class Blog(db.Model):
    """This class stores all the blogs of the forest4life."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    main_pic = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())
    introduction_paragraphy = db.Column(db.Text, nullable=False)    
    introduction_pic = db.Column(db.String(150), nullable=False)
    paragraphy_1_heading = db.Column(db.Text, nullable=False)    
    content_paragraphy_1 = db.Column(db.Text, nullable=False)    
    paragraphy_1_pic_1 = db.Column(db.String(150), nullable=False)
    paragraphy_1_pic_2 = db.Column(db.String(150), nullable=False)
    paragraphy_2_heading = db.Column(db.Text, nullable=False)    
    content_paragraphy_2 = db.Column(db.Text, nullable=False)    
    paragraphy_2_pic_1 = db.Column(db.String(150), nullable=False)
    paragraphy_2_pic_2 = db.Column(db.String(150), nullable=False)
    paragraphy_2_pic_3 = db.Column(db.String(150), nullable=False)
    conclusion_paragraphy = db.Column(db.Text, nullable=False)    
    
    
    
 
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    
class SubFileUploadField(FileUploadField):
    """This class overlides the __save_file method to allow storage of full path."""

    def _save_file(self, data, filename):
        """Return the full path of the file."""
        temp_path = super()._save_file(data, filename)
        return os.path.join(app.config['UPLOAD_FOLDER'], temp_path)


class UsModelView(ModelView):
    """Handles FileUploadFields in the us and founders classes."""
    form_overrides = {'home_background_picture': SubFileUploadField,
                      'about_us_background_picture': SubFileUploadField,
                      'picture': SubFileUploadField,
                      'main_pic' : SubFileUploadField,
                      'introduction_pic' : SubFileUploadField,
                      'paragraphy_1_pic_1' : SubFileUploadField,
                      'paragraphy_1_pic_2' : SubFileUploadField,
                      'paragraphy_2_pic_1' : SubFileUploadField,
                      'paragraphy_2_pic_2' : SubFileUploadField,
                      'paragraphy_2_pic_3' : SubFileUploadField,
                      'logo': SubFileUploadField,
                      }

    form_args = {'home_background_picture': {'base_path': app.config['UPLOAD_FOLDER']},
                 'about_us_background_picture': {'base_path': app.config['UPLOAD_FOLDER']},
                 'picture': {'base_path': app.config['UPLOAD_FOLDER']},
                 'main_pic' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'introduction_pic' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'paragraphy_1_pic_1' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'paragraphy_1_pic_2' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'paragraphy_2_pic_1' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'paragraphy_2_pic_2' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'paragraphy_2_pic_3' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'url' : {'base_path': app.config['UPLOAD_FOLDER']},
                 'logo' : {'base_path': app.config['UPLOAD_FOLDER']}
                 }
    
class AdminFileUploadView(ModelView):
    """This defines how Upload class will handle picture posts."""
    form_overrides = {'photo' : SubFileUploadField,
                      'project_id' : QuerySelectField,
                      }

    
    form_args = {'project_id': {'query_factory': lambda: Project.query.all(),
                                'get_label': 'title',                         
                                'blank_text': 'Please! Select a Project',     
                                'widget': Select2Widget()                     
                                },
                 'photo': {'base_path': app.config['UPLOAD_FOLDER']}
                 }
    
    form_columns = ['photo', 'project_id', 'post_description']
    
    def on_model_change(self, form, model, is_created):
        """Save project.id instead of whole object."""
        if form.project_id.data:
            model.project_id = form.project_id.data.id



admin.add_view(AdminModelView(Address, db.session))
admin.add_view(AdminModelView(Project, db.session))
admin.add_view(AdminModelView(Service, db.session))
admin.add_view(AdminModelView(AdminUser, db.session))
admin.add_view(UsModelView(Us, db.session))
admin.add_view(UsModelView(Founders, db.session))
admin.add_view(UsModelView(Blog, db.session))
admin.add_view(UsModelView(Partners, db.session))
admin.add_view(AdminFileUploadView(Upload, db.session))


with app.app_context():
    db.create_all()

"""Login manager tools."""

@login_manager.user_loader
def user_loader(userid):
    """Return the user whose id is given."""
    return AdminUser.query.get(int(userid))


""" Page routes."""
@app.route('/blog/<blog_id>', strict_slashes=False)
@app.route('/blog', defaults={'blog_id':None}, strict_slashes=False)
def blog(blog_id):
    """Return blog page."""
    if blog_id:
        blog = Blog.query.get(blog_id)
        addresses = Address.query.get(1)
        us = Us.query.get(1)
        partners = Partners.query.all()
        return render_template('individual_blogs.html',
                               blog=blog,
                               partners=partners,
                               us=us,
                               addresses=addresses)
        
    else:
        blog = Blog.query.all()
        addresses = Address.query.get(1)
        partners = Partners.query.all()
        us = Us.query.get(1)
        return render_template('blogs.html',
                               blogs=blog,
                               us=us,
                               partners=partners,
                               addresses=addresses)


@app.route('/', strict_slashes=False)
def home_page():
    """Return a home page for forest4life project."""
    projects = Project.query.all()
    addresses = Address.query.get(1)
    us = Us.query.get(1)
    partners = Partners.query.all()
    services = Service.query.all()
    return render_template('home.html',
                           us=us,
                           partners=partners,
                           services=services,
                           projects=projects,
                           addresses=addresses)


@app.route('/project/', defaults={'project_id': None}, strict_slashes=False)
@app.route('/project/<project_id>', strict_slashes=False)
def all_project(project_id):
    """Return project page."""
    if project_id:
        us = Us.query.get(1)
        project = Project.query.get(project_id)
        addresses = Address.query.get(1)
        partners = Partners.query.all()
        return render_template('individual_project.html',
                               addresses=addresses,
                               partners=partners,
                               us=us,
                               project=project)
    else:
        us = Us.query.get(1)
        projects = Project.query.all()
        partners = Partners.query.all()
        addresses = Address.query.get(1)
        return render_template('projects.html',
                               addresses=addresses,
                               partners=partners,
                               us=us,
                               projects=projects)
        

@app.route('/about', strict_slashes=False)
def about_us():
    """Return about page."""
    us = Us.query.get(1)
    founders = Founders.query.all()
    addresses = Address.query.get(1)
    partners = Partners.query.all()
    return render_template('about_us.html',
                           addresses=addresses,
                           us=us,
                           partners=partners,
                           founders=founders)

"""end for page routes."""

""" helpfull but not page  routes. """

@app.before_request
def before_request():
    if not current_user.is_authenticated and (request.path == '/admin' or
                                              request.path == '/admin/'):
        return redirect(url_for('login'))

    
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Handle log_in."""
    if request.method == 'POST':
        name = request.form.get('Username')
        password = request.form.get('password')
        check_adm = AdminUser.query.filter_by(username=name).first()
        if check_adm and check_adm.password == password:
               login_user(check_adm)
               return redirect(url_for('admin.index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/project/uploads/<filename>')
@app.route('/blog/uploads/<filename>')
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

    
@app.route('/logout')
@login_required
def logout():
    """logout this user."""
    logout_user()
    return redirect(url_for('home_page'))


"""end for the non-page routes."""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
