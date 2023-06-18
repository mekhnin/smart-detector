FROM r-base:4.2.1
COPY src/controller.R /app/controller.R
RUN apt update && apt install -y libcurl4-openssl-dev libsodium-dev
RUN R -s -e "install.packages(c('plumber','jsonlite','Rssa'))"
EXPOSE $port
CMD R -s -e "plumber::plumb('/app/controller.R')\$run(port=$port)"
