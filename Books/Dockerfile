FROM python:3.12.7-alpine3.20

RUN apk update && apk add make
RUN adduser -D api
USER api

WORKDIR /home/api

COPY . /home/api

RUN make install

EXPOSE 5000

CMD ["make", "run"]
