FROM python:3.12

EXPOSE 8080
WORKDIR /app

COPY requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
