from controllers.base.default.controllers.recieve_sync import RecieveSync
from controllers.api.community.points.serializers.cm_log_serializer import CmB2CLogSerializer
from models.flfact_tpv.objects.eg_logtarjetasweb_raw import CmLogPoints


class CmB2CPointsPost(RecieveSync):

    def __init__(self, params=None):
        super().__init__("cmb2cpoints", params)

    def sync(self):
        data = self.params
        if not data:
            return {"data": {"log": "No se han podido obtener los datos de la tarjeta"}, "status": 400}

        if "tarjeta" not in data:
            return {"data": {"log": "No se han podido obtener los datos de la tarjeta"}, "status": 400}

        if "codtarjetapuntos" not in data["tarjeta"]:
            return {"data": {"log": "No se ha podido obtener el identificador de la tarjeta."}, "status": 400}

        codtarjetapuntos = data["tarjeta"]["codtarjetapuntos"]
        data = self.get_serializer().serialize(data["tarjeta"])
        tarjeta = self.create_model(data)
        tarjeta.save()
        self.log("Éxito", "Tarjeta {} sincronizado".format(codtarjetapuntos))
        return {"data": {"log": self.logs}, "status": 200}

    def get_serializer(self):
        return CmB2CLogSerializer()

    def create_model(self, data):
        return CmLogPoints(data)
