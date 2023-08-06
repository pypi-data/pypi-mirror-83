"""
Allow the ability to connect and publish to a queue.
"""
import logging
import time

import kombu
import six


class Producer(object):

    def __init__(self, dest_queue_name, rabbitmq_host, rabbitmq_port=None,
                 serializer=None, compression=None,
                 userid=None, password=None):
        connect_kwargs = {}
        if userid is not None:
            connect_kwargs['userid'] = userid
        if password is not None:
            connect_kwargs['password'] = password
        if rabbitmq_port is not None:
            connect_kwargs['port'] = rabbitmq_port
        broker = kombu.BrokerConnection(rabbitmq_host, **connect_kwargs)
        self.dest_queue = broker.SimpleQueue(
            dest_queue_name,
            serializer=serializer,
            compression=compression,
        )

    def put(self, item):
        """
        Put one item onto the queue.
        """
        self.dest_queue.put(item)

    def buffered_put(self, input_iter, batch_size, resume_threshold=0.1, delay_in_seconds=5.0):
        """
        Given an input iterator, keep adding batches of items to the
        destination queue.
        After each batch, wait for the queue size to drop to a certain level
        until putting in the next batch.
        (Wait until the queue size is batch_size * resume_threshold.)

        Note that it isn't exact, but it will attempt to ensure that the queue
        size never goes (much) beyond batch_size.
        """
        num_enqueued = 0
        while True:
            try:
                logging.debug('Starting batch (batch_size={0})'.format(batch_size))
                for i in range(batch_size):
                    self.put(six.next(input_iter))
                    num_enqueued += 1
                logging.debug('Batch done. {0} items enqueued so far'.format(num_enqueued))
            except StopIteration:
                # We're done!
                #
                logging.debug('Input exhausted. {0} items enqueued in total'.format(num_enqueued))
                break

            # After each batch, we need to pause briefly.
            # Otherwise get_num_messages won't include the messages that we
            # just enqueued.
            #
            time.sleep(delay_in_seconds)

            # Now that we have completed one batch, we need to wait.
            max_size = resume_threshold * batch_size
            num_messages = self.dest_queue.qsize()
            while num_messages >= max_size:
                logging.debug(
                    'Current queue size = {0}, waiting until size <= {1}'.format(
                        num_messages, max_size,
                    ),
                )
                time.sleep(delay_in_seconds)
                num_messages = self.dest_queue.qsize()
