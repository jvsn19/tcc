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
### Environment
``` bash
conda env create -f environment.yml
conda my_crawler activate
```
### Kafka
To run this project, we need to start the zookeper and kafka-server. You can open different terminals to run each command or use the `&` notation to start each server in parallel:
```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties &
$ bin/kafka-server-start.sh config/server.properties &
```
After this you have your kafka server up and running. The basic Kafka usage is to work with topics and messages. A topic is similar to a queue of message that the `KafkaProducer` can add messages and the `KafkaConsumer` can read them. For this project we will create some topics:
- `tcc_wikipedia_urls_topic`: this topic contains all the urls that will be crawled. This way we can work with multiple crawlers. They'll consume a url from this topic asynchronously.
- `tcc_csv_line_topic`: this topic has all the csv lines that we want to add to our "database" (for my TCC I have a csv). This topic will be consumed by a consumer that reads each line and adds to a csv. The table format will be:

  |wikipedia_url_id | wikipedia_url_link | table_url_link | table_url_title | table_url_text | table_url_main_text | table_url_description
  |---|---|---|---|---|---|---|

### Redis
Redis will work as a cache system where I add the urls that I crawled. There is two possible states: "OK" or "ERROR". If I try to crawl a url with "OK" status, the program should avoid and continue. If the status is "ERROR" or `None`, the program should try to crawl again.
``` bash
# To start Redis, you need to initiate the redis-server. You can do it as a paralel process
$ redis-server &
# To test if everything is work properly, run a ping
$ redis-cli ping
PONG
```
