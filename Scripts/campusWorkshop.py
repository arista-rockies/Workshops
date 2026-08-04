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
      "act":
        "server": "ce.act.arista.com"
        "key": "actKey"
        "sshPassword": ""
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
        "sshPassword": "formatStringOfPassword"
      "act":
        "server": "ce.act.arista.com"
        "key": "actKey"
        "sshPassword": ""
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

from modules.act import ActClient
ActClient.configure()

from modules.pgf import pgfDevice

from requests.packages.urllib3.exceptions import InsecureRequestWarning

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

config.parser.add_argument('-test', default=False, action='store_true', help='testing new code')
config.parser.add_argument('-tokenFile', default="tokenConfig.yml", help="Contains the tokens we should use along with the defined pods")
config.parser.add_argument('-pods', required=True, nargs='+', help='specify a space delimited list of pods to run against, by default all pods will be operated on')
config.parser.add_argument('-i', default="2026CampusWorkshopHardware.csv", help="hardware inventory")
config.parser.add_argument('-type', default='campus', help='type of workshop.  can be campus or cv')

async def main():
    config.args = config.parser.parse_args()

    with open(config.args.tokenFile, "r") as f:
        tokens = yaml.safe_load(f.read())["apiToken"]

    for pod in config.args.pods:
        config.apiTokens[pod] = tokens[pod]

    config.loadInventory()

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    for pod in config.apiTokens:
        config.currentPod = pod
        token = tokens.get(config.currentPod, {})

        if hasattr(config.args, 'act'):
            if not 'act' in token:
                print("no act token provided, but act actions requested.  skipping")
            else:
                actClient = ActClient(token)
                actClient.execute()

        if hasattr(config.args, 'agni'):
            if not 'agni' in token:
                print("no agni token provided, but agni actions requested.  skipping")
            else:
                agniClient = AgniClient(token)
                agniClient.execute()

        if hasattr(config.args, 'cue'):
            if not 'cue' in token:
                print("no cue token provided, but cue actions requested.  skipping")
            else:
                cueClient = CueClient(token)
                cueClient.execute()

        if hasattr(config.args, 'cv'):
            if not 'cv' in token:
                print("no cv token provided, but cv actions requested.  skipping")
            else:
                cvClient = pgfCVClient(token)
                await cvClient.execute()

        if hasattr(config.args, 'velo'):
            if not 'velo' in token:
                print("no velo token provided, but velo actions requested.  skipping")
            else:
                veloClient = VeloClient(token)
                veloClient.execute()

asyncio.run(main())
