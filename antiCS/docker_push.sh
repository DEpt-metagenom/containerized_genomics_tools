TOOL=anti_cs
DOCKER_USER=deptmetagenom
VERSION="1.0.0"
DOCKER_IMAGE=${DOCKER_USER}/${TOOL}:${VERSION}
DOCKER_LATEST=${DOCKER_USER}/${TOOL}:latest

# optional to clean up previous docker images:
# sudo docker rm -vf $(sudo docker ps -aq)
# sudo docker rmi -f $(sudo docker images -aq)
# sudo docker system prune -a

docker build -t ${TOOL} .

docker tag ${TOOL} ${DOCKER_IMAGE}
docker tag ${TOOL} ${DOCKER_LATEST}
docker push ${DOCKER_IMAGE}
docker push ${DOCKER_LATEST}
