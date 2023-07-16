import os
import pyrebase
import requests
from flask import Flask, json, request, jsonify
from flask_cors import CORS
from infra.repository.usuario_pf_repository import Usuario_pfRepository

usuario_pf = Usuario_pfRepository()

app = Flask(__name__)
CORS(app)

firebase_config = {

    "apiKey": "AIzaSyDx0zKscovEoZH00uezzvmOyxaCHGb0w3c",
    "authDomain": "fundem-cda3c.firebaseapp.com",
    "projectId": "fundem-cda3c",
    "storageBucket": "fundem-cda3c.appspot.com",
    "messagingSenderId": "110417913882",
    "appId": "1:110417913882:web:4888c2e37d9241abff09a3",
    "measurementId": "G-3DH423VRH6",
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
        mensagem = {'ID Usuário': login["localId"]}
        return jsonify(mensagem)

    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error in erros_firebase.keys():
            mensagem = {"Erro": erros_firebase[error]}
            return jsonify(mensagem)
        else:
            mensagem = {"Erro": "Usuário não cadastrado"}
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
