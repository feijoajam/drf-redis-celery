# Django Rest Framework project with celery tasks and cache

Steps to run the project: 

1. Clone repo `git clone https://github.com/feijoajam/drf-redis-celery`
2. `cd drf-redis-celery`
3. `docker-compose build`
4. `docker-compose up`
5. Find out id of a container named web-app using `docker ps -a`. Let it be your_container_id
6. `docker exec -t -i your_container_id sh -c "python manage.py makemigrations"`
7. `docker exec -t -i your_container_id sh -c "python manage.py migrate"`
8. At `http://localhost:8000/api/subscriptions/?format=json` you can see list of all subscriptions in json format. <br /><br />
To add new subscriptions, services, etc:
9. `docker exec -t -i your_container_id sh -c "python manage.py createsuperuser"`
10. Log in with this user in `http://localhost:8000/admin/` and add data you want
