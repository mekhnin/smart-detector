FROM ubuntu:24.10
RUN apt update && apt install -y curl pipx python3-opencv && pipx install --global pdm
RUN mkdir /app
WORKDIR /app
COPY *.toml .
RUN pdm install
COPY ml-server ml-server
ENTRYPOINT ["pdm", "run", "start"]
EXPOSE 8080/tcp
