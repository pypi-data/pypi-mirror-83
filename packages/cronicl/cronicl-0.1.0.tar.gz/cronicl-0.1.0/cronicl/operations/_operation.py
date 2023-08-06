"""
Operation is a base class which includes most of the heavy-lifting
for tracing and auditing.

There are three methods which are safe to override, 'init', 'close'
and 'execute', 'execute' must be overridden. 'execute' should
contain the processing logic, 'init' is intended for activities
like opening files and caching lookups, 'close' for any tidy-up
like closing files. 'execute' must return a list of messages.
"""

import time, abc, logging, random
try:
    import ujson as json
except ImportError:
    import json
from ._trace import get_tracer
import inspect, hashlib
from .._queue import get_queue
from .._signals import Signals
import threading

class Operation(abc.ABC):

    def __init__(self):
        """
        IF OVERRIDEN, CALL THIS METHOD TOO.

        - like this Operation.__init__(self)
        """
        self.input_record_count = 0
        self.output_record_count = 0
        self.first_seen = 0
        self.execution_time = 0
        self.first_run = True
        self.my_version = None
        self.operation_name = ''
        self.lock = threading.Lock()
        self.errors = 0
        self.sample_rate = None
        self.retry_count = 0


    def init(self, **kwargs):
        """
        OVERRIDE IF REQUIRED

        Called once at the start of the pipeline.
        """
        pass


    def __call__(self, message):
        """
        DO NOT OVERRIDE THIS METHOD.
        
        This is where the auditting and tracing are implemented.
        """
        task_name = self.__class__.__name__

        if self.first_run:
            self.first_run = False
            self.first_seen = time.time()
            logging.debug('first run of: {}'.format(task_name))

        # deal with thread-unsafety
        self.lock.acquire() 
        self.input_record_count += 1
        self.lock.release()

        traced = message.traced
        start_ns = time.time_ns()

        tries = self.retry_count + 1
        while tries > 0:
            # the main processing payload
            try:
                results = self.execute(message)
                break # don't retry
            except KeyboardInterrupt:
                raise # don't count this as a processing error
            except:
                # don't reraise, count and continue
                self.lock.acquire() 
                self.errors += 1
                self.lock.release()
                tries -= 1   
                results = []

        return_type = type(results).__name__
        if return_type == 'generator' and not return_type == 'list':
            raise TypeError('{} must \'return\' a list of messages (list can be 1 element long)'.format(task_name))

        # deal with thread-unsafety
        self.lock.acquire() 
        self.execution_time += time.time_ns() - start_ns
        self.lock.release()

        response = []
        # if the result is None this will fail
        for result in results or []:
            if result is not None:
                message.trace(operation=task_name, version=self.version(), child=result.id, force=self.force_trace())

                # messages inherit some values from their parent,
                # traced and initializer are required to be the
                # same as part of their core function
                result.traced = traced
                result.initializer = message.initializer

                # deal with thread-unsafety
                self.lock.acquire() 
                self.output_record_count += 1
                self.lock.release()

                response.append(result)

        if len(response) == 0:
            message.trace(operation=task_name, version=self.version(), child='00000000-0000-0000-0000-000000000000', force=self.force_trace())

        return response

    @abc.abstractmethod
    def execute(self, record):
        """
        MUST BE OVERRIDEN

        THIS SHOULD RETURN AN LIST OF MESSAGES

        Called once for every incoming record
        """
        pass

    def version(self):
        """
        DO NOT OVERRIDE THIS METHOD.

        The version of the operation code, this is intended to 
        facilitate reproducability and auditability of the pipeline.

        The version is the last 8 characters of the hash of the 
        source code of the 'execute' method. This removes the need 
        for the developer to remember to increment a version 
        variable.

        Hashing isn't security sensitive here, it's to identify
        changes rather than protect information.
        """
        if not self.my_version:
            source = inspect.getsource(self.execute)
            full_hash = hashlib.sha224(source.encode())
            self.my_version = full_hash.hexdigest()[-8:]
        return self.my_version


    def close(self):
        """
        OVERRIDE IF REQUIRED

        Called once when pipeline has finished all records
        """
        pass


    def read_sensor(self):
        """
        IF OVERRIDEN, INCLUDE THIS INFORMATION TOO.

        This reads the auditting information from the operation.
        """
        return { 
            'process': self.__class__.__name__,
            'operation_name': self.operation_name,
            'version': self.version(),
            'input_records': self.input_record_count,
            'output_records': self.output_record_count,
            'errored_records': self.errors,
            'input_output_ratio': round(self.output_record_count / self.input_record_count, 4) if self.input_record_count else 0,
            'records_per_second': round(self.input_record_count / (self.execution_time / 1e9)) if self.execution_time else 0,
            'execution_start': self.first_seen,
            'execution_time': round(self.execution_time / 1e9, 4) if self.execution_time else 0
        }


    def run(self):
        """
        Method to run in a separate threat.
        """
        logging.debug(f"Thread running {self.operation_name} started")
        queue = get_queue(self.operation_name)
        # .get() is bocking, it will wait - which is okay if this
        # function is run in a thread
        message = queue.get()
        while not message == Signals.TERMINATE:
            results = self(message)
            for result in results:
                if result is not None:
                    reply_message = ( self.operation_name, result )
                    get_queue('reply').put(reply_message)
            message = queue.get()
        # None is used to exit the method
        logging.debug(f'TERM {self.operation_name}')


    def force_trace(self):
        """
        Operations have have higher tracing frequencies than the
        flow is set to; this doesn't affect the tracing at any
        other operation, preventing true tracing through the 
        pipeline but does increase observability at specific
        points.

        This does take into account if the message is already
        being traced.

        This was clamped between 0-1 when set.
        """
        if self.sample_rate:
            return random.randint(1, round(1/self.sample_rate)) == 1
        return False
