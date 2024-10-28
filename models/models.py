from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app import db

# Modelo de usuário, utilizado para autenticação de professores e alunos
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'professor' ou 'aluno'
    
    # Relacionamentos
    classes = relationship('Class', back_populates='professor', lazy=True)
    favorites = relationship('Favorite', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

# Modelo de turma, utilizado para associar materiais aos professores
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamentos
    professor = relationship('User', back_populates='classes')
    materials = relationship('Material', back_populates='class_', lazy=True)

    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.name}')>"

# Modelo de material didático, para upload de arquivos
class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    
    # Relacionamentos
    class_ = relationship('Class', back_populates='materials')

    def __repr__(self):
        return f"<Material(id={self.id}, title='{self.title}', class_id={self.class_id})>"

# Modelo de favoritos, para que alunos marquem materiais como favoritos
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    
    # Relacionamentos
    user = relationship('User', back_populates='favorites')
    material = relationship('Material')

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, material_id={self.material_id})>"
