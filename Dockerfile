FROM python:3.10.4

WORKDIR /app

COPY src /app/src
COPY Makefile requirements.txt requirements-tests.txt setup.cfg .env.test /app/

RUN make venv

EXPOSE 8000

CMD ["make", "run/local"]