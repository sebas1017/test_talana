#Desarrollo de prueba

ejecutar tests:

docker-compose run --rm test

al ejecutar el comando se ejecutaran los tests que fallaban y terminaran  correctamente

en este proyecto lleve a cabo ajustes en los archivos:
             
             /adventure/tests
             /adventure/views.py
             /adventure/usecases.py
             /adventure/models.py
             /adventure/serializers.py
             /adventure/urls.py
             /docker-compose.yml



## Requirements

- docker
- docker-compose

## Start the project
 si se desea ejecutar el proyecto utilizar el comando
`docker-compose up`

y en los logs se evidencia que tambien los tests se ejecutan correctamente

### Swagger

http://localhost:8000/api/schema/swagger-ui/


### Mailhog

http://localhost:1025
