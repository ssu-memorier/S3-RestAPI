from constants import LOG


def actionError(action):
    return action+LOG.ACTION_ERROR_STATEMENT


def printSuccessRest(action):
    print(action+LOG.SUCCESS_STATEMENT)
