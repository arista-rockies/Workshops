import argparse, yaml, csv, json
from dataclasses import dataclass, field

####  TODO: should this have values for non-arista gear?
# this is a dict keyed off the pod number, but that has a dynamic dict of relevant
# substitution values used in format() calls
currentPod = None

parser = argparse.ArgumentParser()
args = None

@dataclass(slots=True, frozen=True)
class Tokens:
    pod: str
    cv: CVToken
    cue: CUEToken
    agni: AGNIToken
    act: ACTToken
    velo: VeloToken

@dataclass(slots=True, frozen=True)
class CVToken:
    server: str
    tenant: str
    key1: str
    key2: str

@dataclass(slots=True, frozen=True)
class CUEToken:
    server: str
    tenant: str
    keyID: str
    key: str

@dataclass(slots=True, frozen=True)
class AGNIToken:
    server: str
    tenant: str
    keyID: str
    key: str
    orgID: str

@dataclass(slots=True, frozen=True)
class ACTToken:
    server: str
    resourceName: str
    key: str
    sshPassword: str

@dataclass(slots=True, frozen=True)
class VeloToken:
    server: str
    tenant: str
    keyID: str
    key: str
    sshPassword: str
    enterpriseID: str
    enterpriseLogicalID: str

@dataclass(slots=True, frozen=True)
class Pod:
    pod: str
    tokens: Tokens
    switches: list[Device]
    substitutions: dict[str, Device]
    velo: list[Device] = field(default_factory=list)

    def __post_init__(self):
        if not self.substitutions:
            super().__setattr__('substitutions', {
                "podStr": f"{self.pod:>02}",
                "podInt": int(self.pod),
                "switches": {}
            })

    def findDeviceByHostname(self, hostname):
        for dev in self.switches:
            if dev.hostname == hostname:
                return dev

        return None

    def findDeviceBySN(self, sn):
        for dev in self.switches:
            if dev.sn == sn:
                return dev

        return None

@dataclass(slots=True)
class Pods:
    pods: dict[str, Pod] = field(default_factory=dict)

    def __getitem__(self, key):
        return self.pods.get(key, None)
    def __setitem__(self, key, value):
        self.pods[key] = value
    def __delitem__(self, key):
        if key in self.pods:
            del(self.pods[key])
    def __iter__(self):
        return iter(self.pods)

    def items(self):
        return self.pods.items()

    def setdefault(self, key, pod):
        return self.pods.setdefault(key, pod)

@dataclass(slots=True, frozen=True)
class Device:
    sn: str = field(hash=True)
    mac: str
    hostname: str
    pod: str
    software: str
    id: str
    model: str
    headers: dict[str, str] = field(default_factory=dict)

def loadConfiguration():
    tokens = loadTokens()

    if args.i != "act":
        config = loadCSVInventory(tokens)
    else:
        config = loadACTInventory(tokens)

    return config

#TODO: FIXME
def loadCSVInventory(tokens):
    result = Pods()

    print(f"loading non-act inventory {args.i}")
    with open(args.i, "r") as f:
        for csvDevice in csv.DictReader(f):
            if csvDevice['Model'][0] not in ['A', 'V']:
                continue

            podStr = csvDevice["CVaaS and CV-CUE Pod Assignment"]
            if podStr not in args.pods:
                continue

            pod = result.setdefault(podStr, Pod(podStr, tokens[podStr], [], []))

            # rather than rewrite the code, i'm taking the lazy path
            device = Device(
                csvDevice["Serial Number"],
                csvDevice["Mac address"],
                csvDevice["Hostname"],
                podStr,
                csvDevice["Software Version"],
                csvDevice.get("ID", csvDevice["Hostname"][csvDevice["Hostname"].rfind("-")+1:]),
                csvDevice.get("Model", "")
            )

            if device.model[0] == 'A':
                pod.switches.append(device)
                pod.substitutions['switches'][device.id] = device
            elif device.model[0] == 'V':
                pod.velo.append(device)

    return result

def loadACTInventory(tokens):
    result = Pods()

    with open("files/actTopology.yml", "r") as f:
        s = f.read()

    for podStr, podToken in tokens.items():
        switches = [] 
        substitutions = {"podInt": int(podStr), "podStr": f"{podStr:>02}", "switches": {}}

        topology = yaml.safe_load(s.replace("###", f"{str(podStr):0>2}"))

        for node in topology.get("nodes", []):
            # because of how the yaml node is set up i have to do this funny
            #  each node should have only one top level, which is the hostname
            for key in node:
                if node[key]["node_type"] != "generic":
                    device = Device(
                        node[key]["serial_number"],
                        node[key]["system_mac_address"],
                        node[key].get("id", key),
                        podStr,
                        node[key].get("version", "") if "version" in node[key] else topology.get("veos", {}).get("version", ""),
                        node[key].get("id", key),
                        node[key]["device_model"]
                    )
                    switches.append(device)
                    substitutions['switches'][device.id] = device

                break

        result[podStr] = Pod(podStr, tokens[podStr], switches, substitutions)

    return result

def loadTokens():
    # we are going to filter the tokens here and just not create the tokens for pods we don't care
    #  about
    result = {}
    with open('tokenConfig.yml', 'r') as f:
        tokenConfig = yaml.safe_load(f.read())
        for podStr, pod in tokenConfig["apiToken"].items():
            if not podStr in args.pods:
                continue

            if (velo := pod.get("velo", None)):
                velo = VeloToken(server=velo.get("server"),
                        tenant=velo.get("tenant"),
                        keyID=velo.get("keyid"),
                        key=velo.get("key"),
                        sshPassword=velo.get("sshPassword"),
                        enterpriseID=velo.get("enterpriseID"),
                        enterpriseLogicalID=velo.get("enterpriseLogicalID")
                )
            if (act := pod.get("act", None)):
                act = ACTToken(server=act.get("server"),
                        resourceName=act.get("resourceName"),
                        key=act.get("key"),
                        sshPassword=act.get("sshPassword")
                )
            if (agni := pod.get("agni", None)):
                agni = AGNIToken(server=agni.get("server"),
                        tenant=agni.get("tenant"),
                        keyID=agni.get("keyid"),
                        key=agni.get("key"),
                        orgID=agni.get("orgid")
                )
            if (cue := pod.get("cue", None)):
                cue = CUEToken(server=cue.get("server"),
                        tenant=cue.get("tenant"),
                        keyID=cue.get("keyid"),
                        key=cue.get("key")
                )
            if (cv := pod.get("cv", None)):
                cv = CVToken(server=cv.get("server"),
                        tenant=cv.get("tenant"),
                        key1=cv.get("key1"),
                        key2=cv.get("key2", cv.get("key1"))
                )

            token = Tokens(
                        pod=pod.get("name", None),
                        cv=cv,
                        cue=cue,
                        agni=agni,
                        act=act,
                        velo=velo
                    )

            result[podStr] = token

    return result
