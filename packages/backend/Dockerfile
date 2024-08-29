FROM ubuntu:24.10
RUN apt update && apt install -y curl pipx python3-opencv && pipx install --global pdm
RUN mkdir /app
WORKDIR /app
COPY *.toml .
RUN pdm install
COPY backend backend
ENTRYPOINT ["pdm", "run", "start"]
EXPOSE 5000/tcp