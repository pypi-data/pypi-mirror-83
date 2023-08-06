import json

from tidy3d.config import Config
from tidy3d.httputils import post2, get2, delete2


def newProject(taskParam, solverVersion=Config.VERSION_FDTD):
    return post2(f'fdtd/model/default/task', {
        'taskParam': json.dumps(taskParam),
        'solverVersion': solverVersion
    })


def getProject(itemId):
    return get2(f'fdtd/task/{itemId}')


def deleteProject(itemId):
    return delete2(f'fdtd/task/{itemId}')


def listProjects():
    return get2(f'fdtd/models')
