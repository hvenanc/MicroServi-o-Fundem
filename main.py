import os
import pyrebase
import requests
from flask import Flask, json, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from infra.repository.usuario_pf_repository import Usuario_pfRepository

usuario_pf = Usuario_pfRepository()
load_dotenv()

app = Flask(__name__)
CORS(app)

firebase_config = {

    "apiKey": str(os.getenv('API_KEY_FIREBASE')),
    "authDomain": "login---python.firebaseapp.com",
    "projectId": "login---python",
    "storageBucket": "login---python.appspot.com",
    "messagingSenderId": "934624818868",
    "appId": "1:934624818868:web:0236f9fadc8d47e83ac9e1",
    "measurementId": "G-SNN6WKXKN3",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

erros_firebase = {
    "EMAIL_EXISTS": "E-mail já cadastrado!",
    "WEAK_PASSWORD : Password should be at least 6 characters": "A senha deve possuir mais de 6 Caracteres!",
    "INVALID_EMAIL": "E-mail Inválido!",
    "INVALID_PASSWORD": "E-mail ou Senha Inválidos"
}


@app.route('/login', methods=['POST'])
def logar():
    try:
        dados = json.loads(request.data)
        login = auth.sign_in_with_email_and_password(dados["Email"], dados["Senha"])
        return f'ID Usuário: {login["localId"]}'

    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error in erros_firebase.keys():
            mensagem = {"Erro": erros_firebase[error]}
            return jsonify(mensagem)


@app.route('/signin', methods=['POST'])
def criar():
    try:
        dados = json.loads(request.data)
        usuario = auth.create_user_with_email_and_password(dados["Email"], dados["Senha"])
        auth.send_email_verification(usuario['idToken'])
        usuario_pf.insert(usuario['localId'], dados['Nome'], dados['Data'], dados['Email'], dados['Telefone'])
        mensagem = f'Foi enviado um e-mail de verificação para: {dados["Email"]}'
        return jsonify({"Sucesso": mensagem})

    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error in erros_firebase.keys():
            mensagem = {"Erro": erros_firebase[error]}
            return jsonify(mensagem)


if __name__ == "__main__":
    app.run(debug=True)
