# one-big-thing-backend
Welcome! This goes along with https://github.com/rrnarayan1/one-big-thing-frontend. See that README for an overview of the entire project.

## How to run the server locally
1. Ideally, use `virtualenv` to create a new virtual environment. You'll also need to `pip install` `firebase-admin`, `pandas`, `numpy`, and `flask`
2. Must ask for certificate to access Firebase–running flask without doing so will result in a error. Place certificate in root directory
3. Run `./setup.sh`. This loads the certificate and starts the Flask server.

## API Description
[API Doc](./doc.md)
