[Anan](https://www.blueletterbible.org/lang/lexicon/lexicon.cfm?strongs=H6051)
====

A pytest plugin to run all tests in parallel via AWS Step Functions

**This is very rough currently**


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
