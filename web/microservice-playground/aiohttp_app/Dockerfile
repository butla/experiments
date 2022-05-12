FROM python:3

WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD app.py /app/
EXPOSE 9090

CMD ["python", "app.py"]
