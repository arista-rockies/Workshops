import tempfile, argparse
from modules import config
from cloudvision.Connector.grpc_client import GRPCClient, create_query

import json

# this is a convenience class to set a 3rd variable to true, allowing
#  us to figure out if we have any options set for a given module.
#  this makes spawning the clients smarter
class pgfAction(argparse.Action):
    def __init__(self, option_strings, dest, module=None, **kwargs):
        if module == None:
            raise ValueError("must specify a module")
        super().__init__(option_strings, dest, **kwargs)
        self.module = module

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        setattr(namespace, self.module, True)

class pgfInterface():
    _name: str
    _peer: dict

    def __init__(self, interfaceName: str):
        self._name = interfaceName
        self._peer = None

    def addPeer(self, peerName: str, peerInterface: str):
        self._peer = {}
        self._peer["name"] = peerName
        self._peer["interface"] = peerInterface

    def get(self, sn):
        res = {
            "inputs": {},
            "tags": {
                "query": f"interface:{self._name}@{sn}"
            }
        }
        if self._peer:
            res["inputs"] = {
                "interface": {
                    "neighborDeviceId": self._peer["name"],
                    "neighborInterfaceName": self._peer["interface"]
                }
            }

        return res

class pgfDevice():
    _sn: str
    _model: str
    _mac: str
    _hostname: str
    _interfaces: dict

    def __init__(self, sn: str, model: str, mac: str, hostname: str, tok: str, token: dict[str]):
        self._sn = sn
        self._model = model
        self._mac = mac
        self._hostname = hostname
        self._interfaces = {}
        self.tok = tok
        self.token = token

    def __str__(self):
        res = {
            "inputs": {
                "device": {
                    "hostname": self._hostname,
                    "macAddress": self._mac,
                    "modelName": self._model,
                    "interfaces": []
                }
            },
            "tags": {
                "query": f"device:{self._sn}"
            }
        }
        for interfaceName, interface in self._interfaces.items():
            res["inputs"]["device"]["interfaces"].append(interface.get(self._sn))

        return json.dumps(res)

    def fetchInterfaces(self):
        fp = tempfile.NamedTemporaryFile(mode="w")
        fp.write(self.tok)
        fp.flush()

        with GRPCClient(self.token["server"], token=fp.name) as client:
            path = ["Sysdb", "interface", "status", "all", "intfStatus"]
            query = [ create_query([(path, [])], self._sn) ]
            for batch in client.get(query):
                for notif in batch["notifications"]:
                    for interface in notif["updates"]:
                        self.addInterface(interface)

        fp.close()

    def addInterface(self, interfaceName: str):
        self._interfaces[interfaceName] = pgfInterface(interfaceName)

    def addPeer(self, interfaceName: str, peerName: str, peerInterface: str):
        self._interfaces[interfaceName].addPeer(peerName, peerInterface)

