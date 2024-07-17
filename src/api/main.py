import json
import logging
from typing import Union
from src.configs.config import settings
from src.helpers.sendgrid_event import sendgrid_event_helper

from src.helpers.kafka_client import kafka_client
from fastapi import FastAPI, Request, Response, status, HTTPException

logger = logging.getLogger(__name__)

class InvalidVerificatioError(Exception):
    """Invalid Verification"""

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    docs_url=settings.docs_url
)


@app.get("/")
def read_root():
    return {"Sendgrid Webhook Starter"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Method to receive webhook event from Sendgrid.
    """
    try:
        print('\n### - Received event - ###')    
        headers = request.headers
        result  = await request.json()
        send_grid_payload = json.dumps(
              result,
              sort_keys=True,
              separators=(',', ':')
        ).replace("},{","},\r\n{") + '\r\n'   #NB Found this in Sendgrid github test file https://github.com/sendgrid/sendgrid-python/blob/main/test/unit/test_eventwebhook.py

        if sendgrid_event_helper.is_valid_signature(send_grid_payload, headers, settings.sendgrid_verification_key):   
            for event in result:
                message = json.dumps(event).encode('utf-8').decode()
                publish_to_kafka( message )
            return Response(content='RCV_OK', status_code=status.HTTP_200_OK)
        else:
            raise InvalidVerificatioError("The verification code is not provided or invalid")
    except InvalidVerificatioError as ex:
             print(ex)
             return Response(content='INVALID_VERIFICATION_KEY',status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as ex:
            print(ex)
            return Response(content='INTERNAL_SERVER_ERROR',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def callback(err, msg):
    if (err):
         print(f"Error : {err}")
         logger.error(err)

    logger.info(msg.value())    
    print('\n### - Kafka_Publish_OK - ###')

def publish_to_kafka(msg):
    print('\n### - Publishing to Kafka - ###')
    try:
        kafka_client.produce(settings.kafka_topic, settings.kafka_config, "", msg, callback)
    except BufferError as be:
            logger.error( "BufferError publishing topic [{}]:[{}]".format(settings.kafka_topic,be) )

    except Exception as  e:
            logger.error( "Error publishing data at topic [{}]:[{}]".format(settings.kafka_topic,e) )