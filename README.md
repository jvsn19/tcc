# tcc
This repository contains a crawler used in my graduation project. The main purpose here is to create a crawler that, given an Wikipedia page, parse all the tables on it and get all the urls inside these tables.

## Requirements
- Redis: used as a cache database to check if an url is already crawled.
- Kafka: used as a queue to store all the needed urls
- Conda (not required): I highly encourage to use Conda as a environment managment. The `environment.yml` contains the conda environment configuration, so you just need to run `conda env create -f environment.yml`
