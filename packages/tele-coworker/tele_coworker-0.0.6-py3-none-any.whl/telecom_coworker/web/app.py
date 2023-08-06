from flask import Flask, request, render_template, flash, redirect, url_for
from kazoo.exceptions import NoNodeError

from telecom_coworker.cache.big_cache import BigCache
from telecom_coworker.cache.children_data_cache import ChildrenDataCache
from telecom_coworker.client import Client
from telecom_coworker.models import Task
from telecom_coworker.web import ok, fail
from telecom_coworker.web.config import Config
from telecom_coworker.web.stats import Stats

app = Flask(__name__)
app.config.from_object(Config)

tele_client = Client(namespace=app.config['ZK_NAMESPACE'], hosts=app.config['ZK_HOSTS'])
tele_client.connect()

big_cache = BigCache(tele_client.zk, tele_client.namespace)
stats = Stats(big_cache)

msg_handler = ChildrenDataCache(tele_client.zk, f"/{tele_client.namespace}/messages")


@app.route("/")
def index():
    task_size = stats.tasks_total_num()
    worker_size = stats.workers_total_num()
    payload_size = stats.payload_total()
    task_stats = stats.task_stats()
    task_type_list_need_more_workers = stats.task_type_list_need_more_workers()
    messages = msg_handler.data.values()

    return render_template("index.html", task_size=task_size,
                           worker_size=worker_size, payload_size=payload_size,
                           task_stats=task_stats,
                           task_type_list_need_more_workers=task_type_list_need_more_workers,
                           messages=messages)


@app.route("/page/workers")
def page_workers():
    workers = stats.worker_stats().values()
    return render_template("workers.html", workers=workers)


@app.route("/page/task", methods=('GET', 'POST'))
def page_task():
    if request.method == 'POST':
        tid = request.form.get('tid')
        if tid is not None and len(tid) > 5:
            return redirect(url_for("page_task", tid=tid))
        else:
            flash("没有找到对应的任务")

    query_task_id = request.args.get('tid')
    if query_task_id is not None and len(query_task_id) > 0:
        try:
            state = tele_client.get_task_state(query_task_id)
            return render_template("task.html", state=state)
        except NoNodeError as e:
            flash('没有找到对应的任务')

    return render_template("task.html")


@app.route('/task', methods=['POST'])
def create_task():
    try:
        task: Task = request.json
    except AttributeError as e:
        return fail(40, "需要参数: task_type:str[len>5], params:dict")

    if len(task["task_type"]) < 5:
        return fail(41, '需要参数: task_type:str[len>5]')

    tid = tele_client.add_task(task["task_type"], **task['params'])

    return ok({"task_id": tid})


@app.route('/task/<uuid:task_id>/cancel', methods=['GET', 'POST'])
def cancel_task(task_id):
    result = tele_client.cancel_task(task_id)
    if result:
        return ok()
    else:
        return fail(44, '没有找到对应的Task')
