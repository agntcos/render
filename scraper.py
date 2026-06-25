# backend/scraper.py
from playwright.sync_api import sync_playwright
import time

def raspar_dados_painel(usuario, senha):
    dados_extraidos = []
    
    # URL do painel alvo (substitua ou parametrize conforme necessário)
    URL_LOGIN = "https://app.checkmob.com/login" 
    URL_PAINEL = "https://app.checkmob.com/OrdemServico/PainelDeControle"

    with sync_playwright() as p:
        # Lança o navegador em segundo plano (mude para headless=False se quiser ver acontecendo)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 1. Acessa a página de autenticação
            page.goto(URL_LOGIN)
            
            # 2. Preenche as credenciais (Substitua os seletores '#usuario' e '#senha' pelos IDs reais do site)
            page.fill("input[type='email']", usuario)  # ou o seletor correto do campo de login
            page.fill("input[type='password']", senha)
            
            # 3. Clica no botão de entrar (Substitua pelo seletor correto do botão)
            page.click("button[type='submit']")
            
            # Aguarda a navegação pós-login concluir
            page.wait_for_load_state("networkidle")
            
            # 4. Garante que está na página do painel de controle
            if page.url != URL_PAINEL:
                page.goto(URL_PAINEL)
                page.wait_for_load_state("networkidle")
            
            # 5. Aguarda a tabela de Ordens de Serviço carregar na tela
            # Substitua '.minha-tabela-classes' pelo seletor real da tabela visível na imagem
            seletor_tabela = "table" 
            page.wait_for_selector(seletor_tabela, timeout=15000)
            
            # 6. Mapeia as linhas da tabela (capturando elementos da estrutura identificada na sua imagem)
            linhas = page.query_selector_all(f"{seletor_tabela} tbody tr")
            
            for linha in linhas:
                colunas = linha.query_selector_all("td")
                if len(colunas) >= 8:  # Garante que a linha possui as colunas necessárias
                    dados_extraidos.append({
                        "codigo": colunas[1].inner_text().strip(),       # Segunda coluna (Código)
                        "status": colunas[2].inner_text().strip(),       # Terceira coluna (Status)
                        "titulo": colunas[3].inner_text().strip(),       # Quarta coluna (Título)
                        "local": colunas[4].inner_text().strip(),        # Quinta coluna (Hospital/Clínica)
                        "colaborador": colunas[5].inner_text().strip(),  # Sexta coluna (Usuários)
                        "inicio": colunas[7].inner_text().strip()        # Oitava coluna (Previsão de Início)
                    })
                    
        except Exception as e:
            print(f"Erro durante a automação/raspagem: {e}")
            raise e
        finally:
            browser.close()
            
    return dados_extraidos
