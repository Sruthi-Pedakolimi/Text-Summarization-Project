FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "text_summarization_app.py", "--server.port=8501", "--server.address=0.0.0.0"]