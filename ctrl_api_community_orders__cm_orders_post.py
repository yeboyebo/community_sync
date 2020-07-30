from controllers.base.default.controllers.recieve_sync import RecieveSync
from controllers.api.community.orders.serializers.cm_orders_serializer import CmB2COrdersSerializer
from models.flfact_tpv.objects.eg_logpedidosweb_raw import EgLogPedidoWeb


class CmB2COrdersPost(RecieveSync):

    def __init__(self, params=None):
        super().__init__("cmb2corders", params)

    def sync(self):
        data = self.params

        if not data:
            return {"data": {"log": "No se han podido obtener los datos del pedido"}, "status": 400}

        if "order" not in data:
            return {"data": {"log": "No se han podido obtener los datos del pedido"}, "status": 400}

        if "increment_id" not in data["order"]:
            return {"data": {"log": "No se ha podido obtener el identificador del pedido"}, "status": 400}

        increment = data["order"]["increment_id"]

        data = self.get_serializer().serialize(data["order"])

        order = self.create_model(data)
        order.save()

        self.log("Éxito", "Pedido {} sincronizado".format(increment))
        return {"data": {"log": self.logs}, "status": 200}

    def get_serializer(self):
        return CmB2COrdersSerializer()

    def create_model(self, data):
        return EgLogPedidoWeb(data)
