# @class_declaration interna_tpv_tarjetaspuntos #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_tpv_tarjetaspuntos(modelos.mtd_tpv_tarjetaspuntos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration community_sync_tpv_tarjetaspuntos #
class community_sync_tpv_tarjetaspuntos(interna_tpv_tarjetaspuntos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.csr()
    def consultapuntos(params):
        return form.iface.consultapuntos(params)

    @helpers.decoradores.csr()
    def generarmovimentopuntosoperacionesmagento(params):
        return form.iface.generarmovimentopuntosoperacionesmagento(params)


# @class_declaration tpv_tarjetaspuntos #
class tpv_tarjetaspuntos(community_sync_tpv_tarjetaspuntos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.tpv_tarjetaspuntos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
