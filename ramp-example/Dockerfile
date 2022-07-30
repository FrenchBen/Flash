FROM python:3
RUN apt-get update && apt-get install -y gnuplot && apt-get clean autoclean
WORKDIR /app
COPY . /app/
RUN chmod +x /app/hammer.sh
CMD ["/app/hammer.sh"]