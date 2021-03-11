# Commands to run for app to work

docker pull rabbitmq:3-management-alpine 
docker run -d -t -p 5672:5672 -p 15672:15672 rabbitmq:3-management-alpine
celery -A task_list worker -l info
celery -A task_list beat -l info
python manage.py migrate
python manage.py runserver
