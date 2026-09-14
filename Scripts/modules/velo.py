# TODO:  add create profile
# TODO:  unhardcode the SN
# TODO:  unhardcode the activation key
# TODO:  unhardcode the vco address
# TODO:  async'ify
# TODO: need to move some things to the datamodel to clean this up a bit
import requests, json, time, ipaddress, uuid, nmcli, time, paramiko
from modules import config
from modules import veloDataModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from nmcli._exception import NotExistException
from modules.pgf import pgfAction, pgfBoolAction

# *very* basic velo client
class VeloClient():
    def configure():
        def _addArgument(*args, **kwargs):
            if kwargs.get('action', None) == 'store_true':
                kwargs.pop('action')
                kwargs.setdefault("default", False)
                config.parser.add_argument(*args, action=pgfBoolAction, module="velo", **kwargs)
            else:
                config.parser.add_argument(*args, action=pgfAction, module="velo", **kwargs)

        config.parser.set_defaults(velo=False)

        _addArgument('-veloCleanup', default=False, action='store_true', help='do velo cleanup steps')
        _addArgument('-veloReconfigure', default=False, action='store_true', help='reconfigure the velo for lag')
        _addArgument('-veloSetup', default=False, action='store_true', help='do velo setup steps')
        _addArgument('-veloDump', default=False, action='store_true', help='do some test dumps')
        _addArgument('-veloTest', default=False, action='store_true', help='do velo test code')

    def __init__(self, token):
        if not (t:=token.get("velo", None)):
            raise Exception("invalid token")

        # let's pull some information out of the global inventory
        d = config.globalInventory['velo'][config.currentPod]
        self.serialNumber = d["sn"]
        self.pod = d["Hostname"] #d["podNum"]

        self.token = t
        self.baseURL = f'https://{t["url"]}'
        self._connected = False
        self.headers = {"Content-Type": "application/json", "Authorization": f"Token {t['key']}"}
        self.edge = {}
        self._actionCounter = 0
        self._debug = False

        self._authenticate()
        self._getEdgeBySerial()

        if not self._connected:
            raise Exception("authentication to velo failed")

    def actionCounter(self):
        self._actionCounter += 1
        return self._actionCounter

    def _authenticate(self) -> bool:
        self._connected = True

        d = self._doPortal(method='/enterprise/getEnterprise')
        if not d:
            self._connected = False
            return

        self.eID = d["logicalId"]
        self.enterprise = d["id"]

    def _doPortal(self, method: str=None, data=None) -> dict():
        if not self._connected:
            return

        if not data:
            data = {}

        #data["enterpriseId"] = self.enterprise

        url = f'{self.baseURL}/portal/rest{method}'
        resp = requests.post(url, json=data, headers=self.headers)
        if self._debug:
            print(f' ----------- {method} -------')
            print(json.dumps(resp.json(), indent=2))
            print(f' ----------------------------')

        return resp.json()

    def _doAction(self, method: str=None, url='portal', params=None) -> dict():
        if not self._connected:
            return

        if not params:
            params = {}

        params["enterpriseID"] = self.enterprise

        data = {
            "id": self.actionCounter(),
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }

        url = f'{self.baseURL}/{url}/'
        resp = requests.post(url, json=data, headers=self.headers)
        if self._debug:
            print(f' ----------- {method} -------')
            print(json.dumps(data, indent=2))
            print("**")
            print(json.dumps(resp.json(), indent=2))
            print(f' ----------------------------')
        return resp.json()

    def _getEdgeBySerial(self):
        # get edge doesn't support filtering by serial so we have to do this the dumb way
        allEdges = self._doPortal(method='/enterprise/getEnterpriseEdgeList')
        for edge in allEdges:
            if edge['serialNumber'] == self.serialNumber:
                self.edge = edge
                return

    def _getEdgeByName(self):
        self.edge = self._doPortal(method='/edge/getEdge', data={"name": self.pod})

    def _getLicenses(self):
        self.licenses = self._doPortal(method='/license/getEnterpriseEdgeLicenses')

    def _findInList(self, lst, name):
        for l in lst:
            if l["name"] == name:
                return l
        return {}
    def _getConfiguration(self, name):
        self._getConfigurations()
        return self._findInList(self.configurations, name)

    def _getConfigurations(self):
        self.configurations = self._doPortal(method='/enterprise/getEnterpriseConfigurations')

    def deactivateEdge(self):
        print(f"{config.currentPod} - deactivate")

        # to cleanup/reset the device to gold the easiets method is to deactivate it.  do to this
        #  we need to use some undocumented api calls

        # first we need to request that we go into live mode passing in our device id
        params = {
            "id": self.edge["id"],
        }

        print(f"{config.currentPod} - deactivate - enterLiveMode")
        resp = self._doAction('liveMode/enterLiveMode', params=params)

        # that will return to us a token
        deactivateToken = resp["result"]["token"]
        url = resp["result"]["url"]

        # which we pass into the actions
        params = {
            "actions": [
                {
                    "action": "hardReset",
                    "parameters": {},
                }
            ],
            "token": deactivateToken
        }
        print(f"{config.currentPod} - deactivate - reset")
        resp = self._doAction('liveMode/requestLiveActions', url=url, params=params)

        # lastly let's leave live mode.  dunno if this is strictly required, but the ui does it
        params = {
            "token": deactivateToken
        }

        print(f"{config.currentPod} - deactivate - exitLiveMode")
        self._doAction('liveMode/clientExitLiveMode', url=url, params=params)

    def deleteEdge(self, wait=False, timeout=120):
        # i cannot delete a connected edge, i must wait for it to disconnect
        if wait:
            while timeout>0:
                self._getEdgeBySerial()
                if not self.edge["edgeState"] in ["OFFLINE", "DEGRADED", "NEVER_ACTIVATED"]:
                    print(f'.', flush=True, end='')
                    #print(f'.{self.edge["edgeState"]}', flush=True, end='')
                    #await asyncio.sleep(1)
                    time.sleep(1)
                    timeout -= 1
                else:
                    break

            print("", flush=True, end='\n')
        print(f"{config.currentPod} - deleteEdge")
        data = {
            "id": self.edge["id"]
        }
        self._doPortal('/edge/deleteEdge', data=data)
        
    def cleanup(self):
        if "id" not in self.edge:
            print(f"{config.currentPod} - skipping cleanup, device not found")
            return

        self.deactivateEdge()
        self.deleteEdge(wait=True)

    def provisionEdge(self):
        def _addLink(ar, interface, name, logicalID, privateNetName):
            privateNet = self._findInList(privateNetworks, privateNetName)

            internalID = str(uuid.uuid4())

            ar.append({
                "interfaces": [ interface ],
                "staticSLA": {
                    "latencyMs": "0",
                    "jitterMs": "0",
                    "lossPct": "0"
                },
                "classesOfService": {
                    "classId": None,
                    "classesOfService": []
                },
                "description":"",
                "logicalId": logicalID,
                "internalId": internalID,
                "discovery": "USER_DEFINED",
                "addressingVersion": "IPv4",
                "mode": "PRIVATE",
                "type": "WIRED",
                "name": name,
                "isp": "",
                "publicIpAddress": "",
                "sourceIpAddress": "",
                "nextHopIpAddress": "",
                "customVlanId": False,
                "vlanId": 2,
                "enable8021P": False,
                "priority8021P": 0,
                "virtualIpAddress": "",
                "dynamicBwAdjustmentEnabled": False,
                "bwMeasurement": "STATIC",
                "upstreamMbps": "",
                "downstreamMbps": "",
                "backupOnly": False,
                "udpHolePunching": False,
                "overheadBytes": 0,
                "MTU": 1500,
                "dscpTag": "",
                "staticSlaEnabled": False,
                "classesofServiceEnabled": False,
                "strictIpPrecedence": False,
                "encryptOverlay": True,
                "privateNetwork": {
                    "id": len(ar)+1,
                    "logicalId": privateNet["logicalId"],
                    "ref": "wan:privateNetwork",
                    "enterpriseObjectId": privateNet["id"]
                },
                "lastActive": "",
                "hotStandby": False,
                "minActiveLinks": 1,
                "pmtudDisabled": False,
                "orchestratorServiceReachable": True,
                "orchestratorServiceReachableBackup": True,
            })

        print(f"{config.currentPod} - provisionEdge")

        self._getLicenses()
        edgeConfig = self._getConfiguration('Workshop-Branch')

        # do the provision
        data = {
            "analyticsMode": "SDWAN_ONLY",
            "configurationId": edgeConfig["id"], #str ??
            "edgeLicenseId": self.licenses[0]["id"], #int ??
            "endpointPkiMode": "CERTIFICATE_OPTIONAL",
            "haEnabled": False,
            "modelNumber": "edge710",
            "name": self.pod,
            "serialNumber": self.serialNumber,
            "site": {
                "contactEmail": "pfelt@arista.com",
                "contactName": "pfelt@arista.com",
                "shippingSamAsLocation": 1 #int?
            }
        }
        if not config.args.veloReconfigure:
            activationKey = self._doPortal('/edge/edgeProvision', data=data)

        self._getEdgeBySerial()

        self._debug = config.args.veloDump
        segments = self._doPortal(method='/enterprise/getEnterpriseNetworkSegments')
        stack = self._doPortal(method='/edge/getEdgeConfigurationStack', data={"edgeId":self.edge["id"]})
        gwHandoff = self._doPortal(method='/enterprise/getEnterpriseGatewayHandoff')
        serviceLic = self._doPortal(method='/service/getEnterpriseServiceLicense')
        services = self._doPortal(method='/enterprise/getEnterpriseServices')
        costs = self._doPortal(method='/enterprise/getEnterpriseDistributedCostCalculation')
        nsdPolicy = self._doPortal(method='/enterprise/getEnterpriseUseNSDPolicy')
        analyticsPolicy = self._doPortal(method='/enterprise/getAnalyticsConfiguration')
        privateNetworks = self._doPortal(method='/enterprise/getEnterprisePrivateNetworks')
        self._debug = False

        deviceModule = None
        wanModule = None
        for m in stack[0]["modules"]:
            if m["name"] == 'deviceSettings':
                deviceModule = m
            elif m["name"] == 'WAN':
                wanModule = m

        if not deviceModule or not wanModule:
            raise Exception("could not find device settings!")

        # let's override some crap in the module data to set up the 4 ge
        newRoutedInterfaces = []
        for interface in deviceModule["data"]["routedInterfaces"]:
            # not a huge fan of this logic
            if interface["name"] in ["GE1", "GE2"]:
                newInterface = veloDataModel.veloBaseRoutedInterface(interface["name"])
                if config.args.veloReconfigure:
                    # we want these interfaces to be in the lag.  set it up!
                    newInterface.setLagSlave()
                else:
                    base = "240" if interface["name"] == "GE1" else "248"
                    newInterface.setL3(f"10.0.{100+int(config.currentPod)}.{base}/29")

                newRoutedInterfaces.append(newInterface.interface)
            elif interface["name"] == "LAG1":
                newInterface = veloDataModel.veloBaseRoutedInterface("LAG1")
                newInterface.setLag([])
                if config.args.veloReconfigure:
                    newInterface.setLag([{"name":"GE1"},{"name": "GE2"}])
                    newInterface.setL3(f"10.0.{100+int(config.currentPod)}.0/25")

                newRoutedInterfaces.append(newInterface.interface)
            elif interface["name"] == "LAG2":
                newInterface = veloDataModel.veloBaseRoutedInterface("LAG2")
                newInterface.setLag([])
                if config.args.veloReconfigure:
                    newInterface.setDisabled()

                newRoutedInterfaces.append(newInterface.interface)
            else:
                # all other interfaces, leave as they are
                newRoutedInterfaces.append(interface)

        deviceModule["data"]["routedInterfaces"] = newRoutedInterfaces
                
        data = {
            "configurationId": stack[0]["id"],
            "id": deviceModule["id"],
            "returnData": True,
            "_update": {
                "name": "deviceSettings",
                "description": None,
                "refs": {
                    "deviceSettings:segment": [
                        {
                            "configurationId": stack[0]["id"],
                            "enterpriseObjectId": segments[0]["id"],
                            "logicalId": segments[0]["logicalId"],
                            "moduleId": deviceModule["id"],
                            "ref": "deviceSettings:segment"
                        }
                    ],
                },
                "data": deviceModule["data"]
            },            
        }
        self._debug = False
        self._doAction(method='configuration/updateConfigurationModule', params=data)
        self._debug = False

        data["id"] = wanModule["id"]
        data["_update"]["name"] = "WAN"
        data["_update"]["refs"] = None
        data["_update"]["data"] = {"links": []}

        logicalID = str(uuid.uuid4())

        _addLink(data["_update"]["data"]["links"], "GE3", "isp1", logicalID, "WAN 1")
        _addLink(data["_update"]["data"]["links"], "GE4", "isp2", logicalID, "WAN 2")

        self._debug = False
        self._doAction(method='configuration/updateConfigurationModule', params=data)
        self._debug = False

        if not config.args.veloReconfigure:
            self.activate(activationKey["activationKey"])

    def activate(self, activationKey):
        print(f"{config.currentPod} - activating edge")
        ssid = f"velocloud-{self.serialNumber[-3:]}"
        url = f'http://192.168.2.1/?activation_key={activationKey}&custom_vco={self.token["url"]}'
        print(f"  connecting to ssid: {ssid}")
        connected = False
        while not connected:
            try:
                nmcli.connection.down(ssid)
                nmcli.connection.delete(ssid)
            #except NotExistException:
                #print(f"  we don't appear to have a wifi nic.  exiting without activating.  hit the following url in a browser: {url}")
                ## we don't have a wifi nic.  just exit
                #return
            except:
                # i'm not really interested on if there is a problem
                #  and trying to resolve something
                pass

            try:
                nmcli.device.wifi_connect(ssid, 'vcsecret')
                connected = True
                print("   connected\n   starting activation", flush=True, end="\n")
            except:
                time.sleep(1)
                print(".", flush=True, end="")

        # now that we are connected, let's do the activate
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
        driver.get(url)

        success = driver.find_element(By.ID, 'success-dialog')
        update = driver.find_element(By.ID, 'activation-requires-download')

        print("  waiting for the activation to complete")
        while success.value_of_css_property("display") == "none" and update.value_of_css_property("display") == "none":
            print('.', flush=True, end="")
            time.sleep(1)

            success = driver.find_element(By.ID, 'success-dialog')
            update = driver.find_element(By.ID, 'activation-requires-download')

        print("   completed", flush=True, end="\n")
        nmcli.connection.down(ssid)
        nmcli.connection.delete(ssid)

        sshServer = f'10.1.{100+int(config.currentPod)}.2'
        print(f"   connecting to {sshServer} via ssh")
        sshUser = "root"
        sshPassword = self.token["sshPassword"].format(self.serialNumber[-3:])

        pmClient = paramiko.SSHClient()
        pmClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False
        while not connected:
            try:
                pmClient.connect(sshServer, 22, sshUser, sshPassword)
                connected = True
                print("   connected", flush=True, end="\n")
            except:
                print(".", flush=True, end="")
                time.sleep(1)

        print("  installing lldp")
        scp = pmClient.open_sftp()
        scp.put('files/lldpd_1.0.18-r3_x86_64.ipk', '/root/lldpd_1.0.18-r3_x86_64.ipk')

        pmClient.exec_command("opkg install --force-reinstall lldpd_1.0.18-r3_x86_64.ipk")
        print("  done")

    def setup(self):
        self._getEdgeBySerial()

        if "id" in self.edge:
            print(f"{config.currentPod} - skipping provision, device already there")
            return

        self.provisionEdge()

    def execute(self):
        if config.args.veloTest:
            print("inside veloTest")

        if config.args.veloDump:
            self._getEdgeBySerial()
            print(f'{self.edge}')
            return

        if config.args.veloCleanup:
            self.cleanup()

        if config.args.veloSetup:
            self.setup()

        if config.args.veloReconfigure:
            self.provisionEdge()
