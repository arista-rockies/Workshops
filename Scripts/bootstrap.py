import csv, json, yaml, base64
from cvprac.cvp_client import CvpClient, json_decoder
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse, Response
from modules.agni import AgniClient

app = FastAPI()

# let's load up the inventory so we know what we are doing:

globalInventory = {}
try:
    with open("2026CampusWorkshopHardware.csv", "r") as f:
        for device in csv.DictReader(f):
            globalInventory[device["Serial Number"]] = device
            device["pod"] = int(device["CVaaS and CV-CUE Pod Assignment"][-2:])
except FileNotFoundError:
    pass

# we need to load and parse the token file
with open("tokenConfig.yml", "r") as f:
    tokens = yaml.safe_load(f.read())["apiToken"]

@app.get('/radsec_ca_certificate.pem', response_class=FileResponse)
async def getRadsec(request: Request):
    return FileResponse(path='p12/radsec_ca_certificate.pem')

@app.get('/cert/{sn}', response_class=Response) #FileResponse)
async def getP12(request: Request, sn):
    device = globalInventory[sn]

    token = tokens[str(device["pod"])]
    agniClient = AgniClient(token)

    nad = agniClient._getNadByMac(device['Mac address'].lower())
    cert = agniClient._generateRadsecCert(nad["id"])

    #cert = io.StringIO(device["agni"]["certificate"])

    return Response(content = base64.b64decode(cert['pkcs12Certificate']), media_type="application/pkcs12", headers={"Content-Disposition": "attachment; filename=cert.p12"})
    return FileResponse(path=f'p12/{fname}', filename=fname)

@app.get('/swi/{sn}/{eosVersion}', response_class=FileResponse)
async def getSWI(request: Request, sn, eosVersion):
    device = globalInventory[sn]
    arch = ""
    if device["headers"]["x-arista-architecture"] == "i686":
        arch = "64"
    elif device["headers"]["x-arista-architecture"] == "aarch64":
        arch = "arm"
    fname = f'EOS{arch}-{device["Software Version"]}.swi'
    if fname != eosVersion:
        raise HTTPException(status_code=404, detail="wrong version")

    return FileResponse(path=f'images/{fname}', filename=fname)

@app.get('/bootstrap.py', response_class=PlainTextResponse)
async def bootstrap(request: Request):
    # Headers({'host': '10.0.96.20:8000', 'accept': '*/*', 'x-arista-systemmac': '2c:dd:e9:f6:f9:9b', 'x-arista-modelname': 'CCS-710P-16P', 'x-arista-serial': 'WTW23490441', 'x-arista-hardwareversion': '11.04', 'x-arista-tpmapi': '2.0', 'x-arista-tpmfwversion': '1.512', 'x-arista-secureztp': 'True', 'x-arista-softwareversion': '4.32.5.1M', 'x-arista-architecture': 'i386'})
    device = globalInventory.get(request.headers["x-arista-serial"], None)
    if not device:
        # we didn't find this in the global inventory.  maybe we can parse the info we want out of the serial itself?
        #  we'll bet on the SN starting with P## and try that.  this is, by far, not a robust way to do this:
        sn = request.headers["x-arista-serial"]
        device = {
            "pod": sn[1:sn.find("-")],
            "Software Version": request.headers["x-arista-softwareversion"],
            "Mac address": request.headers["x-arista-systemmac"],
            "Hostname": sn,
            "Serial Number": sn
        }
    token = tokens[str(device["pod"])]

    cvpRacClient = CvpClient()
    cvpRacClient.connect(nodes=[token["cv"]["server"]], username='', password='', is_cvaas=True, api_token=token["cv"]["key1"])
    enrollmentToken = cvpRacClient.api.create_enroll_token(duration="900s")

    arch = ""
    if request.headers["x-arista-architecture"] == "i686":
        arch = "64"
    elif request.headers["x-arista-architecture"] == "aarch64":
        arch = "arm"
    fname = f'EOS{arch}-{device["Software Version"]}.swi'
    vals = {
            "desiredEOSVersion": fname if request.headers["x-arista-softwareversion"] != device["Software Version"] else "",
            "enrollmentToken": enrollmentToken["enrollmentToken"]["token"],
            "doAGNI": "True" if "agni" in token else False,
            "cvAddr": token["cv"]["server"]
    }

    # when a switch requests the bootstrap, we need to make sure it gets onboarded
    #  into agni
    if "agni" in token:
        agniClient = AgniClient(token)
        nadGroupID = agniClient._getNadGroup("Switches")

        data = {
            "ip": "",
            "mac": device['Mac address'],
            "hostname": device['Hostname'],
            "sn": device['Serial Number']
        }
        device["agni"] = agniClient.onboardSwitch(data, nadGroupID)
        device["headers"] = request.headers

    with open(f'files/bootstrap.txt', 'r') as f:
        return f.read().format(**vals)

    #print(request.headers)
    #print(request.url)
    raise HTTPException(status_code=503, detail="terminating")
