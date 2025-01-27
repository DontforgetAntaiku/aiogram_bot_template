FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    lsb-release \
    curl \
    gnupg
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
