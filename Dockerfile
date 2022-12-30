FROM python:3.10

COPY ./requirements.txt /crud_container/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /crud_container/requirements.txt

COPY . /crud_container

EXPOSE 8000

WORKDIR /crud_container

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
