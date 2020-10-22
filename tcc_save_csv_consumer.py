import logging
from argparse import ArgumentParser
from json import loads

from kafka import KafkaConsumer

from utils.file_handler import FileHandler

def setup_parser() -> None:
    parser = ArgumentParser(description='Kafka consumer that reads a topic that follows the \
                                        structure (wikipedia_url_id, wikipedia_url, table_url_link, \
                                        table_url_title, table_url_text, table_url_main_text, \
                                        table_url_description) and adds to the output csv')

    parser.add_argument('--kafka-topic',
                        dest='kafka_topic',
                        help='Kafka Topic that will be consumed',
                        default='tcc_csv_topic')

    return parser

def consume(kafka_topic: str) -> None:
    consumer = KafkaConsumer('quickstart-events',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8')))
# {'url': 'https:', 'id': 10030, 'title': 'Edmund Burke', 'text': None, 'description': None}
    try:
        for event in consumer:
            row = event.value
            id = row.get('id')
            url = row.get('url')
            title = row.get('title')
            text = row.get('text')
            description = row.get('description')
            maintext = row.get('maintext')
            if maintext:
                maintext = maintext.replace('\n', '')
                maintext.replace('\r', '')
            FileHandler.write_tables_csv(
                'table_links',
                'csvs/',
                f'{id}, {url}, {title}, {text}, {description}, {maintext}')

    except KeyboardInterrupt as e:
        stop_consumer(consumer)

def stop_consumer(consumer: KafkaConsumer):
    logging.info('Stopping consumer')

    if consumer is not None:
        consumer.close()

def main():
    parser = setup_parser()
    args = parser.parse_args()
    kafka_topic = args.kafka_topic
    consume(kafka_topic)

if __name__ == '__main__':
    main()
