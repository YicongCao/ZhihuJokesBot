FROM python:3.6-alpine

ENV APP_HOME=/app \
    APP_PYTHON_PACKAGES=/usr/local/lib/python3.6/dist-packages \
    PYTHONIOENCODING=utf-8

WORKDIR ${APP_HOME}

COPY . ${APP_HOME}

RUN pip install -r requirements.txt

RUN ["chmod", "+x", "./dockermain.sh"]

EXPOSE 5000

ENTRYPOINT [ "sh", "./dockermain.sh" ]