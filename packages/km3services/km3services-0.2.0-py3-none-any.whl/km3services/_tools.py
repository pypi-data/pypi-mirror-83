import json
import requests
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """

    def default(self, obj):
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {"real": obj.real, "imag": obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)):
            return None

        return json.JSONEncoder.default(self, obj)


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
