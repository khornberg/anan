[Anan](https://www.blueletterbible.org/lang/lexicon/lexicon.cfm?strongs=H6051)
====

A pytest plugin to run all tests in parallel via AWS Step Functions

**This is very rough currently**

## Goal

Ideally this plugin will seamlessly
- create the cloud computing environment to run the tests
- run the tests in parallel
- reports the test results in a similar manner to running locally


## Work remaining

```
  write more tests for this
x￼ collect tests
￼ package function
  ￼ find code directory, install requirements (ugh), zip
￼ upload function
  ￼ read sls cf, find bucket, upload
￼ infrastructure created?
  ￼ create
￼ start step function
  ￼   get step function from create script
x   ￼ parse tests and make into expected data structure for step ƒ
x￼ wait
x￼ get output
x￼ parse out into individual runs
x￼ send to pytest for output
```


## Install (doesn't work)

pip install pytest-anan

### Testing this repo

```
npm install
pip install - requirements.txt
sls deploy
```

Add a file called `clouds.py`
Add
```
def getStateMachineArn():
    # replace this with the real arn
    return "arn:aws:states:us-east-2:111111111111:stateMachine:testStateMachine"
```

Then you can test this repo with
`python manual-run.py`

If all goes well you should get 4 test passing with the output.
