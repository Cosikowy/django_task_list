# Commands to run for app to work

docker pull rabbitmq:3-management-alpine\
docker run -d -t -p 5672:5672 -p 15672:15672 rabbitmq:3-management-alpine\
celery -A task_list worker -l info\
celery -A task_list beat -l info\
python manage.py migrate\
python manage.py runserver\


niestety znalazło się kilka bugów,
aby edytować profil należy dodać po id /edit (np. profile/1/edit)
podobna sytuacja jest z usunięciem, nie wiem czemu sesja się na chwilę gubi przy przeglądaniu profilu innego użytkownika (profile/1/delete)
