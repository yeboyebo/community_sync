# @class_declaration interna_eg_logdevolucionesweb #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_eg_logdevolucionesweb(modelos.mtd_eg_logdevolucionesweb, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration community_sync_eg_logdevolucionesweb #
class community_sync_eg_logdevolucionesweb(interna_eg_logdevolucionesweb, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eg_logdevolucionesweb #
class eg_logdevolucionesweb(community_sync_eg_logdevolucionesweb, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.eg_logdevolucionesweb_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
