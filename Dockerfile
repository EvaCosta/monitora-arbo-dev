# Usar a imagem oficial do Python como base
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instalar dependências do sistema básicas, se necessário
RUN apt-get update && apt-get install -y \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de requisitos para dentro do contêiner
COPY requirements.txt /app/

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte do projeto
COPY . /app/

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
