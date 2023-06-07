FROM python:3.6.8-slim
RUN pip install flask
COPY app.py /var/app/
ENTRYPOINT ["python", "/var/app/app.py"]
