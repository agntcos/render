# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse o backend

def extrair_dados_checkmob(usuario, senha):
    # TODO: Aqui entrará a lógica do Playwright/Selenium para:
    # 1. Ir até https://app.checkmob.com/OrdemServico/PainelDeControle
    # 2. Preencher usuário e senha e clicar em Entrar
    # 3. Ler a tabela que você enviou na foto
    
    # Simulação de dados retornados em tempo real com base na sua imagem:
    dados_simulados = [
        {
            "codigo": "29166",
            "status": "Em execução",
            "titulo": "HUGO D A M - RESERVA SJC11368269",
            "local": "HOSPITAL BENE SÃO JOSÉ",
            "colaborador": "FERNANDA REGINA DE SOUZA",
            "inicio": "25/06/2026 06:00"
        },
        {
            "codigo": "29168",
            "status": "Finalizada",
            "titulo": "CONCEICAO MARIA SANTOS SOUZA",
            "local": "HOSPITAL LEFORTE MORUMBI",
            "colaborador": "LUCAS HENRIQUE BRITO",
            "inicio": "25/06/2026 06:00"
        }
    ]
    return dados_simulados

@app.route('/api/login-dashboard', methods=['POST'])
def login_dashboard():
    data = request.json
    usuario = data.get('usuario')
    senha = data.get('senha')
    
    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400
        
    try:
        # Executa a captura dos dados
        dados = extrair_dados_checkmob(usuario, senha)
        return jsonify({"sucesso": True, "dados": dados})
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
