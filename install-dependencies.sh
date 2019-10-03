#! /bin/bash

# Install docker
sudo snap install docker

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo docker-compose --version

mkdir inverse-cooking/data 

wget -nc https://dl.fbaipublicfiles.com/inversecooking/ingr_vocab.pkl \
         https://dl.fbaipublicfiles.com/inversecooking/instr_vocab.pkl \
         https://dl.fbaipublicfiles.com/inversecooking/modelbest.ckpt \
         -P inverse-cooking/data
