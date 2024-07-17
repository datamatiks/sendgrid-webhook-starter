from sendgrid.helpers.eventwebhook import EventWebhook, EventWebhookHeader
from fastapi import Request, Response, status
from ellipticcurve.signature import Signature
from ellipticcurve.ecdsa import Ecdsa

class SendgridEventHelper:
    """Sendgrid event webhook helper for signature verification"""

    def is_valid_signature(self, payload, headers: Request.headers, public_key):
        print('### - Validating signature - ###')
        print(headers)
        signature = headers[EventWebhookHeader.SIGNATURE]
        timestamp = headers[EventWebhookHeader.TIMESTAMP]
        event_webhook = EventWebhook()
        print(f"{signature} : {timestamp}")
        ec_public_key = event_webhook.convert_public_key_to_ecdsa(public_key)
        is_verified = event_webhook.verify_signature(
            payload,
            signature,
            timestamp,
            ec_public_key
        )
        print(f"IS_VERIFIED: {is_verified}")
        return is_verified

sendgrid_event_helper = SendgridEventHelper()