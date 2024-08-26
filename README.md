This repository includes code for a Docker setup with 3 containers:

App: This is the React dev server and runs on http://localhost:3000. The code for this resides in src/app directory.
API: This is the backend container that run a Django instance on http://localhost:8000.
Mongo: This is a DB instance running on port 27017. Django views already have code written to connect to this instance of Mongo.

# Setup
1. Clone this repository
```
git clone https://github.com/adbrew/test.git
```
2. Change into the cloned directory and set the environment variable for the code path. Replace `path_to_repository` appropriately.
```
export ADBREW_CODEBASE_PATH="{path_to_repository}/test/src"
```
3. Build container (you only need to build containers for the first time or if you change image definition, i.e., `Dockerfile`). This step will take a good amount of time.
```
docker-compose build
```
4. Once the build is completed, start the containers:
```
docker-compose up -d
```
5. Once complete, `docker ps` should output something like this:
```
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS                      NAMES
e445be7efa61   adbrew_test_api     "bash -c 'cd /src/re…"   3 minutes ago   Up 2 seconds   0.0.0.0:8000->8000/tcp     api
0fd203f12d8a   adbrew_test_app     "bash -c 'cd /src/ap…"   4 minutes ago   Up 3 minutes   0.0.0.0:3000->3000/tcp     app
884cb9296791   adbrew_test_mongo   "/usr/bin/mongod --b…"   4 minutes ago   Up 3 minutes   0.0.0.0:27017->27017/tcp   mongo
```
6. Check that you are able to access http://localhost:3000 and http://localhost:8000/todos
