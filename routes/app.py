from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Class, Material, Favorite

# Criação do Blueprint para rotas do aluno
aluno = Blueprint('aluno', __name__)

# Rota para o painel principal do aluno
@aluno.route('/dashboard')
@login_required
def dashboard():
    classes = Class.query.all()  # Busca todas as turmas
    return render_template('aluno/dashboard.html', classes=classes)

# Rota para visualizar materiais de uma turma específica
@aluno.route('/class/<int:class_id>')
@login_required
def view_class(class_id):
    class_ = Class.query.get_or_404(class_id)
    materials = Material.query.filter_by(class_id=class_.id).all()  # Materiais da turma
    return render_template('aluno/view_class.html', class_=class_, materials=materials)

# Rota para favoritar um material
@aluno.route('/favorite_material/<int:material_id>')
@login_required
def favorite_material(material_id):
    material = Material.query.get_or_404(material_id)
    
    # Verifica se o material já foi favoritado
    favorite_exists = Favorite.query.filter_by(user_id=current_user.id, material_id=material.id).first()
    
    if not favorite_exists:
        new_favorite = Favorite(user_id=current_user.id, material_id=material.id)
        db.session.add(new_favorite)
        db.session.commit()
        flash('Material adicionado aos favoritos!', category='success')
    else:
        flash('Você já favoritou este material.', category='info')
    
    return redirect(url_for('aluno.view_class', class_id=material.class_id))

# Rota para visualizar materiais favoritos
@aluno.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    materials = [Material.query.get(favorite.material_id) for favorite in favorites]
    return render_template('aluno/favorites.html', materials=materials)
