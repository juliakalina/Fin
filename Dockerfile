FROM postgres:latest

RUN apt-get update && apt-get install -y python3-pip libpq-dev python3-venv

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install psycopg2
RUN pip3 install Flask Flask-WTF Flask-Bcrypt Flask-SQLAlchemy

WORKDIR /app
COPY ./src /app

CMD ["python3", "main.py"]
