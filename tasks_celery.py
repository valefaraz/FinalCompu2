# Celery service example: task to multiply two numbers

from celery import Celery

app = Celery('tasks', broker='redis://localhost', backend='redis://localhost:6379')

@app.task
def multiply(a, b):
    return a * b


if __name__ == "__main__":
    app.start()

