import json
import requests
import numpy as np
import random

from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel


from km3services._tools import NumpyEncoder


def oscillationprobabilities(
    flavour_in, flavour_out, energies, cos_zeniths, anti_nu=False, params=None
):
    if params is None:
        params = {
            "dm_21": 7.40e-5,
            "dm_31": 2.494e-3,
            "theta_12": 5.868e-1,
            "theta_23": 8.238e-1,
            "theta_13": 1.491e-1,
            "dcp": 4.084070449666731,
        }

    data = {
        "params": params,
        "nus": {
            "flavour_in": flavour_in,
            "flavour_out": flavour_out,
            "energies": energies,
            "cos_zeniths": cos_zeniths,
            "anti_nu": anti_nu,
        },
    }
    r = requests.post(
        "http://131.188.167.67:30000/probabilities",
        data=json.dumps(data, cls=NumpyEncoder),
    )
    if r.ok:
        return np.array(json.loads(r.text))
    else:
        print(f"Error: {r.reason}")
        print(r.text)


# Server part

app = FastAPI()


class OscillationParameters(BaseModel):
    dm_21: float
    dm_31: float
    theta_12: float
    theta_23: float
    theta_13: float
    dcp: float


class _NumpyArray(BaseModel):
    dtype: str
    data: str


def tonumpy(arr: _NumpyArray):
    return np.frombuffer(arr.data)


class _Neutrinos(BaseModel):
    flavour_in: int
    flavour_out: int
    energies: List[float]
    cos_zeniths: List[float]
    anti_nu: bool


@app.post("/numpy")
async def _numpy(array: _NumpyArray):
    return tonumpy(array)


@app.post("/probabilities")
async def _probability(params: OscillationParameters, nus: _Neutrinos):
    import ROOT

    ROOT.gSystem.Load("libOscProb.so")
    pmns = ROOT.OscProb.PMNS_Fast()
    prem = ROOT.OscProb.PremModel()

    pmns.SetDm(2, params.dm_21)  # set delta_m21 in eV^2
    pmns.SetDm(3, params.dm_31)  # set delta_m31 in eV^2
    pmns.SetAngle(1, 2, params.theta_12)  # set Theta12 in radians
    pmns.SetAngle(1, 3, params.theta_13)  # set Theta13 in radians
    pmns.SetAngle(2, 3, params.theta_23)  # set Theta23 in radians
    pmns.SetDelta(1, 3, params.dcp)  # set Delta13 in radians

    return _osc_prob(
        pmns,
        prem,
        nus.flavour_in,
        nus.flavour_out,
        nus.energies,
        nus.cos_zeniths,
        nus.anti_nu,
    )


def _osc_prob(pmns, prem, flav_in, flav_out, energies, cos_zenith, anti_nu=False):
    # true is for antineutrinos, default is false, i.e. neutrinos
    pmns.SetIsNuBar(anti_nu)
    # use a PremModel to make the paths through the earth with the class PremModel
    # chose an angle for the neutrino and fill the paths with cosTheta, e.g. cosTheta = -1 (vertical up-going)
    P = []
    for E, cosZ in zip(energies, cos_zenith):
        prem.FillPath(cosZ)
        pmns.SetPath(prem.GetNuPath())
        P.append(pmns.Prob(flav_in, flav_out, E))
    return P
