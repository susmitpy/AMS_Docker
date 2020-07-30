FROM python:3.7
ENV PYTHONUNBUFFERED 1
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY /src/. /src/.
WORKDIR /src
