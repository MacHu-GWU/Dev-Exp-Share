# -*- coding: utf-8 -*-

from rich import print as rprint

recmd_result = [
    {
        "Current Product": "40101-048",
        "Current Prod Desc": "VWR GLOVES LTX CL10 7 CS200PR",
        "Current Price\/Unit": "$2.763",
        "Current GP\/Unit": "$2.337",
        "Recmd Product": "40101-058",
        "Recmd Prod Desc": "VWR GLOVES LTX CL10 10 CS200PR",
        "Recmd Price\/Unit": "$5.526",
        "Recmd GP\/Unit": "$4.674"
    },
    {
        "Current Product": "40101-048",
        "Current Prod Desc": "VWR GLOVES LTX CL10 7 CS200PR",
        "Current Price\/Unit": "$2.763",
        "Current GP\/Unit": "$2.337",
        "Recmd Product": "40101-050",
        "Recmd Prod Desc": "VWR GLOVES LTXCL10 7.5 CS200PR",
        "Recmd Price\/Unit": "$2.907",
        "Recmd GP\/Unit": "$2.481"
    }
]

hil_input = dict()
if len(recmd_result) >= 1:
    hil_input["product"] = {
        "id": recmd_result[0]["Current Product"],
        "description": recmd_result[0]["Current Prod Desc"],
        "price_unit": recmd_result[0]["Current Price/Unit"],
        "gp_unit": recmd_result[0]["Current GP/Unit"],
    }
    hil_input["recommendations"] = list()

    for dct in recmd_result:
        new_dct = {
            "id": dct["Recmd Product"],
            "description": dct["Recmd Prod Desc"],
            "price_unit": dct["Recmd Price/Unit"],
            "gp_unit": dct["Recmd GP/Unit"],
        }
        hil_input["recommendations"].append(new_dct)

    rprint(hil_input)