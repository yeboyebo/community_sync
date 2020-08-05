from YBLEGACY import qsatype

from controllers.base.default.serializers.default_serializer import DefaultSerializer

class CmB2CLogSerializer(DefaultSerializer):

    def get_data(self):
        now = str(qsatype.Date())

        increment = str(self.init_data["increment_id"])
        codigo = "WEB{}".format(qsatype.FactoriaModulos.get("flfactppal").iface.cerosIzquierda(increment, 9))

        start_date = now[:10]
        start_time = now[-(8):]

        self.set_string_value("fechaalta", start_date)
        self.set_string_value("horaalta", start_time)
        self.set_string_value("cuerpolog", str(self.init_data).replace("'", "\""))
        self.set_string_value("codcomanda", codigo)
        self.set_string_value("website", "community")

        return True
