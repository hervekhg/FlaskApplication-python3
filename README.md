#Using Docker to Build Flask Application with MySql Database 8-)

## Dockerfile
The Dockerfile build a custom image with all module which are needed for the project.
The image a based on latest version of Ubuntu:18.04

```
docker build -t hervekhg/237story:latest .
docker images
```

## Docker-compose 
The docker-compose build a container with our custom image and connect it to mysql database

```
docker-compose build #Build
docker-compose up # Launch
docker-compose ps # Check
```


