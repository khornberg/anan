import json
import pytest
from pytest import ExitCode
from contextlib import redirect_stdout
import io


def run_tests(*args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        result = pytest.main(*args, **kwargs)
    s = f.getvalue()
    return ExitCode(result), s


def run(event, context):
    args = event.get("Input")
    exit_code, output = run_tests(args)
    body = {"exit_code": str(exit_code), "output": str(output), "tests": event.get('Input')}
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
