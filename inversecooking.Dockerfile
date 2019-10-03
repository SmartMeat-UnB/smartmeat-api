FROM python:3.6
WORKDIR /inversecooking

COPY inverse-cooking/ml-requirements.txt /inversecooking
RUN pip install -r ml-requirements.txt
COPY inverse-cooking /inversecooking

RUN mkdir -p data

# Working with datasets path
# RUN mkdir datasets \ 
#           datasets/images datasets/images/train \ 
#           datasets/images/test datasets/images/val

# RUN wget "http://data.csail.mit.edu/im2recipe/det_ingrs.json" \ 
#          "http://data.csail.mit.edu/im2recipe/recipe1M_layers.tar.gz" \
#          -P datasets/

RUN wget -nc https://dl.fbaipublicfiles.com/inversecooking/ingr_vocab.pkl \
             https://dl.fbaipublicfiles.com/inversecooking/instr_vocab.pkl \
             https://dl.fbaipublicfiles.com/inversecooking/modelbest.ckpt \
             -P data/

VOLUME data

CMD ["python", "src/inversecooking-api.py"]