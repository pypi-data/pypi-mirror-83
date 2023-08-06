"""Dispatcher run

Usage:
  dispatcher.py NAMESPACE ZK_HOSTS
"""
import json
import logging
import random
import time
from collections import defaultdict
from datetime import datetime
from functools import reduce

import click
from kazoo.client import KazooClient

from telecom_coworker import log
from telecom_coworker.cache.big_cache import BigCache
from telecom_coworker.models import TaskState, STATE_EXITED
from telecom_coworker.utils import search_dict_by_keys


class Dispatcher(object):

    def __init__(self, namespace, hosts="localhost:2181"):
        self.namespace = namespace
        self.zk = KazooClient(hosts=hosts)
        self.namespace = namespace
        self.cache: BigCache = None

        self.changed = True

    def _watch_tasks(self, next_tasks):
        self.changed = True

    def _watch_workers(self, next_workers):
        self.changed = True

    def _master_func(self):
        log.info("I ready to by a good dispatcher")
        self.cache = BigCache(self.zk, self.namespace,
                              canceled_tasks_handle_func=self.canceled_tasks_handle,
                              lost_workers_handle_func=self.lost_workers_handle,
                              added_tasks_handle_func=self.added_tasks_handle,
                              added_workers_handle_func=self.added_workers_handle)

        self._assign_mapping = self.cache.assign_mapping()

        self.zk.ChildrenWatch(f"{self.namespace}/tasks")(self._watch_tasks)
        self.zk.ChildrenWatch(f"{self.namespace}/workers")(self._watch_workers)

        while True:
            # self.handle_messages()
            self.assign_task_if_needed()
            time.sleep(2)

    def assign_task_if_needed(self):
        log.info("==> assign_task_if_needed")
        if self.changed:
            self.assign_tasks()
            self.changed = False

    def canceled_tasks_handle(self, canceled_tasks):
        log.info(f"canceled tasks: {canceled_tasks}")
        unassign_worker_task = search_dict_by_keys(self._assign_mapping, canceled_tasks)
        self._unassign_tasks(unassign_worker_task)

    def lost_workers_handle(self, lost_workers):
        log.info(f"lost workers: {lost_workers}")
        self._unassign_workers(lost_workers)

    def added_workers_handle(self, added_workers):
        log.info(f"added workers: {added_workers}")

    def added_tasks_handle(self, added_tasks):
        log.info(f"added tasks: {added_tasks}")

    def assign_tasks(self):
        assigned_tasks = reduce(lambda s1, s2: s1 | s2, self._assign_mapping.values(), set())
        unassigned_tasks = self.cache.tasks - assigned_tasks

        task_infos_by_type = defaultdict(list)
        for ut in unassigned_tasks:
            task_infos_by_type[self.cache.task_infos[ut]["task_type"]].append(self.cache.task_infos[ut])

        assign_count = {w: len(tasks) for w, tasks in self._assign_mapping.items()}

        worker_infos_by_type = defaultdict(list)
        for w in self.cache.worker_infos.values():
            worker_infos_by_type[w["handle_type"]].append(w)

        for task_type in task_infos_by_type:
            tasks = task_infos_by_type[task_type]

            for t in tasks:
                workers = [w for w in worker_infos_by_type[task_type] if
                           w.get("max_handle_num", 2) - assign_count.get(w['wid'], 0) > 0]
                if not workers:
                    log.warning(f"WARNING: Task type {task_type} need more worker")
                    break
                w = random.choice(workers)
                self.assign_task_to_worker(t, w)
                assign_count[w['wid']] = assign_count.get(w['wid'], 0) + 1

    def assign_task_to_worker(self, task, worker):
        t = task["tid"]
        w = worker['wid']
        log.info("assign task %s to worker: %s", t, w)
        task_content = json.dumps(task).encode("utf-8")
        self.zk.create(f"{self.namespace}/assign/{w}/{t}", task_content, makepath=True)
        self._assign_mapping[w].add(t)

    def _unassign_tasks(self, worker_task_map: defaultdict):
        for w, tasks in worker_task_map.items():
            log.info("unassign task: %s by worker: %s", tasks, w)

            for t in tasks:
                self.zk.delete(f"{self.namespace}/assign/{w}/{t}")
                self._assign_mapping[w].discard(t)

    def _unassign_workers(self, workers):
        for w in workers:
            w_tasks = self._assign_mapping[w]

            for task in w_tasks:
                exited_task_state = TaskState(tid=task, state=STATE_EXITED, exitcode=-9,
                                              updated_at=datetime.now().isoformat())
                self.zk.ensure_path(f"{self.namespace}/tasks/{task}/state")
                self.zk.set(f"{self.namespace}/tasks/{task}/state", json.dumps(exited_task_state).encode("utf-8"))

            self.zk.delete(f"{self.namespace}/assign/{w}", recursive=True)
            if w in self._assign_mapping:
                self._assign_mapping.pop(w)

    def _ensure_base_node(self):
        self.zk.ensure_path(f"{self.namespace}/tasks")
        self.zk.ensure_path(f"{self.namespace}/workers")
        self.zk.ensure_path(f"{self.namespace}/assign")
        self.zk.ensure_path(f"{self.namespace}/messages")
        self.zk.ensure_path(f"{self.namespace}/failed_tasks")

    def run(self):
        self.zk.start()
        self._ensure_base_node()
        election = self.zk.Election(f"{self.namespace}/master", "my-identifier")
        election.run(self._master_func)

    def inspect(self):
        log.info(f"assign cache: {self._assign_mapping}")

    def handle_messages(self):
        pass


@click.command()
@click.argument("namespace")
@click.argument("zk_hosts")
def main(namespace, zk_hosts):
    logging.basicConfig(level=logging.DEBUG)

    dispatcher = Dispatcher(namespace, zk_hosts)
    dispatcher.run()


if __name__ == '__main__':
    main()
