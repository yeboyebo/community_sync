from YBLEGACY import qsatype
import json
from controllers.base.default.controllers.download_sync import DownloadSync
from controllers.api.community.refounds.serializers.cm_refound_serializer import CmRefoundsSerializer

from models.flfact_tpv.objects.cm_refound_raw import CmRefound

class CmB2CRefoundsProcess(DownloadSync):

    def __init__(self, driver, params=None):
        super().__init__("cmb2crefoundsprocess", driver, params)
        self.origin_field = "rma_id"
        self.idlogs = ""
        self.small_sleep = 10
        self.large_sleep = 60
        self.no_sync_sleep = 180

    def get_data(self):
        self.small_sleep = 10
        q = qsatype.FLSqlQuery()
        q.setSelect("idlog, cuerpolog")
        q.setFrom("eg_logdevolucionesweb")
        q.setWhere("website = 'community' AND not procesado AND (estadoprocesado IS NULL OR estadoprocesado = '') AND rma_id IS NOT NULL ORDER BY fechaalta, horaalta LIMIT 10")

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
            datajson = json.loads(str(cuerpolog))
            aData.append(datajson)

        return aData

    def process_data(self, data):
        refound_data = CmRefoundsSerializer().serialize(data)
        if not refound_data:
            return

        refound = CmRefound(refound_data)
        refound.save()

    def after_sync(self):
        success_records = []
        error_records = [refound["rma_id"] for refound in self.error_data]
        after_sync_error_records = []

        for refound in self.success_data:
            try:
                qsatype.FLSqlQuery().execSql("UPDATE eg_logdevolucionesweb SET procesado = true, fechaprocesado = CURRENT_DATE, horaprocesado = CURRENT_TIME, estadoprocesado = 'OK' WHERE idlog IN ({}) AND rma_id = '{}'".format(self.idlogs, refound["rma_id"]))
                success_records.append(refound["rma_id"])
            except Exception as e:
                self.after_sync_error(refound, e)
                after_sync_error_records.append(refound["rma_id"])

        for refound in self.error_data:
            try:
                qsatype.FLSqlQuery().execSql("UPDATE eg_logdevolucionesweb SET procesado = true, fechaprocesado = CURRENT_DATE, horaprocesado = CURRENT_TIME, estadoprocesado = 'ERROR' WHERE idlog IN ({}) AND rma_id = '{}'".format(self.idlogs, refound["rma_id"]))
            except Exception as e:
                self.after_sync_error(refound, e)
                after_sync_error_records.append(refound["rma_id"])

        if success_records:
            self.log("Éxito", "Las siguientes devoluciones se han sincronizado correctamente: {}".format(success_records))

        if error_records:
            self.log("Error", "Las siguientes devoluciones no se han sincronizado correctamente: {}".format(error_records))

        if after_sync_error_records:
            self.log("Error", "Las siguientes devoluciones no se han marcado como sincronizados: {}".format(after_sync_error_records))

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
