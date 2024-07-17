import os
import socket
from confluent_kafka import Producer
from pydantic import BaseConfig



class GlobalConfig(BaseConfig):  
    def __init__(self):  
        pass  

    title: str = "Sendgrid Webhook Starter"  
    version: str = "0.1.0"  
    description: str = "Reverse api to be called by Sendgrid for Email Activities"   
    docs_url: str = "/docs"  
    redoc_url: str = "/redoc"
    api_prefix: str = "/api"
    db_echo_log: bool = True
    kafka_username: str =  os.environ.get("CLUSTER_API_KEY")
    kafka_password: str =  os.environ.get("CLUSTER_API_SECRET")
    kafka_server: str   =  os.environ.get("KafkaServer")
    kafka_topic: str    =  os.environ.get("KafkaTopic")
    sendgrid_verification_key: str = os.environ.get("SendgridVerificationKey")

    @property  
    def kafka_config(self) -> dict:
        return {'bootstrap.servers': self.kafka_server,
                'security.protocol': 'SASL_SSL',
                'sasl.mechanism': 'PLAIN',
                'sasl.username': self.kafka_username,
                'sasl.password': self.kafka_password,
                'client.id': socket.gethostname(),
                'session.timeout.ms': 45000
        }
        
    
        
settings = GlobalConfig()