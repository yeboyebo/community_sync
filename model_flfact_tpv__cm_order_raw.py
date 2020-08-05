from models.flsyncppal.objects.aqmodel_raw import AQModel

from models.flfact_tpv.objects.cm_orderline_raw import CmOrderLine
from models.flfact_tpv.objects.cm_shippingline_raw import CmShippingLine
from models.flfact_tpv.objects.cm_payment_raw import CmPayment
from models.flfact_tpv.objects.cm_cashcount_raw import CmCashCount
from models.flfact_tpv.objects.egidlecommerce_raw import EgIdlEcommerce
from models.flfact_tpv.objects.egidlecommercedevoluciones_raw import EgIdlEcommerceDevoluciones

class CmOrder(AQModel):

    def __init__(self, init_data, params=None):
        super().__init__("tpv_comandas", init_data, params)

    def get_cursor(self):
        cursor = super().get_cursor()

        cursor.setActivatedCommitActions(False)

        return cursor

    def get_children_data(self):
        for item in self.data["children"]["lines"]:
            self.children.append(CmOrderLine(item))

        self.children.append(CmShippingLine(self.data["children"]["shippingline"]))

        arqueo = CmCashCount(self.data["children"]["cashcount"])
        self.children.append(arqueo)

        for item in self.data["children"]["payments"]:
            self.children.append(CmPayment(item))

        idlEcommerce = EgIdlEcommerce(self.data["children"]["idl_ecommerce"])
        self.children.append(idlEcommerce)

        if "idl_ecommerce_devolucion" in self.data["children"]:
            if self.data["children"]["idl_ecommerce_devolucion"]:
                idlEcommerceDevoluciones = EgIdlEcommerceDevoluciones(self.data["children"]["idl_ecommerce_devolucion"])
                self.children.append(idlEcommerceDevoluciones)
