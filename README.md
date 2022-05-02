~~# Pancakes

## Useful and powerful links:

* [Trello](https://trello.com/b/OrTDRL2A/projekt-przepi%C5%9Bnik)

## Technologies
* Python 3.10.2
* Django 4.0.3
* Docker 20.10.13 

## Prerequisite

1. Python
2. pip
3. Docker
4. Your favorite IDE
5. Optional pgAdmin environment

## First steps

1. clone repository

         git clone https://github.com/PRz-IO/p01gr02-przepisy-zespol-gr02.git

2. Start containers

         docker-compose up -d

3. When it is done, you have to press Ctrl+C to cancel process, after that you will have to make migrations

         docker-compose run web python manage.py makemigrations

4.  Apply migration:

         docker-compose run web python manage.py migrate

## Run

1. Change path to project path:
      
       cd .\..\..\pancakes\

2. Start db container:
   
         docker-compose up db 
3. Start web container:

         docker-compose up web

4. App is listening on address "http://localhost:8000/"

## Migration
When you change structure of models(adding a field, deleting a model, etc.). You have to to make migration.

1. Make migration:

        docker-compose run web python manage.py makemigrations

2. Apply migration:

        docker-compose run web python manage.py migrate

## TODO

* split unit and integration tests~~
