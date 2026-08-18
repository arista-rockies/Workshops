from modules import config
import requests, argparse, json, yaml, time, paramiko, socks, urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from modules.pgf import pgfAction
from enum import Enum

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class LabState(Enum):
    RUNNING = 2
    STOPPED = 4

class actException(Exception):
    pass

class actConnectException(actException):
    pass

class actOptionsExeption(actException):
    pass

class ActClient():
    def configure():
        def _addArgument(*args, **kwargs):
            if kwargs.get('action', None) == 'store_true':
                kwargs.pop('action')
                kwargs["nargs"] = '?'
                kwargs.setdefault("default", False)
                kwargs.setdefault("const", True)

            config.parser.add_argument(*args, action=pgfAction, module="act", **kwargs) 

        _addArgument('-actProxy', default=None, help='Set a socks proxy. defaults to None')
        _addArgument('-actStartLab', action='store_true', default=False, help='start specified labs')
        _addArgument('-actStopLab', action='store_true', default=False, help='stop specified labs')
        _addArgument('-actUndeployLab', action='store_true', default=False, help='undeploy specified pods')
        _addArgument('-actUpdateTopology', action='store_true', default=False, help='update the topology')
        _addArgument('-actDeployLab', action='store_true', default=False, help='deploy and start the topology')
        _addArgument('-actGetLab', action='store_true', default=False, help='print bootstrap ips')
        _addArgument('-actSetupLinux', action='store_true', default=False, help='configure bootstrap')
        _addArgument('-actUpdateLinux', action='store_true', default=False, help='configure bootstrap')
        _addArgument('-actTest', action='store_true', default=False)
        _addArgument('-actResetBlocks', action='store_true', default=False)
        _addArgument('-actUnblockCampusB', action='store_true', default=False)
        _addArgument('-actUnblockZTR', action='store_true', default=False)
            
    def __init__(self, token):
        self.token = token
        self.apiKey = token["act"]["key"]
        self.baseURL = f'https://{token["act"]["server"]}'

        if config.args.actProxy:
            self.proxies = { "http": f"socks5://{config.args.actProxy}", "https": f"socks5://{config.args.actProxy}" }
        else:
            self.proxies = None

        self.headers = {}
        self.connected = False
        self.topologies = None
        self.labs = None
        self.resourceName = token["act"]["resourceName"]

        self.connect()
        labs = self.getLabs(nameFilter=self.resourceName.format("")) # our filter is a startsWith.  just string substitute empty

    def _findByName(self, lst, name):
        for i in lst:
            if i["name"] == name:
                return i

        return False

    def execute(self):
        if config.args.actTest:
            while True:
                resp = self.waitOnOperation('84af49feafa945738a321a5533db650f', sleep=10, timeout=None, statusChar=".", debug=True)
                print(resp)
                time.sleep(1)

        if config.args.actResetBlocks:
            self._iptables("reset")
            return

        if config.args.actUnblockCampusB:
            self._iptables("unBlockCampusB")
            return

        if config.args.actUnblockZTR:
            self._iptables("unBlockZTR")
            return

        if config.args.actStartLab:
            self.doStartLab()
            return
        if config.args.actStopLab:
            self.doStopLab()
            return
        if config.args.actUndeployLab:
            self.doUndeployLab()
            return
        if config.args.actUpdateTopology:
            self.doUpdateTopology()
            return
        if config.args.actDeployLab:
            self.doDeployAndStart()
            return
        if config.args.actGetLab:
            self.doGetLab()
            return
        if config.args.actUpdateLinux:
            self.doUpdateLinux()
            return
        if config.args.actSetupLinux:
            self.doSetupLinux()
            return

    def connect(self):
        if 'Authorization' not in self.headers:
            self._getToken()

        self.connected = True

    def _getToken(self):
        key = { "api_key": self.apiKey }
        url = f'{self.baseURL}/rest/v1/auth/login'
        resp = requests.post(url, proxies=self.proxies, json=key)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(resp.text)
            print(e)
            raise actConnectException("Not connected, please call the connect method first")

        self.apiKey = resp.json()
        self.headers["Authorization"] = f"Bearer {self.apiKey['token']}"

    def _executeRequest(self, requestType='GET', url=None, data=None, timeout=None):
        if not self.connected:
            raise actConnectException("Not connected, please call the connect method first")

        if not url:
            raise actOptionsExeption("Invalid data for request")

        url = f'{self.baseURL}{url}'
        resp = requests.request(requestType, url, json=data, proxies=self.proxies, headers=self.headers, timeout=timeout)
        resp.raise_for_status()

        return resp.json()

    ############# Topologies calls
    def getTopologies(self, nameFilter=None):
        params = []
        params.append("offset=0")
        params.append("pageSize=100000")
        
        url = f'/rest/v1/topologies?{"&".join(params)}'
        resp = self._executeRequest(url=url)

        if nameFilter == None:
            self.topologies = resp
            return resp

        # there is probably a better way of filering here......
        result = []
        for topology in resp["result"]:
            if nameFilter in topology["name"]:
                result.append(topology)

        self.topologies = result
        return result

    def getTopology(self, id):
        url = f'/rest/v1/topologies/{id}'
        resp = self._executeRequest(url=url)

        #FIXME what do we do if there isn't a topology at that id?
        return resp

    def deleteTopology(self, id):
        url = f'/rest/v1/topologies/{id}'
        resp = self._executeRequest(requestType='DELETE', url=url)

        return resp

    def getTopologyByName(self, name):
        return self._findByName(self.topologies["result"], name)

    def updateTopology(self, id, name, newTopology=None):
        url = f'/rest/v1/topologies/{id}'

        data = { "id": id, "name": name }
        if newTopology:
            data["file"] = newTopology

        resp = self._executeRequest(requestType='PATCH', url=url, data=data)


        return resp

    def createTopology(self, name, newTopology=None):
        url = f'/rest/v1/topologies'

        data = { "name": name, "description": name, "diagram_path": "" }
        if newTopology:
            data["file"] = newTopology

        try:
            resp = self._executeRequest(requestType='POST', url=url, data=data)
        except Exception as e:
            print("error on create topo")
            print(e)

        return resp

    ############# operations calls
    def getOperation(self, id):
        url = f'/rest/v1/operations/{id}'
        resp = self._executeRequest(requestType='GET', url=url)

        return resp

    def waitOnOperation(self, id, sleep=10, timeout=None, statusChar=None, debug=False):
        if debug:
            print(id)
        while True:
            op = self.getOperation(id)
            if debug:
                print(op)

            if op["status"] != "Pending" or timeout == 0:
                if statusChar:
                    print("")
                return op
                break

            time.sleep(sleep)
            if timeout != None:
                timeout -= 1

            if statusChar:
                print(statusChar, end="", flush=True)


    ############# Labs calls
    def getLabs(self, nameFilter=None):
        params = []
        params.append("offset=0")
        params.append("limit=1000")
        
        if nameFilter:
            params.append(f"name={nameFilter}")

        url = f'/rest/v1/labs?{"&".join(params)}'
        resp = self._executeRequest(url=url)

        self.labs = resp["result"]
        return self.labs

        labs = []
        for lab in resp["result"]:
            if nameFilter in lab["name"]:
                labs.append(lab)

        self.labs = labs
        return labs

    def getLabByID(self, id):
        url = f'/rest/v1/labs/{id}'
        resp = self._executeRequest(url=url)

        #FIXME what do we do if there isn't a lab at that id?
        return resp

    def getLabByName(self, name):
        return self._findByName(self.labs, name)

    def deleteLab(self, id):
        url = f'/rest/v1/labs/{id}'
        resp = self._executeRequest(requestType='DELETE', url=url)

        return resp

    def startLab(self, id):
        url = f'/rest/v1/labs/{id}/start'
        resp = self._executeRequest(requestType='POST', url=url)

        return resp

    def stopLab(self, id):
        url = f'/rest/v1/labs/{id}/stop'
        resp = self._executeRequest(requestType='POST', url=url)

        #FIXME does this function return anything?

    def deployLab(self, id, timeout=None):
        url = f'/rest/v1/labs/{id}/deploy'
        resp = self._executeRequest(requestType='POST', url=url, timeout=timeout)

        return resp

    def undeployLab(self, id):
        url = f'/rest/v1/labs/{id}/undeploy'
        resp = self._executeRequest(requestType='POST', url=url)

    def createLab(self, name):
        url = f'/rest/v1/labs'

        data = { "name": name, "description": name, "topology_definition": f'{name}.yml' }
        resp = self._executeRequest(requestType='POST', url=url, data=data)

        return resp

    def doStopLab(self):
        print(f"{config.currentPod} - doStopLab")

        name = self.resourceName.format(config.currentPod)
        lab = self.getLabByName(name)
        if LabState(lab["state"]) == LabState.RUNNING:
            self.stopLab(lab["id"])

    def doStartLab(self):
        print(f"{config.currentPod} - doStartLab")
        name = self.resourceName.format(config.currentPod)
        lab = self.getLabByName(name)
        if LabState(lab["state"]) == LabState.STOPPED:
            res = self.startLab(lab["id"])

    def doUndeployLab(self):
        print(f"{config.currentPod} - doUndeployLab")
        name = self.resourceName.format(config.currentPod)
        lab = self.getLabByName(name)
        self.undeployLab(lab["id"])

    def doDeployAndStart(self):
        try:
            s = ""
            with open("files/actTopology.yml", "r") as f:
                s = f.read()
        except:
            print("  could not deploy and start, terminating")
            return

        # make sure we have the update topologies
        self.getTopologies()

        print(f"{config.currentPod} - doDeployAndStart ")
        name = self.resourceName.format(config.currentPod)

        lab = self.getLabByName(name)
        if lab:
            print(f"  deleting lab {name}", end="", flush=True)
            resp = self.deleteLab(lab["id"])
            resp = self.waitOnOperation(resp["id"], sleep=10, timeout=None, statusChar=".")

        topology = self.getTopologyByName(name)
        if topology:
            print(f"  deleting topology {name}", end="", flush=True)
            resp = self.deleteTopology(topology["id"])
            resp = self.waitOnOperation(resp["id"], sleep=10, timeout=None, statusChar=".")

        newTopology = yaml.safe_load(s.replace("###", f"{config.currentPod:0>2}"))
        try:
            print(f"  creating topology {name}", end="", flush=True)
            resp = self.createTopology(name, newTopology)
            resp = self.waitOnOperation(resp["id"], sleep=10, timeout=None, statusChar=".")
        except Exception as e:
            print(e)
            print("!")
            return None

        # now we instantiate the lab
        print(f"  creating lab {name}", end="", flush=True)
        resp = self.createLab(name)
        resp = self.waitOnOperation(resp["id"], sleep=10, timeout=None, statusChar=",")
        labID = resp["result"]["id"]

        print(f"  deploying lab {name}", end="", flush=True)
        resp = self.deployLab(labID)
        resp = self.waitOnOperation(resp["id"], sleep=10, timeout=None, statusChar='!', debug=True)

    def doUpdateTopology(self):
        try:
            s = ""
            with open("files/actTopology.yml", "r") as f:
                s = f.read()
        except:
            print("  could not update topology, terminating")
            return

        topologies = self.getTopologies()
        name = self.resourceName.format(config.currentPod)
        topology = self._findByName(topologies["result"], name)

        if not topology:
            print(f"did not find topology {name}, continuing")
            return

        print(f"{config.currentPod} - doUpdateTopology ")

        newTopology = yaml.safe_load(s.replace("###", f"{config.currentPod:0>2}"))
        try:

            print(f"  updating topology ", end="", flush=True)
            resp = self.updateTopology(topology["id"], topology["name"], newTopology)

            self.waitOnOperation(resp["id"], sleep=10, timeout=None, statusChar=".")
            print("")
        except Exception as e:
            print(e)
            print("!")
            return

    def doGetLab(self, quiet=False):
        if not quiet:
            print(f"{config.currentPod} - doGetLab ")

        name = self.resourceName.format(config.currentPod)
        lab = self.getLabByName(name)
        if not lab:
            print("could not find lab, skipping")
            return None

        lab = self.getLabByID(lab['id'])
        if not lab.get('devices', None):
            if not quiet:
                print("could not find any devices.  has this lab deployed?")
            return None

        print(LabState(lab["state"]))
        # i want to print out the ip of the bootstrap boxes
        for dev in lab['devices']['generic']:
            if 'bootstrap' in dev['hostname']:
                print(f"{dev['hostname']}: {dev['internal_ip']}")
        return True

    def _setupSSH(self, ip, sshUser, sshPassword):
        # https://stackoverflow.com/questions/47441351/using-paramiko-with-socks-proxy
        sock = None
        if self.proxies:
            s = urllib.parse.urlsplit(self.proxies["http"])
            sock = socks.socksocket()
            sock.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=s.hostname,
                port=s.port
            )
            sock.connect((ip, 22))

        print(f"   connecting to {ip} via ssh")
        pmClient = paramiko.SSHClient()
        pmClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False
        while not connected:
            try:
                pmClient.connect(ip, 22, sshUser, sshPassword, sock=sock)
                connected = True
                print("   connected", flush=True, end="\n")
                return pmClient
            except Exception as e:
                print(".", flush=True, end="")
                time.sleep(1)

        raise Exception(f'could not connect to {ip}')

    def _iptables(self, operation):
        if operation in ["reset", "blockAll", "unBlockAll", "unBlockCampusB", "unBlockZTR"]:
            print(f"{config.currentPod} - {operation}IPTables")
            name = self.resourceName.format(config.currentPod)
            # not sure why getLabByName doesn't return devices but getLabByID does
            lab = self.getLabByName(name)
            l = self.getLabByID(lab["id"])
            if not l.get("devices", None):
                print("could not find any devices in this lab.  has it finished being deployed?")
                return

            # i know the bootstrap box is a generic
            for host in l["devices"]["generic"]:
                if "bootstrap" in host["hostname"]:
                    sshUser = "administrator"
                    sshPassword = self.token["act"]["sshPassword"]
                    pmClient = self._setupSSH(host["internal_ip"], sshUser, sshPassword)

                    pmClient.exec_command(f"sudo bash workshopIPTables.sh {operation}")

    def doSetupLinux(self):
        print(f"{config.currentPod} - doSetupLinux ")
        name = self.resourceName.format(config.currentPod)

        while not self.doGetLab(quiet=True):
            print(".", flush=True, end="")
            time.sleep(10)

        print("", flush=True)

        # not sure why getLabByName doesn't return devices but getLabByID does
        lab = self.getLabByName(name)
        l = self.getLabByID(lab["id"])
        if not l.get("devices", None):
            print("could not find any devices in this lab.  has it finished being deployed?")
            return

        # i know the bootstrap box is a generic
        for host in l["devices"]["generic"]:
            if "bootstrap" in host["hostname"]:
                sshUser = "administrator"
                sshPassword = self.token["act"]["sshPassword"]
                pmClient = self._setupSSH(host["internal_ip"], sshUser, sshPassword)

                scp = pmClient.open_sftp()
                scp.put('tokenConfig.yml', '/home/administrator/tokenConfig.yml')
                scp.put('setupACTGateway.sh', '/home/administrator/setupACTGateway.sh')
                scp.put('workshopIPTables.sh', '/home/administrator/workshopIPTables.sh')
                scp.chmod('/home/administrator/setupACTGateway.sh', 0o700)
                scp.chmod('/home/administrator/workshopIPTables.sh', 0o700)

                pmClient.exec_command("sudo setenforce Permissive")
                stdin, stdout, stderr = pmClient.exec_command("sudo -S /home/administrator/setupACTGateway.sh", get_pty=True)

                # if we don't read the redirects then the con will terminate and stop the script
                for line in iter(stdout.readline, ""):
                    print(line, end="")

                pmClient.close()

    def doUpdateLinux(self):
        print(f"{config.currentPod} - doUpdateLinux ")
        name = self.resourceName.format(config.currentPod)

        while not self.doGetLab(quiet=True):
            print(".", flush=True, end="")
            time.sleep(10)

        print("", flush=True)

        # not sure why getLabByName doesn't return devices but getLabByID does
        lab = self.getLabByName(name)
        l = self.getLabByID(lab["id"])
        if not l.get("devices", None):
            print("could not find any devices in this lab.  has it finished being deployed?")
            return

        # i know the bootstrap box is a generic
        for host in l["devices"]["generic"]:
            if "bootstrap" in host["hostname"]:
                sshUser = "administrator"
                sshPassword = self.token["act"]["sshPassword"]
                pmClient = self._setupSSH(host["internal_ip"], sshUser, sshPassword)

                stdin, stdout, stderr = pmClient.exec_command("cd Projects/Workshops/Scripts/ && git pull && sudo systemctl restart bootstrap", get_pty=True)

                # if we don't read the redirects then the con will terminate and stop the script
                for line in iter(stdout.readline, ""):
                    print(line, end="")

                pmClient.close()
