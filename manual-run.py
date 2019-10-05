import os
import json
from itertools import groupby
import uuid
import time
import boto3
import pytest
from pytest import ExitCode

import clouds

REGION = "us-east-2" # os.environ.get("AWS_REGION", "us-east-2")


def timeout():
    yield 1
    yield 2
    yield 3


timeouts = timeout()


class Rep(object):
    count_towards_summary = True


def get_step_function_client():
    return boto3.client("stepfunctions", region_name=REGION)


def start(tests, name):
    client = get_step_function_client()
    return client.start_execution(
        stateMachineArn=clouds.getStateMachineArn(), name=name, input=json.dumps({"tests": tests})
    )


def get_results(execution):
    client = get_step_function_client()
    response = client.describe_execution(executionArn=execution.get("executionArn"))
    while response.get("status") == "RUNNING":
        time.sleep(next(timeouts))
        response = client.describe_execution(executionArn=execution.get("executionArn"))
    return response


def get_stats(bodies):
    status_map = {"ExitCode.USAGE_ERROR": "failed", "ExitCode.OK": "passed"}
    stats = {}
    for k, g in groupby(bodies, key=lambda r: r["exit_code"]):
        stats.update({status_map.get(k): [Rep() for x in g]})
    return stats


def get_outputs(bodies):
    return [r["output"] for r in bodies]


def analyze_results(results, expected_results_length):
    if len(results) != expected_results_length:
        raise Exception(
            "something did not go well, the number of results was {} and we were expecting {}".format(
                len(results), expected_results_length
            )
        )
    bodies = [json.loads(result["Payload"]["body"]) for result in results]
    return get_stats(bodies), get_outputs(bodies)


class AnanPlugin(object):
    results = {}

    # TODO setup infrastructure automatically

    def pytest_runtestloop(self, session):
        name = str(uuid.uuid4())
        print("Starting run for {}".format(name))
        tests = [[i.nodeid] for i in session.items]
        execution = start(tests, name)
        print("Started run {}".format(execution.get("executionArn")))
        response = get_results(execution)
        self.results = json.loads(response.get("output"))
        return "NoOp for Cloudy Run"

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        stats, outputs = analyze_results(self.results, terminalreporter._numcollected)
        terminalreporter.stats = stats
        for output in outputs:
            terminalreporter.write(output)
            terminalreporter.write("\n")
        terminalreporter.write("<>< Ran and gathered from the clouds\n")


def run(args):
    # TODO Add region override
    result = pytest.main(args, plugins=[AnanPlugin()])
    return ExitCode(result)


if __name__ == "__main__":
    args = ["tests", "--verbose"]
    run(args)
