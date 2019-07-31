# liando

# django 启动

python wisdom_brain_manage.py runserver --insecure


# celery 启动

- linux    
    celery -A wisdom_brain.taskapp worker -l info
- windows 
    celery -A wisdom_brain.taskapp worker -l info -P eventlet   
