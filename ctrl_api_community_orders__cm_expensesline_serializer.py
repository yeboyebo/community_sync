from YBLEGACY.constantes import *

from controllers.api.community.orders.serializers.cm_orderline_serializer import CmOrderLineSerializer


class CmExpensesLineSerializer(CmOrderLineSerializer):

    def get_data(self):
        if not self.init_data["shipping_price"]:
            return False

        iva = self.init_data["iva"]
        if not iva or iva == "":
            iva = 0

        self.set_string_value("codtienda", "AWEB")

        self.set_string_value("referencia", self.get_referencia(), max_characters=18)
        self.set_string_value("descripcion", self.get_descripcion(), max_characters=100)
        self.set_string_value("barcode", self.get_barcode(), max_characters=20)
        self.set_string_value("talla", self.get_talla(), max_characters=50)
        self.set_string_value("color", self.get_color(), max_characters=50)
        self.set_string_value("codimpuesto", self.get_codimpuesto(iva), max_characters=10)

        self.set_string_relation("codcomanda", "codcomanda", max_characters=15)

        self.set_data_value("cantdevuelta", 0)
        self.set_data_value("cantidad", self.get_cantidad())

        self.set_data_value("ivaincluido", True)
        self.set_data_relation("iva", "iva")

        self.set_data_relation("pvpunitarioiva", "shipping_price")
        self.set_data_relation("pvpsindtoiva", "shipping_price")
        self.set_data_relation("pvptotaliva", "shipping_price")

        gastos_sin_iva = self.init_data["shipping_price"]

        if iva and iva != 0:
            gastos_sin_iva = gastos_sin_iva / (1 + (parseFloat(iva) / 100))

        self.set_data_value("pvpunitario", gastos_sin_iva)
        self.set_data_value("pvpsindto", gastos_sin_iva)
        self.set_data_value("pvptotal", gastos_sin_iva)

        return True

    def get_referencia(self):
        return "0000ATEMP00001"

    def get_descripcion(self):
        return "MANIPULACIÓN Y ENVIO"

    def get_barcode(self):
        return "8433613403654"

    def get_talla(self):
        return None

    def get_color(self):
        return None

    def get_cantidad(self):
        return 1
