# FlaskIdentityApi
This is an implementation of an identity API in flask. It implements jwt protected routes.

## Environment variables
The LexBox project uses a couple of `environment variables` that have to be added to
a `.env` file in the project's root directory. These are:
* SECRET -> flask secret
* EMAIL -> gmail address used for the emailing service
* PASSWORD -> the password for the above email address
* URL -> url of where the application is running
* MONGO_USER -> the mongodb user 
* MONGO_PASSWORD -> the mongodb password

## Running the app
First make sure to have a MongoDb instance running. This
can be achieved with `docker` by running the following command:
`docker run -it --name mongo -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin -e MONGO_INITDB_DATABASE=lexbox mongo`

* Open up a terminal
* Navigate to the project's root directory
* Run: `src venv/bin/activate`
* Run: `pip3 install -r requirements.txt`
* Run: `python3 main.py`
