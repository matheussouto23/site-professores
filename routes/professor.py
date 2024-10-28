from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from models import Class, Material
from config import UPLOAD_FOLDER

# Criação do Blueprint para rotas do professor
professor = Blueprint('professor', __name__)

# Rota para o painel principal do professor
@professor.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é exclusiva para professores.', category='error')
        return redirect(url_for('main.dashboard'))
    
    classes = Class.query.filter_by(professor_id=current_user.id).all()
    return render_template('professor/dashboard.html', classes=classes)

# Rota para criar uma nova turma
@professor.route('/create_class', methods=['GET', 'POST'])
@login_required
def create_class():
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é exclusiva para professores.', category='error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        
        if class_name:
            new_class = Class(name=class_name, professor_id=current_user.id)
            db.session.add(new_class)
            db.session.commit()
            flash('Turma criada com sucesso!', category='success')
            return redirect(url_for('professor.dashboard'))
        else:
            flash('O nome da turma é obrigatório.', category='error')
    
    return render_template('professor/create_class.html')

# Rota para fazer upload de material didático para uma turma específica
@professor.route('/upload_material/<int:class_id>', methods=['GET', 'POST'])
@login_required
def upload_material(class_id):
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é exclusiva para professores.', category='error')
        return redirect(url_for('main.dashboard'))
    
    class_ = Class.query.get_or_404(class_id)
    
    # Verifica se o professor é o proprietário da turma
    if class_.professor_id != current_user.id:
        flash('Você não tem permissão para adicionar materiais a esta turma.', category='error')
        return redirect(url_for('professor.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files['file']
        
        if title and file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            new_material = Material(
                title=title,
                description=description,
                filename=filename,
                class_id=class_id
            )
            db.session.add(new_material)
            db.session.commit()
            flash('Material enviado com sucesso!', category='success')
            return redirect(url_for('professor.dashboard'))
        else:
            flash('O título e o arquivo são obrigatórios.', category='error')
    
    return render_template('professor/upload_material.html', class_=class_)
