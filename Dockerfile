# Usa uma imagem oficial do Python super leve e otimizada para produção
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner Linux do Render
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instala as bibliotecas Python sem salvar cache desnecessário (economiza memória)
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código da pasta backend (app.py, etc.) para dentro do contêiner
COPY . .

# Expõe a porta padrão que o Flask vai escutar
EXPOSE 10000

# Comando definitivo que o Gunicorn usa para rodar o servidor Flask em produção
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
