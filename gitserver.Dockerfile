FROM alpine:latest

RUN apk update && apk add git

RUN adduser -D git
USER git
WORKDIR /home/git

RUN mkdir -p /home/git/repos/repository.git && cd /home/git/repos/repository.git && git init --bare

CMD ["sh", "-c", "while :; do sleep 10; done"]
