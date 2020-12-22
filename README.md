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
First make sure to have MongoDb and Minio instances running. They can both be 
bootstrapped by using [docker-compose](https://docs.docker.com/compose/), specifically
by running `docker-compose up` from the project's root directory.
Otherwise, both Minio and MongoDb have to be manually installed and configured to use
the same `environment variables` as present in the `docker-compose.yml` file.  

Also, bear in mind that the following commands apply to UNIX-like systems,
like Linux and MacOS. If using Windows, go ask Billie for help. 

* Open up a terminal
* Navigate to the project's root directory
* Run: `python3 -m venv venv`
* Run: `source venv/bin/activate`
* Run: `pip3 install -r requirements.txt`
* Run: `python3 main.py`
