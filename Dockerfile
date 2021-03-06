FROM python:3.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "app.py"]