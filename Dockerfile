
FROM docker.io/python:3.8-slim-bullseye

RUN groupadd -r Tong && useradd -r -g Tong Tong
# RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev
RUN pip install Flask==3.0.0 akshare==1.11.1 backtrader==1.9.78.123 apscheduler==3.10.4  
WORKDIR /app
# COPY app /app
COPY cmd.sh /
EXPOSE 9090 9191 
