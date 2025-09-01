FROM python:3.12

WORKDIR /app/auth_service


COPY requirements.txt /app/

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt


COPY . .

COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

CMD ["/app/docker-entrypoint.sh"]