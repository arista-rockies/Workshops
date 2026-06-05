#####
#TODO: need to pause setup until devices show up
#TODO: need to cleanup all studios, not just hardcoded studios
#TODO: cleanup access interface configuration studio
#TODO: workspace cleanup
#TODO: we'll need to work with the ztp auto upgrade toggle when bouncing
#        between workshop setups
#TODO: maybe we should import from csv into pgfDevice?
#TODO: need to asyncify everything
#####
#NOTICE: i import modules and use the whole module name, rather than use the from .. import .. syntax
#          this is as designed to ensure that i don't get namespace collisions due to needing so many
#          cv apis

""" example token format
apiToken:
  "0":
      "name": "pod 0"
      "cv":
        "server": "www.arista.io"
        "tenant": "rockies-training-00"
        "key1": "serviceAccountToken1"
        "key2": "serviceAccountToken2"
  "1":
      "name": "pod 1"
      "cv":
        "tenant": "rockies-training-01"
        "key1": "serviceAccountToken1"
        "key2": "serviceAccountToken2"
      "cue":
        "tenant": "Z_ROCKIES-ATD-01"
        "keyid": "cueKeyID"
        "key": "cueKey"
        "url": "https://awm11013-c4.srv.wifi.arista.com/wifi/api/"
      "agni":
        "tenant": "Z_ROCKIES-ATD-01"
        "keyid": "agniKeyID"
        "key": "agniKey"
        "orgid": "agniOrgID"
      "velo":
        "tenant": "Rockies Workshop"
        "key": "velokey"
        "url": "https://veloVCO.com"
"""
import os, argparse, yaml, asyncio, csv, requests, json

from modules import config
config.parser = argparse.ArgumentParser()

### there are a couple of ways to do this.  not sure i like the one i picked
from modules.cue import CueClient
CueClient.configure()

from modules.agni import AgniClient
AgniClient.configure()

from modules.cv import pgfCVClient
pgfCVClient.configure()

from modules.velo import VeloClient
VeloClient.configure()

from modules.pgf import pgfDevice

from requests.packages.urllib3.exceptions import InsecureRequestWarning

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

config.parser.add_argument('-test', default=False, action='store_true', help='testing new code')
config.parser.add_argument('-tokenFile', default="tokenConfig.yml", help="Contains the tokens we should use along with the defined pods")
config.parser.add_argument('-pods', required=True, nargs='+', help='specify a space delimited list of pods to run against, by default all pods will be operated on')

async def main():
    config.args = config.parser.parse_args()
    if config.args.allCleanup:
        config.args.cleanup = True
        config.args.cueCleanup = True

    with open(config.args.tokenFile, "r") as f:
        tokens = yaml.safe_load(f.read())["apiToken"]

    for pod in config.args.pods:
        config.apiTokens[pod] = tokens[pod]

    with open(config.args.i, "r") as f:
        for device in csv.DictReader(f):
            if device['Model'][0] not in ['A', 'V']:
                continue


            # rather than rewrite the code, i'm taking the lazy path
            device["sn"] = device["Serial Number"]
            device["mac"] = device["Mac address"]
            device["hostname"] = device["Hostname"]

            if device['Model'][0] == 'A':
                podNum = int(device["CVaaS and CV-CUE Pod Assignment"][-2:])
                p = config.globalInventory.setdefault(podNum, [])
                p.append(device)
            elif device['Model'][0] == 'V':
                podNum = device["CVaaS and CV-CUE Pod Assignment"]
                device["podNum"] = podNum

                p = config.globalInventory.setdefault('velo', {})[podNum] = device

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    for pod in config.apiTokens:
        config.currentPod = pod
        token = tokens.get(config.currentPod, {})

        if 'cv' in token:
            cvClient = pgfCVClient(token)
            await cvClient.execute()

        if 'cue' in token:
            cueClient = CueClient(token)
            cueClient.execute()

        if 'agni' in token:
            agniClient = AgniClient(token)
            agniClient.execute()

        if 'velo' in token:
            veloClient = VeloClient(token)
            veloClient.execute()

asyncio.run(main())
