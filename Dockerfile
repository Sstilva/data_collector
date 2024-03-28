FROM python:3.9.19-alpine

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

COPY . /
RUN mkdir /output
ENTRYPOINT [ "python" , "app" ]
