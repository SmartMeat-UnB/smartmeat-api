#! /bin/bash
mkdir inverse-cooking/data 

wget -nc https://dl.fbaipublicfiles.com/inversecooking/ingr_vocab.pkl \
         https://dl.fbaipublicfiles.com/inversecooking/instr_vocab.pkl \
         https://dl.fbaipublicfiles.com/inversecooking/modelbest.ckpt \
         -P inverse-cooking/data
