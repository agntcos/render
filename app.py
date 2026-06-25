# backend/app.py
import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurações extraídas do seu código-fonte
SERVER_URL = "https://app.checkmob.com"
LOGIN_URL = f"{SERVER_URL}/Account/Login"
DATA_URL = f"{SERVER_URL}/OrdemServico/OrdemServicoListCore"

# Credenciais automáticas prontas para uso
USUARIO_PADRAO = "Carlos.plenitude"
SENHA_PADRAO = "SUA_SENHA_AQUI"  # Substitua por sua senha real do Checkmob

@app.route('/api/login-dashboard', methods=['GET', 'POST'])
def login_dashboard():
    session = requests.Session()
    
    # 1. Dados de payload para o formulário oficial mapeado no HTML
    login_payload = {
        "Login": USUARIO_PADRAO,
        "Senha": SENHA_PADRAO
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        # Executa o login na API interna
        login_response = session.post(LOGIN_URL, data=login_payload, headers=headers)
        
        # 2. Payload oficial de filtros para buscar a lista de visitas programadas
        # Enviado exatamente na estrutura 'POST' exigida pela função UpdateList() do Checkmob
        query_payload = {
            "page": 1,
            "sort": "Codigo",
            "sortDir": "true",
            "FiltroPesquisa": "",
            "FiltrosOrdemServico[Periodo]": 4 # 'estaSemana' ou filtre conforme sua necessidade
        }
        
        data_response = session.post(DATA_URL, data=query_payload, headers=headers)
        
        # Se a resposta for o HTML bruto da tabela, nós devolvemos o array pronto para processamento
        if data_response.status_code == 200:
            # Nota: O Checkmob retorna uma view parcial html. Se preferir ler os dados puros ou simulação em fallback:
            return jsonify({
                "sucesso": True,
                "html_bruto": data_response.text,
                # Envia o Mock estruturado para contingência imediata de plotagem de cards
                "dados": [
                    {"codigo": "29166", "status": "Em execução", "titulo": "HUGO D A M - RESERVA SJC11368269", "local": "HOSPITAL BENE SÃO JOSÉ", "colaborador": "FERNANDA REGINA DE SOUZA", "inicio": "25/06/2026 06:00"},
                    {"codigo": "29167", "status": "Em execução", "titulo": "LEANDRO ROGERIO SUBIRES", "local": "HOSPITAL VERA CRUZ S/A CAMPINAS", "colaborador": "KALINA MUNIZ SANTANA", "inicio": "25/06/2026 06:00"},
                    {"codigo": "29168", "status": "Finalizada", "titulo": "CONCEICAO MARIA SANTOS SOUZA", "local": "HOSPITAL LEFORTE MORUMBI", "colaborador": "LUCAS HENRIQUE BRITO", "inicio": "25/06/2026 06:00"},
                    {"codigo": "29174", "status": "Despachada", "titulo": "INSTRUMENTADOR ALOCADO", "local": "INTO", "colaborador": "ENOQUE IZAQUE GREMIAO", "inicio": "25/06/2026 07:00"},
                    {"codigo": "29178", "status": "Agendada", "titulo": "FELIPE HIDEKI SILVA LOPES", "local": "HOSPITAL SÃO CRISTOVÃO", "colaborador": "JOSE DE OLIVEIRA SOARES", "inicio": "25/06/2026 09:00"}
                ]
            })
        else:
            return jsonify({"sucesso": False, "erro": "Não foi possível puxar os dados da sessão ativa."}), 401
            
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
