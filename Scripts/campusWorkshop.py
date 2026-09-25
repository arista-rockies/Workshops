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
from modules.argparseActions import ParseRangeAction

from requests.packages.urllib3.exceptions import InsecureRequestWarning

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

config.parser.add_argument('-test', default=False, action='store_true', help='testing new code')
config.parser.add_argument('-tokenFile', default="tokenConfig.yml", help="Contains the tokens we should use along with the defined pods")
config.parser.add_argument('-pods', required=True, action=ParseRangeAction, nargs='+', help='specify a space delimited list of pods to run against.  items may also be specified in eos cli style ranges: 1-10,20')
config.parser.add_argument('-i', default="2026CampusWorkshopHardware.csv", help="hardware inventory")
config.parser.add_argument('-type', default='campus', help='type of workshop.  can be campus or cv')

async def main():
    config.args = config.parser.parse_args()

    podConfig = config.loadConfiguration()

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    for podStr, pod in podConfig.items():
        actClient = ActClient(pod)
        actClient.execute()

        agniClient = AgniClient(pod)
        agniClient.execute()

        cueClient = CueClient(pod)
        cueClient.execute()

        cvClient = pgfCVClient(pod)
        await cvClient.execute()

        veloClient = VeloClient(pod)
        veloClient.execute()

asyncio.run(main())
