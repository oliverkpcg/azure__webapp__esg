docker build -t flask-app . 
az acr login --name prototypescontainers
docker tag flask-app prototypescontainers.azurecr.io/flask-app:v1
docker push prototypescontainers.azurecr.io/flask-app:v1