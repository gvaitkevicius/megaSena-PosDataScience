from flask import Flask, request, jsonify,render_template
from pymongo import MongoClient
from flask_cors import CORS
#Werkzeug import secure_filename
import random


app = Flask(__name__)
CORS(app)

def verificar_ganhador_mega(*numeros):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['megasena']  
    collection = db['mega']
    
    consulta = {
        "$and": [
            {"n1": {"$in": numeros}},
            {"n2": {"$in": numeros}},
            {"n3": {"$in": numeros}},
            {"n4": {"$in": numeros}},
            {"n5": {"$in": numeros}},
            {"n6": {"$in": numeros}},
            {"$expr": {"$eq": [{"$size": {"$setIntersection": [numeros, ["$n1", "$n2", "$n3", "$n4", "$n5", "$n6"]]}}, 6]}}
        ]
    }
    
    resultados = collection.find(consulta)
    
    datas = [resultado['data'] for resultado in resultados]
    client.close()
    
    return datas

def verificar_quina_mega(*numeros):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['megasena']  
    collection = db['mega']
    
    consulta = {
        "$and": [
            {"$or": [
                {"n1": {"$in": numeros}},
                {"n2": {"$in": numeros}},
                {"n3": {"$in": numeros}},
                {"n4": {"$in": numeros}},
                {"n5": {"$in": numeros}},
                {"n6": {"$in": numeros}},
            ]},
            {"$expr": {"$eq": [{"$size": {"$setIntersection": [numeros, ["$n1", "$n2", "$n3", "$n4", "$n5", "$n6"]]}}, 5]}}
        ]
    }
    
    resultados = collection.find(consulta)
    
    datas = [resultado['data'] for resultado in resultados]
    client.close()
    
    return datas

def verificar_quadra_mega(*numeros):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['megasena']  
    collection = db['mega']
    
    consulta = {
        "$and": [
            {"$or": [
                {"n1": {"$in": numeros}},
                {"n2": {"$in": numeros}},
                {"n3": {"$in": numeros}},
                {"n4": {"$in": numeros}},
                {"n5": {"$in": numeros}},
                {"n6": {"$in": numeros}},
            ]},
            {"$expr": {"$eq": [{"$size": {"$setIntersection": [numeros, ["$n1", "$n2", "$n3", "$n4", "$n5", "$n6"]]}}, 4]}}
        ]
    }
    
    resultados = collection.find(consulta)
    
    datas = [resultado['data'] for resultado in resultados]
    client.close()
    
    return datas

@app.route('/apis/get-ganhador/<nums>')
def getGanhador(nums):
    numeros = [int(num) for num in nums.split(',')]
    if len(numeros) < 6 or len(numeros) > 9:
        return jsonify({"mensagem": "Total de números deve estar entre 6 e 9."})
    
    datas_concurso_sena = verificar_ganhador_mega(*numeros)
    datas_concurso_quina = verificar_quina_mega(*numeros)
    datas_concurso_quadra = verificar_quadra_mega(*numeros)
    
    resposta = {}
    if datas_concurso_sena:
        resposta["ganhadores_sena"] = datas_concurso_sena
    if datas_concurso_quina:
        resposta["ganhadores_quina"] = datas_concurso_quina
    if datas_concurso_quadra:
        resposta["ganhadores_quadra"] = datas_concurso_quadra
        
    if not datas_concurso_sena and not datas_concurso_quina and not datas_concurso_quadra:
        resposta["mensagem"] = "Não foi encontrado um ganhador com esses números."
    
    return jsonify(resposta)

@app.route('/apis/getOcorrencias/')
def listar_numeros_mais_sorteados():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['megasena']
    collection = db['mega']

    pipeline = [
        {"$project": {"numeros": ["$n1", "$n2", "$n3", "$n4", "$n5", "$n6"]}},
        {"$unwind": "$numeros"},
        {"$group": {"_id": "$numeros", "ocorrencias": {"$sum": 1}}},
        {"$sort": {"ocorrencias": -1}},
        {"$limit": 60} 
    ]
    
    numeros_mais_sorteados = list(collection.aggregate(pipeline))
    client.close()
    
    return jsonify(numeros_mais_sorteados)

@app.route('/apis/sugerirJogo/')
def sugerirJogo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['megasena']
    collection = db['mega']
    
    pipeline = [
        {"$project": {"numeros": ["$n1", "$n2", "$n3", "$n4", "$n5", "$n6"]}},
        {"$unwind": "$numeros"},
        {"$group": {"_id": "$numeros", "ocorrencias": {"$sum": 1}}},
        {"$sort": {"ocorrencias": -1}},
        {"$limit": 30}  # Limitando aos 30 números mais frequentes
    ]
    
    numeros_mais_frequentes = list(collection.aggregate(pipeline))
    client.close()
    
    numeros = [numero['_id'] for numero in numeros_mais_frequentes]
    numeros_sorteio = random.sample(numeros, 8)
    
    return jsonify(numeros_sorteio)

#@app.route('/')
#def index():
 #   return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
