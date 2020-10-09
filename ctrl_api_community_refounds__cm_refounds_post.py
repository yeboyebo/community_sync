from controllers.base.default.controllers.recieve_sync import RecieveSync
from controllers.api.community.refounds.serializers.cm_log_serializer import CmB2CLogSerializer
from models.flfact_tpv.objects.eg_logdevolucionesweb_raw import EgLogDevolucionesWeb


class CmB2CRefoundsPost(RecieveSync):

    def __init__(self, params=None):
        super().__init__("cmb2crefounds", params)

    def sync(self):
        data = self.params

        if not data:
            return {"data": {"log": "No se han podido obtener los datos de la devolución"}, "status": 400}

        if "refound" not in data:
            return {"data": {"log": "No se han podido obtener los datos de la devolución"}, "status": 400}

        if "rma_id" not in data["refound"]:
            return {"data": {"log": "No se ha podido obtener el identificador de la devolución."}, "status": 400}

        rma_id = data["refound"]["rma_id"]

        data = self.get_serializer().serialize(data["refound"])

        refound = self.create_model(data)
        refound.save()

        self.log("Éxito", "Devolución {} sincronizado".format(rma_id))
        return {"data": {"log": self.logs}, "status": 200}

    def get_serializer(self):
        return CmB2CLogSerializer()

    def create_model(self, data):
        return EgLogDevolucionesWeb(data)
