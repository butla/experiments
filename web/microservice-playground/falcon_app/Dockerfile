FROM python:3.4
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 9090 
CMD ["uwsgi", "--http-socket", ":9090", "--module", "falcon_app.app:app", "--disable-logging"]

