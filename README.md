<h2 align="center">useful-course-back</h2>

## Старт

##### 1) Клонировать репозиторий

##### 2) Запустить контейнер

    docker-compose up --build

#### 3) Демо
    python manage.py loaddata dumpdata.json
    

### PR

    > docker-compose -f docker-compose.prod.yml up -d
    > docker exec -it useful-course-back_back_1 bash
    перезапуск nginx:
    > sudo systemctl reload nginx

    > docker-compose -f docker-compose.collab.yml up -d




