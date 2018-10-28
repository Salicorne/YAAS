FROM python:3.6 
ENV PYTHONUNBUFFERED 1 
COPY ./requirements.txt /requirements.txt 
COPY . /code
RUN pip install gunicorn
RUN pip install -r requirements.txt
WORKDIR /code
RUN cd /code
RUN touch db.sqlite3 && rm db.sqlite3
RUN python manage.py migrate
CMD ["gunicorn", "yaas.wsgi", "--bind", "0.0.0.0:8000"]
EXPOSE 8000
