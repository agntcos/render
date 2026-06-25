# backend/app.py
import os
# Configuração crucial para o Render: diz ao Playwright para usar os navegadores padrão do contêiner Linux
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

from flask import Flask, request, jsonify
from flask_cors import CORS
# Importa a função que realiza o login e a raspagem de dados do arquivo scraper.py
from scraper import raspar_dados_painel 

app = Flask(__name__)

# Permite que o seu arquivo index.html (frontend local) se comunique de forma segura com este servidor na nuvem
CORS(app)

@app.route('/api/login-dashboard', methods=['POST'])
def login_dashboard():
    data = request.json
    usuario = data.get('usuario')
    senha = data.get('senha')
    
    # Validação inicial para garantir que os campos não foram enviados vazios
    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400
        
    try:
        # Executa a automação do Playwright passando as credenciais digitadas no painel
        dados_reais = raspar_dados_painel(usuario, senha)
        
        # Retorna os dados organizados em formato JSON para o Frontend construir os cards
        return jsonify({
            "sucesso": True, 
            "dados": dados_reais
        })
        
    except Exception as e:
        print(f"Erro processado na requisição: {str(e)}")
        return jsonify({
            "sucesso": False, 
            "erro": "Falha na autenticação ou leitura dos dados. Verifique suas credenciais."
        }), 500

if __name__ == '__main__':
    # O Render define a porta automaticamente através da variável de ambiente PORT. Se não encontrar, usa a 10000.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
