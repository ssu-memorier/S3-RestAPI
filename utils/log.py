from constant import LOG


def ActionError(action):
    return action+LOG.ACTION_ERROR_STATEMENT


def printSuccessRest(action):
    print(action+LOG.SUCCESS_STATEMENT)
