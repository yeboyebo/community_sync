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

        if "customer" not in data:
            return {"data": {"log": "No se han podido obtener los datos de la tarjeta"}, "status": 400}

        if "email" not in data["customer"]:
            return {"data": {"log": "El Json no contiene el email del cliente."}, "status": 400}

        email = data["customer"]["email"]
        data = self.get_serializer().serialize(data["customer"])
        tarjeta = self.create_model(data)
        tarjeta.save()
        self.log("Éxito", "Tarjeta con Email {} sincronizado".format(email))
        return {"data": {"log": self.logs}, "status": 200}

    def get_serializer(self):
        return CmB2CLogSerializer()

    def create_model(self, data):
        return CmLogPoints(data)
