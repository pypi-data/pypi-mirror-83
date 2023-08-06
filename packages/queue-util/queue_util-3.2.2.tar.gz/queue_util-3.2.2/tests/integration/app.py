#!env python

import sys
import time

from threading import Thread

from queue_util import Consumer, Producer


MAX_RUN_TIME = 120.0


def main(rabbit_queue_name, rabbit_host='127.0.0.1', rabbit_port=5672):
    messages = [i for i in range(42, 690)]

    producer = Producer(
        rabbit_queue_name,
        rabbit_host,
        rabbit_port,
        serializer='json',
    )
    for message in messages:
        producer.put(message)

    del producer

    received = []

    def handle_data(item):
        received.append(item)

    consumer = Consumer(
        rabbit_queue_name,
        handle_data,
        rabbit_host,
        rabbit_port,
        max_retries=10,
    )
    consumer_thread = Thread(
        target=consumer.run_forever,
        kwargs={'wait_timeout_seconds': 0.1},
    )

    start_time = time.time()
    consumer_thread.start()

    while (
            time.time() < start_time + MAX_RUN_TIME and
            len(received) < len(messages) and
            consumer_thread.is_alive()
    ):
        time.sleep(MAX_RUN_TIME/100.0)

    consumer.terminate = True
    consumer_thread.join(timeout=10.0)
    if consumer_thread.is_alive():
        raise RuntimeError('Consumer still running, received {0} items ({1} unique)'.format(
            len(received),
            len(set(received)),
        ))
    if len(set(received)) < len(messages):
        raise RuntimeError("Consumer didn't get it all, received {0} items ({1} unique)".format(
            len(received),
            len(set(received)),
        ))
    consumer_thread.join()


if __name__ == '__main__':
    RABBIT_HOST = '127.0.0.1'
    RABBIT_QUEUE_NAME = 'queue_util_test_app'

    main(RABBIT_QUEUE_NAME, rabbit_host=RABBIT_HOST, rabbit_port=int(sys.argv[1]))
