from YBLEGACY import qsatype

from controllers.base.default.serializers.default_serializer import DefaultSerializer

class CmB2CLogSerializer(DefaultSerializer):

    def get_data(self):
        now = str(qsatype.Date())
 
        email = str(self.init_data["email"])
        start_date = now[:10]
        start_time = now[-(8):]
        self.set_string_value("fechaalta", start_date)
        self.set_string_value("horaalta", start_time)
        self.set_string_value("email", str(email))
        self.set_string_value("website", "community")

        self.data["cuerpolog"] = str(self.init_data).replace("'", "\"")

        return True
