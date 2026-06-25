# backend/app.py
import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

from flask import Flask, jsonify
from flask_cors import CORS
from scraper import raspar_dados_painel 

app = Flask(__name__)
CORS(app)

# 🔐 SUAS CREDENCIAIS FIXAS DO CHECKMOB
USUARIO_PADRAO = "Carlos.plenitude"  # Substitua se necessário
SENHA_PADRAO = "Plenitude@2025"       # Coloque sua senha real aqui

@app.route('/api/login-dashboard', methods=['POST', 'GET']) # Aceita GET para facilitar a automação
def login_dashboard():
    try:
        # O robô agora usa as credenciais salvas internamente no servidor
        dados_reais = raspar_dados_painel(USUARIO_PADRAO, SENHA_PADRAO)
        return jsonify({
            "sucesso": True, 
            "dados": dados_reais
        })
    except Exception as e:
        print(f"Erro processado no servidor: {str(e)}")
        return jsonify({
            "sucesso": False, 
            "erro": "Falha na extração automática de dados."
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
