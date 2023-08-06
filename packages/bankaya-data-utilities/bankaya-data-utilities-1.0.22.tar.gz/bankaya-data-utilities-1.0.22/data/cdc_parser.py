import json
import numpy as np
import datetime as dt
import logging

from .cdc_rules import civilstate, residence


class CDCParser:
    def __init__(self, raw_data):
        # str raw_data to json dict data
        logging.info(f"cdc parser will transform raw_data to dictionary from {raw_data}")
        self.dict_data = json.loads(raw_data)
        logging.info("cdc parser transformed correctly the raw_data to dictionary")
        # getting fields
        self.features = {}
        self.persona()
        self.scores()
        self.empleos()
        self.consultas()
        self.credits()
        logging.info(f"cdc parser completed with features: {self.features}")

    def dt_from_str(self, strng):
        return dt.datetime.strptime(strng, '%Y-%m-%d')

    # parsers
    def persona(self):
        try:
            data = self.dict_data["persona"] if "persona" in self.dict_data["persona"] else None
            if data is not None:
                self.features["lastname1"] = data["apellidoPaterno"] if "apellidoPaterno" in data else None
                self.features["lastname2"] = data["apellidoMaterno"] if "apellidoPaterno" in data else None
                self.features["name"] = data["nombres"] if "nombres" in data else None
                self.features["fullname"] = " ".join([data["nombres"], data["apellidoPaterno"], data["apellidoMaterno"]]) if \
                    "nombres" in data and "apellidoPaterno" in data and "apellidoMaterno" in data else None
                self.features["alive"] = 0 if "fechaDefuncion" in data and data["fechaDefuncion"] != "9999-01-01" else 1
                bdt = self.dt_from_str(data["fechaNacimiento"]) if "fechaNacimiento" in data else None
                if bdt is not None:
                    self.features["age"] = (dt.datetime.now() - bdt) / 365
                    self.features["mbirth"] = bdt.month
                self.features["dependents"] = data["numeroDependientes"] if "numeroDependientes" in data else None
                self.features["residence"] = residence[data["residencia"]] if "residencia" in data else "0"
                self.features["civilstate"] = civilstate[data["estadoCivil"]] if "estadoCivil" in data else "N"
                self.features["rfc"] = data["RFC"] if "RFC" in data else None
                self.features["curp"] = data["CURP"] if "CURP" in data else None
                self.features["nationaity"] = data["nacionalidad"] if "nacionalidad" in data else None
                self.features["socialsecnum"] = data["numeroSeguridadSocial"] if "numeroSeguridadSocial" in data else None
                self.features["gender"] = data["sexo"] if "sexo" in data else None
        except Exception as e:
            logging.exception("exception thrown in CDCParser.persona")

    def scores(self):
        try:
            data = self.dict_data["scores"] if "scores" in self.dict_data else None
            if data is not None:
                self.features["fico"] = -1
                self.features["ficoreasons"] = ""
                for sc in data:
                    if sc["nombreScore"] != "FICO": continue
                    self.features["fico"] = data[0]["valor"] if "valor" in data[0] else None
                    self.features["ficoreasons"] = ",".join(str(v) for v in data[0]["razones"]) if "razones" in data[0] else None
                    break
        except Exception as e:
            logging.exception("exception thrown in CDCParser.scores")

    def empleos(self):
        try:
            data = self.dict_data["empleos"] if "empleos" in self.dict_data else None
            if data is not None:
                self.features["emp_num"] = len(data)
                self.features["emp_states"] = [v["estado"] if "estado" in v else None for v in data]
                self.features["emp_salaries"] = [v["salarioMensual"] if "salarioMensual" in v else None for v in data]
                self.features["emp_postc"] = [v["CP"] if "CP" in v else None for v in data]
                self.features["emp_positions"] = [v["puesto"].lower() if "puesto" in v else None for v in data]
                self.features["emp_durations"] = [
                    (self.dt_from_str(v["fechaUltimoDiaEmpleo"]) - self.dt_from_str(v["fechaContratacion"])).days \
                    if "fechaUltimoDiaEmpleo" in v and "fechaContratacion" in v else None for v in data]
        except Exception as e:
            logging.exception("exception thrown in CDCParser.empleos")

    def consultas(self):
        try:
            data = self.dict_data["consultas"] if "consultas" in self.dict_data else None
            if data is not None:
                self.features["cons_num"] = len(data)
                self.features["cons_dates"] = sorted([self.dt_from_str(v["fechaConsulta"]) if "fechaConsulta" in v else None for v in data])
                self.features["cons_difftimes"] = np.diff(self.features["cons_dates"])
                self.features["cons_services"] = [v["servicios"] if "servicios" in v else None for v in data]
                self.features["cons_responsabilities"] = [v["tipoResponsabilidad"] if "ipoResponsabilidad" in v else None for v in data]
                self.features["cons_creditype"] = [v["tipoCredito"] if "tipoCredito" in v else None for v in data]
                self.features["cons_amount"] = [v["importeCredito"] if "importeCredito" in v else None for v in data]
        except Exception as e:
            logging.exception("exception thrown in CDCParser.consultas")

    def credits(self):
        try:
            data = self.dict_data["creditos"] if "creditos" in self.dict_data else None
            if data is not None:
                self.features["creds_num"] = len(data)
                self.features["creds_debt_amts"] = [v["montoPagar"] if "montoPagar" in v else None for v in data]
                self.features["creds_pay_amts"] = [v["montoUltimoPago"] if "montoUltimoPago" in v else None for v in data]
                self.features["creds_pay_delay"] = [v["saldoVencidoPeorAtraso"] if "montoPagar" in v else None for v in data]
                self.features["creds_pay_done"] = [v["numeroPagos"] if "numeroPagos" in v else None for v in data]
                self.features["creds_pay_report"] = [v["totalPagosReportados"] if "totalPagosReportados" in v else None for v in data]
                self.features["creds_pay_exp"] = [v["numeroPagosVencidos"] if "numeroPagosVencidos" in v else None for v in data]
                self.features["creds_pay_frec"] = [v["frecuenciaPagos"] if "frecuenciaPagos" in v else None for v in data]
                self.features["creds_pay_str"] = [
                    v["historicoPagos"].replace(" ", "").replace("-", "").replace("0", "").replace("V", "0") \
                    if "historicoPagos" in v else "0" \
                    for v in data]
                self.features["creds_debt_amt"] = [v["saldoActual"] if "saldoActual" in v else None for v in data]
                self.features["creds_debt_exp"] = [v["saldoVencido"] if "saldoVencido" in v else None for v in data]
                self.features["creds_curr_delay"] = [int(v["pagoActual"].replace("V", "0")) if "pagoActual" in v else None for v in data if v != "-"]
                self.features["creds_total_delay"] = np.sum(
                    [np.sum([int(w) for w in v.split()]) for v in self.features["creds_pay_str"]])
                self.features["creds_total_debt"] = np.sum([v for v in self.features["creds_debt_amt"]])
                self.features["creds_exp_debt"] = np.sum([v for v in self.features["creds_debt_exp"]])
                self.features["creds_acc_type"] = [v["tipoCuenta"] if "tipoCuenta" in v else None for v in data]
                self.features["creds_gen_delays"] = [v["peorAtraso"] if "peorAtraso" in v else None for v in data]
                self.features["creds_pago_delta"] = [
                    self.dt_from_str(v["fechaUltimoPago"]) - self.dt_from_str(v["fechaAperturaCuenta"]) \
                    if "fechaUltimoPago" in v and "fechaAperturaCuenta" in v else None \
                    for v in data]
                self.features["creds_compra_delta"] = [
                    self.dt_from_str(v["fechaUltimaCompra"]) - self.dt_from_str(v["fechaAperturaCuenta"]) \
                    if "fechaUltimaCompra" in v and "fechaAperturaCuenta" in v else None \
                    for v in data]
        except Exception as e:
            logging.exception("exception thrown in CDCParser.credits")

    def get_features(self):
        return self.features
