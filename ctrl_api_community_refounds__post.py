import json

from django.http import HttpResponse

from sync.tasks import task_manager


# @class_declaration interna_post #
class interna_post():
    pass


# @class_declaration community_sync_post #
from models.flsyncppal import flsyncppal_def as syncppal


class community_sync_post(interna_post):

    @staticmethod
    def start(pk, data):
        result = None
        status = None

        if "passwd" in data and data["passwd"] == syncppal.iface.get_param_sincro('apipass')['auth']:
            response = task_manager.task_executer("b2c_refounds_post", data)
            if response:
                result = response["data"]
                status = response["status"]
        else:
            result = {"msg": "Autenticación denegada"}
            status = 401

        return HttpResponse(json.dumps(result), status=status, content_type="application/json")


# @class_declaration post #
class post(community_sync_post):
    pass
