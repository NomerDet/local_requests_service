FROM python:3.10

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /root/.local/share/mkcert
RUN apt-get update && apt-get install wget libnss3-tools -y
#RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-arm64
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
#RUN mv mkcert-v1.4.4-linux-arm64 /usr/bin/mkcert
RUN mv mkcert-v1.4.4-linux-amd64 /usr/bin/mkcert
RUN chmod +x /usr/bin/mkcert
RUN mkcert -install && mkcert backend localhost 192.168.0.161 213.87.9.163 212.233.88.43

WORKDIR /app

COPY local_requests_service .

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile






#CMD ["python3", "-m", "pipenv", "run", "uvicorn", "main:app"]
