from kafka import KafkaAdminClient
from argparse import ArgumentParser

kafka_admin = KafkaAdminClient()

def main() -> None:
    parser = ArgumentParser(description='Kafka consumer that reads a topic that follows the \
                                        structure (wikipedia_url_id, wikipedia_url, table_url_link, \
                                        table_url_title, table_url_text, table_url_main_text, \
                                        table_url_description) and adds to the output csv')
    parser.add_argument('--action',
                        dest='action',
                        help='Action that KafkaAdmin will run.\nCurrent \
                             actions: \n  - Create\n  - Delete')
    parser.add_argument('--topics',
                        dest = 'topics',
                        nargs='+',
                        help = 'Topics to complement the action. \
                                For example, if you want to create \
                                a new Kafka topic, you should pass the \
                                topic name.')
    args = parser.parse_args()
    action = args.action
    topics = args.topics

    if action == 'create':
        kafka_admin.create_topics(topics)

    if action == 'delete':
        kafka_admin.delete_topics(topics)


if __name__ == '__main__':
    main()
