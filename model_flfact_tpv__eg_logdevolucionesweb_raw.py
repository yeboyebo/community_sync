from models.flsyncppal.objects.aqmodel_raw import AQModel


class EgLogDevolucionesWeb(AQModel):

    def __init__(self, init_data, params=None):
        super().__init__("eg_logdevolucionesweb", init_data, params)
