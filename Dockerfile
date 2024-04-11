FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 5000



ENV FLASK_APP=flaskr

CMD ["flask","run","--host=0.0.0.0"]