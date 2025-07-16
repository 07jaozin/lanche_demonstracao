
FROM python:3.9-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie apenas o arquivo requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/

# Atualize o pip e instale as dependências do arquivo requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copie todo o conteúdo do projeto para o diretório de trabalho no container
COPY . /app/

# Instale o Gunicorn (caso não esteja no requirements.txt)
RUN pip install gunicorn
RUN pip install cloudinary 


# Defina as variáveis de ambiente do Flask
ENV FLASK_APP=projeto/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Exponha a porta 8080 (se você quiser usar esta porta, como é comum em plataformas como o Railway)
EXPOSE 8080

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "projeto.app:app"]