FROM python:3.8

# Update apt packages
RUN apt-get update
RUN apt-get upgrade -y

WORKDIR /home/app

COPY . .

RUN chmod +x entrypoint.sh
RUN pip install -r requirements.txt

RUN rm -vrf /var/cache/apk/*
RUN rm -vrf /root/.cache

RUN useradd -s /bin/bash app
RUN chown -R app /home/app

USER app

ENTRYPOINT ["sh", "entrypoint.sh"]