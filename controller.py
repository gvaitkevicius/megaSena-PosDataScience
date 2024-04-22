import csv
import numpy as np
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
CORS(app)  # Permitindo todas as origens para rotas iniciadas por /api/
data = None

class FileUploader:
    def __init__(self):
        self.data = None

    @app.route('/api/uploader/', methods=['POST'])
    def uploader():
        global data
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        filename = secure_filename(file.filename)
        file.save(filename)
        
        uploader_instance = FileUploader()
        uploader_instance.carregar(filename) 
        data = uploader_instance.data
        
        os.remove(filename)

        return jsonify({'message': 'File uploaded successfully', 'filename': filename})

    def carregar(self, filename):
        if filename:
            with open(filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                self.data = [row for row in csvreader]

                
@app.route('/api/getContagem/')
def numeros_e_contagens():
    global data
    
    contagens = {}

    if data is None or len(data) <= 1:
        return jsonify({'error': 'Data not uploaded'})
    
    for linha in data[1:]: 
        numeros_sorteados = np.array([int(coluna) for coluna in linha[0].split(';')[2:] if coluna.isdigit()])

        unique, counts = np.unique(numeros_sorteados, return_counts=True)

        for numero, ocorrencias in zip(unique, counts):
            if numero in contagens:
                contagens[numero] += ocorrencias
            else:
                contagens[numero] = ocorrencias

    contagens_lista = [{"_id": int(chave), "ocorrencias": int(valor)} for chave, valor in contagens.items()]
    
    contagens_ordenadas = sorted(contagens_lista, key=lambda x: x["ocorrencias"], reverse=True)

    return jsonify(contagens_ordenadas)


@app.route('/api/sugerirJogo/')
def sugerirJogoCSV():
    global data  
    contagens = {}
    
    if data is None:
        return jsonify({'error': 'Erro ao trazer os dados'})

    for linha in data[1:]: 
        numeros_sorteados = [int(coluna) for coluna in linha[0].split(';')[2:]]

        for numero in numeros_sorteados:
            if numero in contagens:
                contagens[numero] += 1
            else:
                contagens[numero] = 1
                    
    contagens_ordenadas = sorted(contagens.items(), key=lambda x: x[1], reverse=True)

    numeros_mais_frequentes = [numero[0] for numero in contagens_ordenadas[:30]]

    numeros_sorteio = random.sample(numeros_mais_frequentes, 8)

    return jsonify(numeros_sorteio)

##############################################################################################
def verificar_ganhador_mega_csv(*numeros):
    global data  
    ganhadores = []
    
    if data is None:
        return ganhadores
    
    for linha in data[1:]:  
        partes = linha[0].split(';')
        data_sorteio = partes[1]  
        numeros_sorteados = [int(num) for num in partes[2:]]  
        
        if np.isin(numeros, numeros_sorteados).sum() == 6:
            ganhadores.append(data_sorteio)  
    
    return ganhadores

def verificar_quina_mega_csv(*numeros):
    global data  
    ganhadores = []
    
    if data is None:
        return ganhadores
    
    for linha in data[1:]:  
        partes = linha[0].split(';')
        data_sorteio = partes[1]  
        numeros_sorteados = [int(num) for num in partes[2:]]  
        
        if np.isin(numeros, numeros_sorteados).sum() == 5:
            ganhadores.append(data_sorteio)  
    
    return ganhadores

def verificar_quadra_mega_csv(*numeros):
    global data  
    ganhadores = []
    
    if data is None:
        return ganhadores
    
    for linha in data[1:]:  
        partes = linha[0].split(';')
        data_sorteio = partes[1]  
        numeros_sorteados = [int(num) for num in partes[2:]]  
        
        if np.isin(numeros, numeros_sorteados).sum() == 4:
            ganhadores.append(data_sorteio)  
    
    return ganhadores

@app.route('/api/get-ganhador/<nums>')
def getGanhadorCSV(nums):
    numeros = [int(num) for num in nums.split(',')]
    if len(numeros) < 6 or len(numeros) > 9:
        return jsonify({"mensagem": "Total de números deve estar entre 6 e 9."})
    
    datas_concurso_sena = verificar_ganhador_mega_csv(*numeros)
    datas_concurso_quina = verificar_quina_mega_csv(*numeros)
    datas_concurso_quadra = verificar_quadra_mega_csv(*numeros)
    resposta = {}
    if datas_concurso_sena:
        resposta["ganhadores_sena"] = datas_concurso_sena
    if datas_concurso_quina:
        resposta["ganhadores_quina"] = datas_concurso_quina
    if datas_concurso_quadra:
       resposta["ganhadores_quadra"] = datas_concurso_quadra
        
    if not datas_concurso_sena: ##and not datas_concurso_quina and not datas_concurso_quadra:
        resposta["mensagem"] = "Não foi encontrado um ganhador com esses números."
    
    return jsonify(resposta)


if __name__ == '__main__':
    app.run(debug=True)