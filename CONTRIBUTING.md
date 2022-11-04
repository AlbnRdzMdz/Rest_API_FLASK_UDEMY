#Contributing

## How to run the Dockerfile locally


docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run"




En mi caso:
docker build -t rest-api-flask-python .      

docker run -dp 5000:5000 -w /app -v "/c/Users/lumen/Documents/ActualizacionProfesional/FlaskRestAPI/1_FirstRESTAPI:/app" rest-api-flask-python


