from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Inicialização do Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Inicialização do login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo do banco de dados
class User(UserMixin):
    def __init__(self, id, username, email, is_teacher):
        self.id = id
        self.username = username
        self.email = email
        self.is_teacher = is_teacher

@login_manager.user_loader
def load_user(user_id):
    user_data = supabase.table('usuarios').select('*').eq('id', user_id).execute()
    if user_data.data:
        user_info = user_data.data[0]
        return User(user_info['id'], user_info['username'], user_info['email'], user_info['is_teacher'])
    return None

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = supabase.table('usuarios').select('*').eq('email', email).execute()

        if user_data.data and check_password_hash(user_data.data[0]['password'], password):
            user = User(user_data.data[0]['id'], user_data.data[0]['username'], user_data.data[0]['email'], user_data.data[0]['is_teacher'])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            session['message'] = 'Login ou senha incorretos'
            return redirect(url_for('login'))
    return render_template('login.html', message=session.pop('message', None))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')
        is_teacher = request.form.get('is_teacher') == 'on'

        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'is_teacher': is_teacher
        }

        supabase.table('usuarios').insert(new_user).execute()
        session['message'] = 'Cadastro realizado com sucesso! Faça login para continuar.'
        return redirect(url_for('login'))
    return render_template('register.html', message=session.pop('message', None))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota do painel de usuário
@app.route('/dashboard')
@login_required
def dashboard():
    materials_data = supabase.table('materiais_didaticos').select('*').eq('user_id', current_user.id).execute()
    
    if current_user.is_teacher:
        materials = materials_data.data
        return render_template('dashboard/professor.html', materials=materials)
    else:
        all_materials = supabase.table('materiais_didaticos').select('*').execute()
        return render_template('dashboard/aluno.html', materials=all_materials.data)

# Rota para upload de materiais (somente para professores)
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_material():
    if not current_user.is_teacher:
        session['message'] = 'Acesso negado. Somente professores podem fazer upload de materiais.'
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_material = {
                'title': title,
                'description': description,
                'filename': filename,
                'user_id': current_user.id
            }
            supabase.table('materiais_didaticos').insert(new_material).execute()
            session['message'] = 'Material enviado com sucesso!'
            return redirect(url_for('dashboard'))
    return render_template('upload.html', message=session.pop('message', None))

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
