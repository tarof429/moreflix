FROM python:3.12.9-alpine3.21

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "moreflix", "run", "--host=0.0.0.0"]