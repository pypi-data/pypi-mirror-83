# Serialize json messages
import json
import logging
import base64
import os
from kafka import KafkaConsumer,TopicPartition,KafkaAdminClient
from kafka.errors import KafkaError
import threading
import time
import ssl
from time import sleep
from kafka import KafkaClient

class KNativeKafkaConsumer(threading.Thread):
    daemon = True    
    ssl.match_hostname = lambda cert, hostname: True
    def __init__(self,topics:str,group_id:str):

        """
        Initialize a KNativeKafkaConsumer class based on the input params and the environment variables.
        Parameters
        ----------
           :param self: KNativeKafkaConsumer object                 
           :param topics: Kafka topic name
           Check whether the topic is passed as parameter, if not, get from the os.environ.

        """
    
        self.logger = logging.getLogger()
        self.logger.info("Initializing Kafka Consumer")
     
        self.group_id = group_id
  
        
        if topics:
            self.topics=topics
        elif 'KAFKA_TOPIC' in os.environ:
            self.topics=os.environ['KAFKA_TOPIC']
        else:
            raise ValueError('Topic is required!')
                    
 
        bootstrap_server=os.getenv('KAFKA_BOOTSTRAP_SERVERS',default='localhost:9092')
        is_tls_enable=os.getenv('KAFKA_NET_TLS_ENABLE',default='False')
        if is_tls_enable == 'True' or is_tls_enable == 'true' or is_tls_enable == 'TRUE':
            self.security_protocol='SSL'
            if 'KAFKA_NET_TLS_CA_CERT' not in os.environ:
                raise ValueError( 'TLS CA Certificate is required!')
            if 'KAFKA_NET_TLS_CERT' not in os.environ:
                raise ValueError( 'TLS Certificate is required!')
            if 'KAFKA_NET_TLS_KEY' not in os.environ:
                raise ValueError( 'TLS Key is required!')
            os.environ['KAFKA_NET_TLS_CA_CERT'] = 'ca.crt'
            os.environ['KAFKA_NET_TLS_CERT'] = 'cert.pem'
            os.environ['KAFKA_NET_TLS_KEY'] =   'key.pem'   
            self.ssl_cafile=os.environ['KAFKA_NET_TLS_CA_CERT']
            self.ssl_certfile=os.environ['KAFKA_NET_TLS_CERT']
            self.ssl_keyfile=os.environ['KAFKA_NET_TLS_KEY']

        else:
            self.security_protocol="PLAINTEXT"
            self.ssl_cafile=None
            self.ssl_certfile=None
            self.ssl_keyfile=None
            self.logger.info("Inside else")
        self.logger.info("KafkaConsumer Instance Creation")

        try:                
            self.consumer=KafkaConsumer(                      
                          bootstrap_servers=bootstrap_server,   
                          group_id=group_id,     
                          security_protocol=self.security_protocol,
                          ssl_check_hostname=True,
                          ssl_cafile=os.environ['KAFKA_NET_TLS_CA_CERT'],
                          ssl_certfile=os.environ['KAFKA_NET_TLS_CERT'],
                          ssl_keyfile=os.environ['KAFKA_NET_TLS_KEY'],
                          auto_offset_reset='earliest', 
                          enable_auto_commit=False,
                          api_version=(2,0,0))        
        except KafkaError as e:
  
            print("KafkaError while creating consumer - {}".format(e))
            self.logger.error("Kafka Error %s", "major problem", exc_info=1)
        
        except Exception as ex:
            print("Exception while creating consumer - {}".format(ex))
            self.logger.error("Kafka Exceptioon, There is a  %s", "major problem", exc_info=1)
 

    def getMessage(self):
        """
        Get the message
        Parameters
        ----------
            :param self: KNativeKafkaConsumer object               
        Returns
        -------                    
            :return: message value
        """
        print("**** Print the Messages ****")
        
        try:
            self.consumer.subscribe([self.topics])
            print("Subscribe")
            for message in self.consumer:
                if message is not None:
                    print("topic={} partition={} offset={} key={} value={}".format(message.topic,
                                                                        message.partition,
                                                                        message.offset,
                                                                        message.key,
                                                                        message.value))


        except Exception as ex:
                print("Exception while getting the message - {}".format(ex))
                self.logger.error("Exception -- While getting the message %s", "major problem. We got an exception!", exc_info=1)

    def seek_to_position(self, topic, partition, offset):
        """
        Seek to the given offset.
        Arguments:
          topic(str): topic name
          partition(int): partition number
          offset(int): offset number
        Returns:
          result(bool) : False if exception occures, True otherwise
        """
        print("seeking to position {}:{}:{}".format(topic, partition, offset))
        topic_partition = TopicPartition(topic=topic, partition=partition)
        try:
            self.consumer.seek(partition=topic_partition, offset=offset)
            result = True
        except KafkaError as exc:
            print("Exception during seek - {}".format(exc))
            result = False
        return result
        
   