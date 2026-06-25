# backend/app.py
import os
# Impede o Playwright de buscar executáveis locais inválidos dentro do Linux do Render
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import raspar_dados_painel 

app = Flask(__name__)
CORS(app)

@app.route('/api/login-dashboard', methods=['POST'])
def login_dashboard():
    data = request.json
    usuario = data.get('usuario')
    senha = data.get('senha')
    
    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400
        
    try:
        dados_reais = raspar_dados_painel(usuario, senha)
        return jsonify({
            "sucesso": True, 
            "dados": dados_reais
        })
    except Exception as e:
        print(f"Erro processado no servidor: {str(e)}")
        return jsonify({
            "sucesso": False, 
            "erro": "Falha na extração de dados do Checkmob."
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
