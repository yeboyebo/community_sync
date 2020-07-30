from models.flsyncppal.objects.aqmodel_raw import AQModel


class EgLogPedidoWeb(AQModel):

    def __init__(self, init_data, params=None):
        super().__init__("eg_logpedidosweb", init_data, params)
