from celery import Celery

app = Celery(
    'medicine_delivery',
    broker='pyamqp://guest@localhost//',  # RabbitMQ URI (change if needed)
    backend='rpc://',  # Result backend (optional, depending on your needs)
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)
