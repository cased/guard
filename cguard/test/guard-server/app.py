from flask import Flask, request
import time

app = Flask(__name__)


@app.route("/")
def root():
    return "test guard-server is live"


@app.route("/approvals")
def create_approval(approval_id):
    # create approval
    return {"status": "ok"}


@app.route("/approvals/<approval_id>")
def approval(approval_id):
    params = request.args
    delay = params.get("delay")
    deny = params.get("deny")

    if delay:
        time.sleep(int(delay))

    if deny:
        return {"approved": False}

    return {"approved": True}
