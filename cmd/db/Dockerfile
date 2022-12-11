FROM python:3.9
RUN pip install --upgrade pip && \
    pip install poetry==1.0 && \
    poetry config virtualenvs.create false

COPY pyproject.toml ./

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["python","-m","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]