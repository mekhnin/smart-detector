FROM ubuntu:24.10
RUN apt update && apt install -y pipx curl && pipx install --global pdm
RUN mkdir /app
WORKDIR /app
COPY *.toml .
RUN pdm install
COPY web web
ENTRYPOINT ["pdm", "run", "start"]
EXPOSE 8501/tcp