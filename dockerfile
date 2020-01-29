FROM python:3.7-slim
EXPOSE 5000
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/credentials.json
WORKDIR /app
COPY . .
COPY cred.json /usr/local/credentials.json
RUN pip install -r requirements.txt
CMD python app.py