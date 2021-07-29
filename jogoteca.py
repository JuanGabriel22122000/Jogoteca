from flask import Flask, render_template, request, redirect, session, flash, url_for



app = Flask(__name__)
app.secret_key = 'Açuassuna'

class Jogo:
    def __init__(self,nome,console,categoria) :
        self.nome = nome
        self.console = console
        self.categoria = categoria   

jogo1 = Jogo('Mario','Super nintendo','Aventura')
jogo2 = Jogo('Tetris','GBA','Quebra-cabeça')
jogo3 = Jogo('Pokemon GO','Mobile','RPG')

lista = [jogo1,jogo2,jogo3]

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha  

usuario1 = Usuario('luan', 'Luan Marques', '1234')
usuario2 = Usuario('nico', 'Nico Steppat', '7a1')
usuario3 = Usuario('flavio', 'Flávio', 'javascript')  
    
usuarios = { usuario1.id: usuario1, usuario2.id: usuario2, usuario3.id: usuario3 }


@app.route('/')
def index():

    return render_template('lista.html',titulo = 'JOGOS', jogos = lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Erro, usuário precisa estar logado para visitar está página!!')
        return redirect(url_for('login', proxima=url_for('novo')))
    
    return render_template('novo.html', titulo='Novo jogo')

@app.route('/criar', methods =['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else :
        flash('Não logado,usuário ou senha incorreto!')
        return redirect (url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


# trecho da app
app.run(debug = True)