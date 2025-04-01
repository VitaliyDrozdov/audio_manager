FROM python:3.12.0

ENV HOME=/home/audio_manager \
    APP_HOME=/home/audio_manager/src \
    PYTHONPATH="$PYTHONPATH:/home/audio_manager" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN mkdir -p $APP_HOME \
    && groupadd -r audio_manager\
    && useradd -r -g audio_manager audio_manager


WORKDIR $HOME

COPY src src
ADD alembic.ini .
ADD migrations .
ADD requirements_all.txt .


RUN pip install --upgrade pip \
    && pip install -r ./requirements_all.txt \
    && chown -R audio_manager:audio_manager .


USER audio_manager
