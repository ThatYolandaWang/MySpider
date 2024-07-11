FROM python:3.7
LABEL org.opencontainers.image.source="https://github.com/thatyolandawang/myspider"
WORKDIR /app
ADD . .

RUN pip install -r ./myspider/requirements.txt

CMD [ "python", "./myspider/start.py"]
#ENTRYPOINT ['python3', '/app/myspider/start.py']