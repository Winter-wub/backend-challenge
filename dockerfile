FROM python:3.7-slim
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/credentials.json
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD python app.py