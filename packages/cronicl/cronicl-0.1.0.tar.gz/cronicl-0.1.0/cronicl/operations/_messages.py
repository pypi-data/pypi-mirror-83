"""
Implements an envelope for payloads.

The envelope includes meta information about the payload, for example
a unique identifier and a flag for if the message and its
descendants are being traced. 

The message also carries a set of attributes, this allows key/value
information separate to the payload to be sent with the payload.
"""

# we're using to select random samples so prng is good enough
import uuid, logging, random 
try:
    import ujson as json
except ImportError:
    import json
from ._trace import get_tracer
from ._sanitizer import sanitize_record


class Message(object):

    def __init__(self, payload=None, traced=False, topic='dead_letters', initializer=None):
        # unique identifier for this message
        self.id = str(uuid.uuid4()) 
        self.payload = payload
        self.attributes = {}
        self.traced = traced
        self.initializer = initializer
        if not self.initializer:
            self.initializer = self.id
        

    def __repr__(self):
        return self.payload


    def __str__(self):
        return str(self.payload)


    def trace(self, operation='not defined', version='0'*8, child='', force=False):
        if self.traced or force:
            sanitized_record = sanitize_record(self.payload, self.initializer)
            try:
                sanitized_record = json.dumps(sanitized_record)
            except ValueError:
                sanitized_record = str(sanitized_record)
            get_tracer().emit(self.id, operation, version, child, self.initializer, sanitized_record)


def create_new_message(payload, sample_rate=0):
    """
    Factory for messages, includes logic to select messages for 
    random sampling.
    """
    if sample_rate >= 1:
        traced = True
    elif sample_rate > 0:
        traced = random.randint(1, round(1/sample_rate)) == 1
    else:
        traced = False
    message = Message(payload=payload, traced=traced)
    message.trace(operation='Create Message', child=message.id)
    return message