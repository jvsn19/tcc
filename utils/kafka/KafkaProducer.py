from json import dumps

from kafka import KafkaProducer as KP

class Singleton(type):
    _instances = {}
    _a = 10
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, *kwargs)

        return cls._instances[cls]

class KafkaProducer(metaclass = Singleton):
    _kafka_producer = None

    def __init__(self, bootstrap_servers = ['localhost:9092']):
        self.__class__.kafka_producer = KP(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda val: dumps(val).encode('utf-8'))

    @classmethod
    def send(cls, topic: str, value: dict):
        '''
        This method pushes a new value to the Kafka server. The value will be
        encoded as a json.
        topic: str
        value: dict()
        '''
        if not cls._kafka_producer:
            cls()
        cls.kafka_producer.send(topic = topic, value = value)
