# tcc
This repository contains a crawler used in my graduation project. The main purpose here is to create a crawler that, given an Wikipedia page, parse all the tables on it and get all the urls inside these tables.

## Requirements
- Redis: used as a cache database to check if an url is already crawled.
- Kafka: used as a queue to store all the needed urls
- Conda (not required): I highly encourage to use Conda as a environment managment.

## Installation
#### Kafka
https://kafka.apache.org/quickstart

#### Redis
https://redis.io/topics/quickstart

#### Conda
https://docs.conda.io/projects/conda/en/latest/user-guide/install/

## Setup
1. Setup conda environment
    ``` bash
    conda env create -f environment.yml
    conda my_crawler activate
    ```
2. Start Kafka
    ``` bash
    conda env create -f environment.yml
    conda my_crawler activate
    ```
3. Start Redis
    ``` bash
    # To start Redis, you need to initiate the redis-server. You can do it as a paralel process
    $ redis-server &
    # To test if everything is work properly, run a ping
    $ redis-cli ping
    PONG
    ```
