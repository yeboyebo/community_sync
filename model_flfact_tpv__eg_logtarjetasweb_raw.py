from models.flsyncppal.objects.aqmodel_raw import AQModel


class CmLogPoints(AQModel):

    def __init__(self, init_data, params=None):
        super().__init__("eg_logtarjetasweb", init_data, params)
