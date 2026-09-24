import csv, json, yaml, base64, os
from cvprac.cvp_client import CvpClient, json_decoder
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse, Response
from modules.agni import AgniClient
from modules import config
from types import SimpleNamespace
from jinja2 import Environment, FileSystemLoader

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# let's load up the inventory so we know what we are doing:

currentPod = os.getenv("POD")
inventory = os.getenv("INVENTORY")
tokenFile = os.getenv("TOKENFILE")

config.args = SimpleNamespace()
setattr(config.args, "i", inventory)
setattr(config.args, "pods", [currentPod])
setattr(config.args, "tokenFile", tokenFile)

podConfig = config.loadConfiguration()
pod = podConfig[currentPod]

@app.get('/radsec_ca_certificate.pem', response_class=FileResponse)
async def getRadsec(request: Request):
    return FileResponse(path='p12/radsec_ca_certificate.pem')

@app.get('/cert/{sn}', response_class=Response) #FileResponse)
async def getP12(request: Request, sn):
    # if we don't have an agni token, bail early
    if not pod.tokens.agni:
        logger.info("we don't have an agni token.  we should skip this step")
        return Response(content=b"")

    device = pod.findDeviceBySN(sn)

    agniClient = AgniClient(pod)

    nad = agniClient._getNadByMac(device.mac.lower())
    cert = agniClient._generateRadsecCert(nad["id"])

    return Response(content = base64.b64decode(cert['pkcs12Certificate']), media_type="application/pkcs12", headers={"Content-Disposition": "attachment; filename=cert.p12"})

@app.get('/swi/{sn}/{eosVersion}', response_class=FileResponse)
async def getSWI(request: Request, sn, eosVersion):
    device = pod.findDeviceBySN(sn)
    logger.info(f'{device.headers["x-arista-serial"]} desired: {device.software} current: {device.headers["x-arista-softwareversion"]}')
    arch = ""
    if device.headers["x-arista-architecture"] == "i686":
        arch = "64"
    elif device.headers["x-arista-architecture"] == "aarch64":
        arch = "arm"
    fname = f'EOS{arch}-{device.software}.swi'
    if fname != eosVersion:
        raise HTTPException(status_code=404, detail="wrong version")

    return FileResponse(path=f'images/{fname}', filename=fname)

@app.get('/bootstrap.py', response_class=PlainTextResponse)
async def bootstrap(request: Request):
    # Headers({'host': '10.0.96.20:8000', 'accept': '*/*', 'x-arista-systemmac': '2c:dd:e9:f6:f9:9b', 'x-arista-modelname': 'CCS-710P-16P', 'x-arista-serial': 'WTW23490441', 'x-arista-hardwareversion': '11.04', 'x-arista-tpmapi': '2.0', 'x-arista-tpmfwversion': '1.512', 'x-arista-secureztp': 'True', 'x-arista-softwareversion': '4.32.5.1M', 'x-arista-architecture': 'i386'})
    device = pod.findDeviceBySN(request.headers["x-arista-serial"])
    print(f" {currentPod} - {device}")
    if not device:
        print(f'could not find {request.headers["x-arista-serial"]}')
        return

    device.headers.update(request.headers)
    print(device)
    cvpRacClient = CvpClient()
    cvpRacClient.connect(nodes=[pod.tokens.cv.server], username='', password='', is_cvaas=True, api_token=pod.tokens.cv.key1)
    enrollmentToken = cvpRacClient.api.create_enroll_token(duration="900s")

    arch = ""
    if request.headers["x-arista-architecture"] == "i686":
        arch = "64"
    elif request.headers["x-arista-architecture"] == "aarch64":
        arch = "arm"
    fname = f'EOS{arch}-{device.software}.swi'
    print(f'{request.headers["x-arista-serial"]} desired: {device.software} current: {request.headers["x-arista-softwareversion"]}')
    vals = {
            "desiredEOSVersion": fname if request.headers["x-arista-softwareversion"] != device.software else "",
            "enrollmentToken": enrollmentToken["enrollmentToken"]["token"],
            "doAGNI": "True" if pod.tokens.agni else False,
            "cvAddr": pod.tokens.cv.server
    }

    # when a switch requests the bootstrap, we need to make sure it gets onboarded
    #  into agni
    if pod.tokens.agni:
        agniClient = AgniClient(pod)
        nadGroupID = agniClient._getNadGroup("Switches")

        data = {
            "ip": "",
            "mac": device.mac,
            "hostname": device.hostname,
            "sn": device.sn
        }
        device.headers["agni"] = agniClient.onboardSwitch(data, nadGroupID)

    jinjaEnv = Environment(loader=FileSystemLoader('files'))
    template = jinjaEnv.get_template('bootstrap.j2').render(vals)

    return template
