# StepByStep

```
python manage.py runserver
celery -A StepByStep worker -B -l info --concurrency=4
```

## login

`https://github.com/login/oauth/authorize?client_id=1db4aae055b7d417f366&redirect_uri=http://localhost:8000/login`
