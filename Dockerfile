FROM ubuntu:latest
LABEL authors="Maks"

ENTRYPOINT ["top", "-b"]