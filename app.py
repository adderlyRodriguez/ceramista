import os
import smtplib
from datetime import datetime
from flask_migrate import Migrate
#from.models import Project
# Es crucial importar 'desc' para el ordenamiento descendente
# from sqlalchemy import desc 

from email.message import EmailMessage
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# --------------------------------------------------
# Variables de entorno
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# App
# --------------------------------------------------
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_local')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///db.sqlite3'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------------------------------
# Cloudinary
# --------------------------------------------------
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# --------------------------------------------------
# MODELOS
# --------------------------------------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(500), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # AGREGAR ESTO
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )
    category = db.relationship('Category', backref='projects')

# --------------------------------------------------
# Crear tablas
# --------------------------------------------------
with app.app_context():
    db.create_all()

# --------------------------------------------------
# Categorías disponibles en todos los templates
# --------------------------------------------------
@app.context_processor
def inject_categories():
    return dict(categories=Category.query.all())
#
migrate = Migrate(app, db)
# --------------------------------------------------
# RUTAS
# --------------------------------------------------
@app.route('/inicio')
def inicio():
    # CAMBIO LÓGICO:
    # 1. Proyecto.category.asc(): Agrupa alfabéticamente (A-Z)
    # 2. Proyecto.date.desc(): Ordena los más recientes primero dentro del grupo
    projects = Project.query.order_by(
        Project.category_id.asc(),
        Project.date.desc()
    ).all()
    
    return render_template('inicio.html', projects=projects)



@app.route('/')
def portfolio():
    # Deshabilita el modo admin al entrar al Inicio
    session.pop('admin', None) 
    projects = Project.query.order_by(Project.date.desc()).all()
    # projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)

@app.route('/category/<int:category_id>')
def projects_by_category(category_id):
    projects = Project.query.filter_by(category_id=category_id).order_by(Project.date.desc()).all()
    return render_template('portfolio.html', projects=projects)


# ---------------- ADMIN ----------------

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('code') == os.getenv('ADMIN_CODE'):
            session['admin'] = True
            return redirect(url_for('new_project'))
        return "Código incorrecto", 403

    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('portfolio'))


# ---------------- CRUD PROYECTOS ----------------

@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        file = request.files.get('file')
        upload = cloudinary.uploader.upload(file, resource_type="auto")

        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            media_url=upload['secure_url'],
            media_type=upload['resource_type'],
            category_id=request.form.get('category')
        )
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('portfolio'))

    return render_template('create_project.html')


@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.category_id = request.form.get('category')
        if request.form.get('date'):
            from datetime import datetime
            project.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')

        file = request.files.get('file')
        if file:
            upload = cloudinary.uploader.upload(file, resource_type="auto")
            project.media_url = upload['secure_url']
            project.media_type = upload['resource_type']

        db.session.commit()
        return redirect(url_for('portfolio'))

    return render_template('edit_project.html', project=project)


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('portfolio'))


# ---------------- CONTACTO ----------------

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = EmailMessage()
        msg['Subject'] = request.form.get('subject')
        msg['From'] = os.getenv('EMAIL_SENDER')
        msg['To'] = os.getenv('EMAIL_RECEIVER')

        msg.set_content(f"""
Nombre: {request.form.get('name')}
Email: {request.form.get('email')}

Mensaje:
{request.form.get('message')}
""")

        with smtplib.SMTP(os.getenv('EMAIL_HOST'),
                          int(os.getenv('EMAIL_PORT'))) as server:
            server.starttls()
            server.login(
                os.getenv('EMAIL_SENDER'),
                os.getenv('EMAIL_PASSWORD')
            )
            server.send_message(msg)

        return redirect(url_for('portfolio'))

    return render_template('contact.html')


# --------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)