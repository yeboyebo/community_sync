from YBLEGACY import qsatype
from YBLEGACY.constantes import *

from controllers.base.default.serializers.default_serializer import DefaultSerializer

class CmPointsSerializer(DefaultSerializer):

    def get_data(self):

        existe_tarjeta = qsatype.FLUtil.sqlSelect("tpv_tarjetaspuntos", "codtarjetapuntos", "codtarjetapuntos = '" + str(self.init_data["codtarjetapuntos"]) + "'")

        if existe_tarjeta:
            raise NameError("La tarjeta " + str(self.init_data["codtarjetapuntos"]) + " ya existe en la BBDD.")
            return False

        self.set_data_value("activa", self.init_data["activa"])
        self.set_string_value("codtarjetapuntos", str(self.init_data["codtarjetapuntos"]))
        self.set_string_value("nombre", str(self.init_data["nombre"]))
        self.set_data_value("sincronizada", self.init_data["sincronizada"])
        self.set_string_value("telefono", str(self.init_data["telefono"]))
        self.set_string_value("codbarrastarjeta", str(self.init_data["codbarrastarjeta"]))
        self.set_string_value("email", str(self.init_data["email"]))
        self.set_string_value("cifnif", str(self.init_data["cifnif"]))
        self.set_string_value("direccion", str(self.init_data["direccion"]))
        self.set_string_value("provincia", str(self.init_data["provincia"]))
        self.set_string_value("ciudad", str(self.init_data["ciudad"]))
        self.set_string_value("codpais", str(self.init_data["codpais"]))

        return True
