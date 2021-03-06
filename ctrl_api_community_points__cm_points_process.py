from YBLEGACY import qsatype
import json
from controllers.base.default.controllers.download_sync import DownloadSync
from controllers.api.community.points.serializers.cm_points_serializer import CmPointsSerializer

from models.flfact_tpv.objects.cm_points_raw import CmPoints

class CmB2CPointsProcess(DownloadSync):

    def __init__(self, driver, params=None):
        super().__init__("cmb2cpointsprocess", driver, params)
        self.origin_field = "email"
        self.idlogs = ""
        self.small_sleep = 10
        self.large_sleep = 60
        self.no_sync_sleep = 180

    def get_data(self):
        q = qsatype.FLSqlQuery()
        q.setSelect("idlog,cuerpolog")
        q.setFrom("eg_logtarjetasweb")
        q.setWhere("website = 'community' AND not procesado AND (estadoprocesado IS NULL OR estadoprocesado = '') ORDER BY fechaalta, horaalta LIMIT 1")

        q.exec_()

        if not q.size():
            self.small_sleep = 60
            return []

        body = self.fetch_query(q)
        aData = []

        for row in body:

            if self.idlogs == "":
                self.idlogs = str(row['idlog'])
            else:
                self.idlogs += "," + str(row['idlog'])

            cuerpolog = row['cuerpolog']
            cuerpolog = cuerpolog.replace("None", "\"None\"")
            cuerpolog = cuerpolog.replace("'", "\"")
            cuerpolog = cuerpolog.replace("False", "\"False\"")
            cuerpolog = cuerpolog.replace("True", "\"True\"")
            datajson = json.loads(str(cuerpolog))

            aData.append(datajson)

        return aData

    def process_data(self, data):

        points_data = CmPointsSerializer().serialize(data)

        if not points_data:
            return

        points = CmPoints(points_data)

        points.save()

    def after_sync(self):
        success_records = []
        error_records = [tarjeta["email"] for tarjeta in self.error_data]
        after_sync_error_records = []

        for tarjeta in self.success_data:
            try:
                qsatype.FLSqlQuery().execSql("UPDATE eg_logtarjetasweb SET procesado = true, fechaprocesado = CURRENT_DATE, horaprocesado = CURRENT_TIME, estadoprocesado = 'OK' WHERE idlog IN ({}) AND email = '{}'".format(self.idlogs, tarjeta["email"]))
                success_records.append(tarjeta["email"])
            except Exception as e:
                self.after_sync_error(tarjeta, e)
                after_sync_error_records.append(tarjeta["email"])

        for tarjeta in self.error_data:
            try:
                qsatype.FLSqlQuery().execSql("UPDATE eg_logtarjetasweb SET procesado = true, fechaprocesado = CURRENT_DATE, horaprocesado = CURRENT_TIME, estadoprocesado = 'ERROR' WHERE idlog IN ({}) AND email = '{}'".format(self.idlogs, tarjeta["email"]))
            except Exception as e:
                self.after_sync_error(tarjeta, e)
                after_sync_error_records.append(tarjeta["email"])

        if success_records:
            self.log("Éxito", "Las siguientes tarjetas se han sincronizado correctamente: {}".format(success_records))

        if error_records:
            self.log("Error", "Las siguientes tarjetas no se han sincronizado correctamente: {}".format(error_records))

        if after_sync_error_records:
            self.log("Error", "Las siguientes tarjetas no se han marcado como sincronizados: {}".format(after_sync_error_records))

        d = qsatype.Date()
        if not qsatype.FactoriaModulos.get("formtpv_tiendas").iface.marcaFechaSincroTienda("AWEB", "VENTAS_TPV", d):
            return False

        return self.small_sleep

    def fetch_query(self, q):

        field_list = [field.strip() for field in q.select().split(",")]
        rows = []
        while q.next():
            row = {field: q.value(field) for (field) in field_list}
            rows.append(row)

        return rows
