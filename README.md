# FlaskIdentityApi
This is an implementation of an identity API in flask. It implements jwt protected routes.

## Environment variables
The LexBox project uses a couple of `environment variables` that have to be added to
a `.env` file in the project's root directory. These are:
* SECRET -> flask secret
* EMAIL -> gmail address used for the emailing service
* PASSWORD -> the password for the above email address
