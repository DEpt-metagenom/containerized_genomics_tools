TOOL=vizstudio
DOCKER_USER=deptmetagenom
#VERSION="4.5.1"
#DOCKER_IMAGE=${DOCKER_USER}/${TOOL}:${VERSION}
DOCKER_LATEST=${DOCKER_USER}/${TOOL}:latest

# optional to clean up previous docker images:
# sudo docker rm -vf $(sudo docker ps -aq)
# sudo docker rmi -f $(sudo docker images -aq)
# sudo docker system prune -a

sudo docker build -t ${TOOL} .

#sudo docker tag ${TOOL} ${DOCKER_IMAGE}
sudo docker tag ${TOOL} ${DOCKER_LATEST}
#sudo docker push ${DOCKER_IMAGE}
sudo docker push ${DOCKER_LATEST}