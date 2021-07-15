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
                return {"saldoPuntos": saldopuntos, "email": email, "codtarjetapuntos": existe_tarjeta}
            else:
                return {"Error": "Petición Incorrecta", "status": -1}
        except Exception as e:
            qsatype.debug(ustr(u"Error inesperado consulta de puntos: ", e))
            return {"Error": params, "status": -2}
        return False

    def community_sync_generarmovimentopuntosoperacionesmagento(self, params):
        try:
            print("1")
            if "passwd" in params and params["passwd"] == self.params['auth']:
                print("2")
                if "email" not in params:
                    return {"Error": "Formato Incorrecto. Falta el email en los parametros", "status": -1}
                if "operacion" not in params:
                    return {"Error": "Formato Incorrecto. Falta la operacion en los parametros", "status": -1}
                if "canpuntos" not in params:
                    return {"Error": "Formato Incorrecto. Falta la cantidad de puntos en los parametros", "status": -1}
                print("3")
                if not self.acumularPuntosOperacionesMagento(params):
                    return False
                print("4")
                if not qsatype.FLUtil.execSql(ustr(u"UPDATE tpv_tarjetaspuntos SET saldopuntos = CASE WHEN (SELECT SUM(canpuntos) FROM tpv_movpuntos WHERE codtarjetapuntos = tpv_tarjetaspuntos.codtarjetapuntos) IS NULL THEN 0 ELSE (SELECT SUM(canpuntos) FROM tpv_movpuntos WHERE codtarjetapuntos = tpv_tarjetaspuntos.codtarjetapuntos) END WHERE email = '", str(params['email']), "'")):
                    return False
                print("5")
                return True

        except Exception as e:
            qsatype.debug(ustr(u"Error inesperado generarmovimentopuntosoperacionesmagento: ", e))
            return {"Error": "Petición Incorrecta", "status": 0}

        return True

    def community_sync_acumularPuntosOperacionesMagento(self, params):
        print("acumularPuntosOperacionesMagento")
        curTpvTarjetas = qsatype.FLSqlCursor("tpv_tarjetaspuntos")
        q = qsatype.FLSqlQuery()
        q.setSelect("codtarjetapuntos, saldopuntos")
        q.setFrom("tpv_tarjetaspuntos")
        q.setWhere("email = '" + str(params['email']) + "'")
        print("acumularPuntosOperacionesMagento 1")
        if not q.exec_():
            return False
        print("acumularPuntosOperacionesMagento 2")
        while q.next():
            print("acumularPuntosOperacionesMagento 3")
            curTpvTarjetas.select("codtarjetapuntos = '" + q.value("codtarjetapuntos") + "'")
            if not curTpvTarjetas.first():
                return False
            print("acumularPuntosOperacionesMagento 4")
            curTpvTarjetas.setModeAccess(curTpvTarjetas.Edit)
            curTpvTarjetas.refreshBuffer()

            qsatype.FLSqlQuery().execSql("INSERT INTO tpv_movpuntos (codtarjetapuntos, fecha, fechamod, horamod, canpuntos, operacion, sincronizado, codtienda) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(str(q.value("codtarjetapuntos")), str(qsatype.Date())[:10], str(qsatype.Date())[:10], str(qsatype.Date())[-(8):], params['canpuntos'], params['operacion'], True, "AWEB"))

            if not curTpvTarjetas.commitBuffer():
                return False

        return True

    def community_sync_getDesc(self):
        return None

    def __init__(self, context=None):
        super().__init__(context)

    def consultapuntos(self, params):
        return self.ctx.community_sync_consultapuntos(params)

    def generarmovimentopuntosoperacionesmagento(self, params):
        return self.ctx.community_sync_generarmovimentopuntosoperacionesmagento(params)

    def acumularPuntosOperacionesMagento(self, params):
        return self.ctx.community_sync_acumularPuntosOperacionesMagento(params)

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
