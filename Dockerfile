# # Usar a imagem oficial do Python como base
# FROM python:3.9-slim

# # Definir o diretório de trabalho dentro do contêiner
# WORKDIR /app


# # Instala dependências do sistema
# RUN apt-get update && apt-get install -y build-essential python3-dev libffi-dev default-libmysqlclient-dev gcc

# # Copiar o arquivo de requisitos e o script para dentro do contêiner
# COPY requirements.txt /app/
# COPY process_data.py /app/
# COPY dados_salvos /app/
# COPY temp_upload /app/

# # COPY arquivos/CHIKO2025.xls /app/
# COPY app.py /app/

# # Instalar as dependências
# RUN pip install --no-cache-dir -r requirements.txt


# EXPOSE 8501

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Usar a imagem oficial do Python como base
# Usar a imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

RUN pip install --upgrade pip
# Instalar dependências do sistema necessárias para o Pillow e outras bibliotecas
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev \
#     libffi-dev \
#     libssl-dev \
#     gcc \
#     libjpeg-dev \
#     zlib1g-dev \
#     libfreetype6-dev \
#     && apt-get clean


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
