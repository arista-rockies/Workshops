import argparse, yaml, csv

# not a huge fan, but i'm out of time
def findDeviceBySerial(deviceInventory, sn):
    for device in deviceInventory:
        if device["sn"] == sn:
            return device
    return None

def findDeviceByName(self, deviceInventory, hostname):
    for device in deviceInventory:
        if device["hostname"] == hostname:
            return device
    return None

def loadInventory():
    if args.i != "act":
        print(f"loading non-act inventory {args.i}")
        with open(args.i, "r") as f:
            for device in csv.DictReader(f):
                if device['Model'][0] not in ['A', 'V']:
                    continue

                # rather than rewrite the code, i'm taking the lazy path
                device["sn"] = device["Serial Number"]
                device["mac"] = device["Mac address"]
                device["hostname"] = device["Hostname"]
                device["software"] = device["Software Version"]
                device["id"] = device.get("ID", device["Hostname"])
                device["model"] = device.get("Model", "")

                if device['Model'][0] == 'A':
                    podNum = device["CVaaS and CV-CUE Pod Assignment"][-2:]
                    device["pod"] = podNum

                    p = globalInventory.setdefault(podNum, [])
                    p.append(device)

                    subs = globalSubstitutions.setdefault(podNum, {"podInt": int(podNum), "podStr": str(podNum)})
                    subs[f'{device["hostname"]}_Serial'] = device["sn"]
                    subs[f'{device["hostname"]}_Hostname'] = device["hostname"]

                elif device['Model'][0] == 'V':
                    podNum = device["CVaaS and CV-CUE Pod Assignment"]
                    device["podNum"] = podNum

                p = globalInventory.setdefault('velo', {})[podNum] = device
    elif args.i == "act":
        with open("files/actTopology.yml", "r") as f:
            s = f.read()

        for pod in apiTokens:
            p = globalInventory.setdefault(pod, [])
            subs = globalSubstitutions.setdefault(pod, {})
            topology = yaml.safe_load(s.replace("###", f"{str(pod):0>2}"))

            for node in topology.get("nodes", []):
                # because of how the yaml node is set up i have to do this funny
                #  each node should have only one top level, which is the hostname
                for key in node:
                    if node[key]["node_type"] != "generic":
                        device = {
                            "sn": node[key]["serial_number"],
                            "mac": node[key]["system_mac_address"],
                            "hostname": node[key].get("id", key),
                            "pod": pod,
                            "software": node[key].get("version", "") if "version" in node[key] else topology.get("veos", {}).get("version", ""),
                            "id": node[key].get("id", key),
                            "model": node[key]["device_model"]
                        }
                        p.append(device)

                        subs = globalSubstitutions.setdefault(pod, {"podInt": int(pod), "podStr": str(pod)})
                        subs[f'{device["id"]}_Serial'] = device["sn"]
                        subs[f'{device["id"]}_Hostname'] = device["hostname"]

                    break

####  TODO: should this have values for non-arista gear?
# this is a dict keyed off the pod number, but that has a dynamic dict of relevant
# substitution values used in format() calls
globalSubstitutions = {}

globalInventory = {}
apiTokens = {}
currentPod = None

parser = argparse.ArgumentParser()
args = None
