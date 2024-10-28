from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from app import db
from models import User

# Criação do Blueprint para autenticação
auth = Blueprint('auth', __name__)

# Rota para a página de login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Busca o usuário pelo e-mail
        user = User.query.filter_by(email=email).first()
        
        # Verifica a senha e se o usuário existe
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login bem-sucedido!', category='success')
            return redirect(url_for('main.dashboard'))  # Redireciona para o dashboard
        else:
            flash('Email ou senha incorretos, tente novamente.', category='error')
    
    return render_template('login.html')

# Rota para a página de registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # 'professor' ou 'aluno'
        
        # Verifica se o usuário já existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Este e-mail já está registrado.', category='error')
        elif len(username) < 2:
            flash('O nome de usuário deve ter pelo menos 2 caracteres.', category='error')
        elif len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', category='error')
        else:
            # Cria um novo usuário
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='sha256'),
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada com sucesso!', category='success')
            login_user(new_user)
            return redirect(url_for('main.dashboard'))
    
    return render_template('register.html')

# Rota para logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', category='success')
    return redirect(url_for('auth.login'))
