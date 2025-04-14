import shutil


def resetDB(func):
    def wrapper():
        shutil.copy('base.db', 'operations.db')
        func()
    return wrapper


def removeTimestamp(inDict):
    if "timestamp" in inDict:
        del inDict["timestamp"]
    return inDict


def removeTransactionDatetime(inDict):
    inDict = removeTimestamp(inDict)
    for transaction in inDict["data"]:
        del transaction["transaction_datetime"]
    return inDict
