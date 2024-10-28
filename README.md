# site-professores
Breadcrumbssite-professores/
├── app.py                  # Arquivo principal para rodar a aplicação Flask
├── config.py               # Configurações globais, como secret keys e URI do banco de dados
├── requirements.txt        # Dependências do projeto
├── .gitignore              # Arquivos e pastas a serem ignorados pelo Git
├── models/                 # Modelos de dados (SQLAlchemy)
│   └── models.py           # Modelos User, Material, Favorito etc.
├── routes/                 # Rotas da aplicação divididas por funcionalidades
│   ├── auth.py             # Rotas de autenticação (login e registro)
│   ├── professor.py        # Rotas específicas para professores
│   └── aluno.py            # Rotas específicas para alunos
├── static/                 # Arquivos estáticos
│   ├── css/                # Arquivos CSS para estilização
│   │   └── style.css       # Arquivo de estilo principal
│   ├── js/                 # Arquivos JavaScript, se necessário
│   └── uploads/            # Diretório para armazenar uploads de materiais didáticos
├── templates/              # Páginas HTML para as interfaces
│   ├── index.html          # Página inicial
│   ├── login.html          # Página de login
│   ├── register.html       # Página de registro
│   ├── dashboard/          # Painéis específicos de cada usuário
│   │   ├── professor.html  # Painel do professor
│   │   └── aluno.html      # Painel do aluno
│   └── materials/          # Páginas de listagem e visualização de materiais
│       └── material_list.html
└── utils/                  # Funções auxiliares
    └── helpers.py          # Funções para manipulação de favoritos, uploads, etc.
