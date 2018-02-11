FROM python:3
MAINTAINER Maxime Falaize <pro@maxime-falaize.fr>

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]