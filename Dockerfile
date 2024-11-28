FROM python:3.8
#WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Kolkata


RUN apt-get update && apt-get install -y \
    build-essential \
    vim \
    git \
    bash


RUN pip install --upgrade pip
#    \
#	&& pip3 install pymongo \
#	&& pip3 install pytz \
#	&& pip3 install redis-py-cluster
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /logs
WORKDIR /cache-redis-entities-to-id-article-batch
COPY . /cache-redis-entities-to-id-article-batch

EXPOSE 8080
# Command to run the application
# CMD ["gunicorn", "src.api:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9030", "--timeout", "120"]

# exectute start up script
# CMD ["sh", "api.sh"]
CMD [ "sh", "entrypoint.sh" ]
# CMD ["/bin/sh", "-c", "while true; do echo 'Infinite loop'; sleep 1; done"]
