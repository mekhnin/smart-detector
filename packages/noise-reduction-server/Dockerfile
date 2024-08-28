FROM rstudio/plumber
RUN apt update && apt install -y  curl libfftw3-bin libfftw3-dev
RUN R -s -e "install.packages(c('Rssa'))"
COPY R /app
WORKDIR /app
ENTRYPOINT R -s -e "plumber::plumb('controller.R')\$run(host = '0.0.0.0', port = 8085)"
EXPOSE 8085/tcp
