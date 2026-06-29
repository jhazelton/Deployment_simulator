FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip

WORKDIR /app

COPY . .

CMD ["python3", "jim_dply3.py"]
