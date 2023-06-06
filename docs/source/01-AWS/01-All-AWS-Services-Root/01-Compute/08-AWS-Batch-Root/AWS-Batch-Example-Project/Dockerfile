# this is public and open source
FROM public.ecr.aws/docker/library/python:3.9-alpine
# set working directory
WORKDIR /usr/src/app
# package application
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./
ENTRYPOINT ["python", "./main.py"]
