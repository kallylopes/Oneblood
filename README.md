# OneBlood


### Criar virtualenv

    virtualenv env


### Adicionar virtualenv no .gitingore

    echo 'env' > .gitignore

### Clonar repositório

    git clone https://github.com/kallylopes/Oneblood.git

### Instalar requirements

    pip install -r requirements.txt


### Criar database

    sqlite3 oneblood.db < schema.sql 

### Mudar path do database no arquivo minicurso-flask.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////[SEU PATH]]/Oneblood/personagens.db'

    