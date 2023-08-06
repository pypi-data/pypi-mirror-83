import json
from uuid import uuid4 as uuid

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NotEmptyError

from telecom_coworker import log
from telecom_coworker.models import Task, TaskState, STATE_PENDING


class Client(object):
    def __init__(self, namespace, hosts="localhost:2181"):
        self.namespace = namespace
        self.zk = KazooClient(hosts=hosts)

    def add_task(self, task_type, task_id=None, **params):
        tid = task_id if task_id is not None else str(uuid())
        task: Task = {"tid": tid, "task_type": task_type, "params": params}
        self.zk.create(f"{self.namespace}/tasks/{tid}", json.dumps(task).encode("utf-8"))
        return tid

    def cancel_task(self, task_id):
        try:
            self.zk.delete(f"{self.namespace}/tasks/{task_id}", recursive=True)
            return True
        except (NoNodeError, NotEmptyError) as e:
            log.exception("cancel task failed, ERROR:%s", e)
            return False

    def connect(self):
        self.zk.start()

    def get_task_state(self, task_id):
        try:
            state_str, _ = self.zk.get(f"{self.namespace}/tasks/{task_id}/state")
            state: TaskState = json.loads(state_str.decode('utf-8'))
        except NoNodeError as e:
            if self.zk.exists(f"{self.namespace}/tasks/{task_id}"):
                state = TaskState(tid=task_id, state=STATE_PENDING)
                return state
            raise e

        return state
