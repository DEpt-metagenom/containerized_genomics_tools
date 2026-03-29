TOOL=mmseqs_for_nextflow
DOCKER_USER=deptmetagenom
VERSION="7.b804f"
DOCKER_IMAGE=${DOCKER_USER}/${TOOL}:${VERSION}
#DOCKER_LATEST=${DOCKER_USER}/${TOOL}:latest

# optional to clean up previous docker images:
# sudo docker rm -vf $(sudo docker ps -aq)
# sudo docker rmi -f $(sudo docker images -aq)
# sudo docker system prune -a

sudo docker build -t ${TOOL} .

sudo docker tag ${TOOL} ${DOCKER_IMAGE}
#sudo docker tag ${TOOL} ${DOCKER_LATEST}
sudo docker push ${DOCKER_IMAGE}
#sudo docker push ${DOCKER_LATEST}