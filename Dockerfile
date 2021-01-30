FROM python:3.7

# Default uvicorn package doesn't have built-in support for websockets
RUN pip install fastapi uvicorn[standard] jinja2

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
