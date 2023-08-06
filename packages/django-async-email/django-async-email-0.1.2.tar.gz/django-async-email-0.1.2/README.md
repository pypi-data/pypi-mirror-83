# TODO

* Enviar todas as mensagens que levantem TemplateDoesNotExist para uma fila apropriada

# django-async-email

[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/tox/badge.svg)](https://github.com/eltonplima/django-async-email/actions)
[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/flake8/badge.svg)](https://github.com/eltonplima/django-async-email/actions)

```python
EMAILS_TEMPLATES = {
    "welcome": {
        "subject": "welcome/subject.txt",
        "body_html": "welcome/body.html",
        "body_txt": "welcome/body.txt",
    }
}

# Customize the max_retries for one specific email category task
ASYNC_EMAIL_TASKS = {"async_email.tasks.welcome": {"max_retries": 20}}

# Customize the max_retries for all the tasks
# Default is 20
ASYNC_EMAIL_TASKS_MAX_RETRIES = 10
ASYNC_EMAIL_TASKS_MAX_RETRIES = 10
```

# Important notes

python setup.py sdist bdist_wheel && pip uninstall -y django_async_email && python -m pip install dist/django_async_email-0.1.0-py2.py3-none-any.whl

## Demo project

```shell script
cd demo_project
# Build and run the docker image
docker-compose build && docker-compose up -d demo_project
# Run migrations
docker-compose exec demo_project python manage.py migrate
# Create the superuser
docker-compose exec demo_project python manage.py createsuperuser
```

```shell script
celery worker --app=demo_project.celery -l info --pool=eventlet
```
