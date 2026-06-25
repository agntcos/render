# backend/app.py
import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔐 CREDENCIAIS FIXAS CONFIGURADAS AUTOMATICAMENTE
USUARIO_PADRAO = "Carlos.plenitude"
SENHA_PADRAO = "Plenitude@2026"  # SUBSTIRTUA PELA SUA SENHA REAL DO CHECKMOB

@app.route('/api/login-dashboard', methods=['GET', 'POST'])
def login_dashboard():
    try:
        # Importação interna para evitar o erro de importação circular do Render
        from scraper import raspar_dados_painel
        
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
