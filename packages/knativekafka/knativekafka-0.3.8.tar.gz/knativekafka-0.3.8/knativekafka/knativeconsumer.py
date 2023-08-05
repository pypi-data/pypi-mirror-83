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

class KNativeConsumer(threading.Thread):
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
        print("Initializing Kafka Consumer")
        self.group_id = group_id
  
        
        if topics:
            self.topics=topics
        elif 'KAFKA_TOPIC' in os.environ:
            self.topics=os.environ['KAFKA_TOPIC']
        else:
            raise ValueError('Topic is required!')
                    
 
        bootstrap_server=os.getenv('KAFKA_BOOTSTRAP_SERVERS',default='localhost:9092')
        is_tls_enable=os.getenv('KAFKA_NET_TLS_ENABLE',default='False')
        if is_tls_enable == 'True' or is_tls_enable == 'true':
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
 
            self.logger.info("Inside if")
        else:
            self.security_protocol="PLAINTEXT"
            self.ssl_cafile=None
            self.ssl_certfile=None
            self.ssl_keyfile=None
        self.logger.info("KafkaConsumer Instance Creation")
        print("KafkaConsumer Instance Creation")
        try:                
            self.consumer=KafkaConsumer(
                          topics=self.topics,
                          bootstrap_servers=bootstrap_server,   
                          group_id=group_id,     
                          security_protocol=self.security_protocol,
                          ssl_check_hostname=True,
                          ssl_cafile=os.environ['KAFKA_NET_TLS_CA_CERT'],
                          ssl_certfile=os.environ['KAFKA_NET_TLS_CERT'],
                          ssl_keyfile=os.environ['KAFKA_NET_TLS_KEY'],
                          api_version=(0,10),
                          max_poll_records=2,
                          auto_offset_reset='earliest',
                          enable_auto_commit=False)
                         
        except KafkaError as e:
            
            print("KafkaError")
            print("KafkaError while creating consumer - {}".format(e))
            self.logger.error(f'Kafka Error {e}')
            self.logger.error("Houston, we have a %s", "major problem", exc_info=1)
        
        except Exception as ex:
            print("Inexception")
            print("Exception while creating consumer - {}".format(ex))
            self.logger.error(f'Kafka Eexceptioon {ex}')
            self.logger.error("Houston, we have a %s", "major problem", exc_info=1)
 
        print("KafkaConsumer Creation Success!")
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
            # (!?) wtf, why we need this to get partitions assigned
            # AssertionError: No partitions are currently assigned if poll() is not called
            self.consumer.poll()
            self.consumer.seek_to_beginning()

            # also AssertionError: No partitions are currently assigned if poll() is not called
            print('partitions of the topic: ',self.consumer.partitions_for_topic(self.topics))
            self.logger.error('partitions of the topic: ')
            self.logger.error(self.consumer.partitions_for_topic(self.topics))
            from kafka import TopicPartition
            print('before poll() x2: ')
            # print(self.consumer.position(TopicPartition(self.topics, 0)))
            print(self.consumer.position(TopicPartition(self.topics, 2)))
            self.logger.error(self.consumer.position(TopicPartition(self.topics, 2)))
            # (!?) sometimes the first call to poll() returns nothing and doesnt change the offset
            messages = self.consumer.poll()
            sleep(1)
            messages = self.consumer.poll()

            print('after poll() x2: ')
            #print(self.consumer.position(TopicPartition(self.topics, 0)))
            print(self.consumer.position(TopicPartition(self.topics, 2)))
            self.logger.error(self.consumer.position(TopicPartition(self.topics, 2)))
            print('messages: ', messages)
            self.logger.error(messages)


        except Exception as ex:
                print("Inexception")
                print("Exception while getting the message - {}".format(ex))
                self.logger.error(f'Kafka Exception {ex}')
                self.logger.error("We have a %s", "major problem. We got an exception!", exc_info=1)

    def getMetric(self):
        tp = self.consumer.assignment()
        committed_offset = self.consumer.committed(tp)
        print("committed_offset")
        print(committed_offset)
        if committed_offset is None:
            committed_offset = 0
        for _, v in self.consumer.end_offsets([tp]).items():
            latest_offset = v
        print("committed_offset")
        print(committed_offset)
        self.logger.error(committed_offset)
        print("latest offset")
        print(latest_offset)
        self.logger.error(latest_offset)
        print("lag")
        print(latest_offset - committed_offset)

        self.consumer.close(autocommit=False)
