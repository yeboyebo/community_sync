# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration community_sync #
from YBLEGACY.constantes import *
from random import choice
from models.flsyncppal import flsyncppal_def as syncppal

class community_sync(interna):

    params = syncppal.iface.get_param_sincro('apipass')

    def community_sync_consultapuntos(self, params):
        try:
            if "passwd" in params and params["passwd"] == self.params['auth']:

                if "email" not in params:
                    return {"Error": "Formato Incorrecto", "status": 0}
                email = params['email']

                existe_tarjeta = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"codtarjetapuntos", ustr(u"email = '", email, u"'"))

                if not existe_tarjeta:
                    return {"Error": "No se ha encontrado la tarjeta.", "status": 1}

                saldopuntos = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"saldopuntos", ustr(u"email = '", email, u"'"))
                return {"saldoPuntos": saldopuntos, "email": email}
            else:
                return {"Error": "Petición Incorrecta", "status": -1}
        except Exception as e:
            qsatype.debug(ustr(u"Error inesperado consulta de puntos: ", e))
            return {"Error": params, "status": -2}
        return False
    
    def community_sync_getDesc(self):
        return None

    def __init__(self, context=None):
        super().__init__(context)

    def consultapuntos(self, params):
        return self.ctx.community_sync_consultapuntos(params)

    def getDesc(self):
        return self.ctx.community_sync_getDesc()


# @class_declaration head #
class head(community_sync):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
