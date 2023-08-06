import json

from kazoo.client import KazooClient

from telecom_coworker.models import Message


def send_message(zk: KazooClient, namespace, msg: Message):
    zk.create(f"{namespace}/messages/msg-", json.dumps(msg).encode("utf-8"), sequence=True)


if __name__ == '__main__':
    zk = KazooClient()
    zk.start()
    send_message(zk, "basic", Message("test-type", "task_id1", "worker_1", "hello"))
