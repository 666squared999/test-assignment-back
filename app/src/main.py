from fastapi import FastAPI

from scrapping import rozetka, fozzyshop, novus, auchan, BuckwheatInfo

import utils

app = FastAPI()


@app.get("/buckwheat")
async def bw(wmin: float = None, wmax: float = None, allres: bool = False):
    shops = [{
        'rozetka': await rozetka.parse(),
        'fozzyshop': await fozzyshop.parse(),
        'novus': await novus.parse(),
        'auchan': await auchan.parse(),
    }]

    getf = (lambda bws: bws[:1]) if allres is False else (lambda bws: bws)
    wmin = 0.0 if wmin is None else wmin
    wmax = float('inf') if wmax is None else wmax

    return utils.process(shops, getf=lambda bws: getf(
        [bw for bw in bws if wmin <= bw['weight'] <= wmax]
    ))