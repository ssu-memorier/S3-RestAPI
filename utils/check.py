from apiUser.models import Content


def isObjectExist(uid, dir, key):
    try:
        Content.objects.get(uid=uid, dir=dir, key=key)
        return True
    except:
        return False
