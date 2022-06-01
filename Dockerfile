FROM python:3.8-bullseye

RUN mkdir -p /opt/app \
    && mkdir -p /opt/app/coinr

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

COPY requirements.txt start-server.sh ./

RUN pip install -r requirements.txt

COPY coinr ./coinr/

RUN python coinr/manage.py collectstatic --no-input

RUN addgroup --gid 1000 --system coinr \
    && adduser --uid 1000 --system --group coinr \
    && chown -R coinr:coinr /opt/app

USER coinr

EXPOSE $PORT
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
