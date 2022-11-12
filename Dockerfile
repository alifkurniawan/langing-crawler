FROM python:3.8.15-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* \

#RUN apk add --no-cache --update \
#    git
#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran musl-dev g++ \
#    libffi-dev openssl-dev \
#    libxml2 libxml2-dev \
#    libxslt libxslt-dev \
#    libjpeg-turbo-dev zlib-dev git

#RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

COPY engine ./engine
COPY output ./output

ENV MONGO_URL=""
ENV MONGO_DB_NAME=langing
ENV ANALYTIC_ID=""
ENV MINUTES=15

CMD ["sh", "-c",  "python -m engine collect ${ANALYTIC_ID} -m ${MINUTES}" ]
