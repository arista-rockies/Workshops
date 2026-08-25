from modules import config
from modules import pgf
import uuid, requests, time, yaml, tempfile
from requests_toolbelt import MultipartEncoder
from modules.pgf import pgfAction
from os.path import basename

#######
from cvprac.cvp_client import CvpClient, json_decoder
#######
from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector.codec.custom_types import FrozenDict
from cloudvision.Connector.codec import Wildcard, Path
import json
#######
import pyavd, asyncio, pyavd._cv.client
import pyavd._cv.api.arista.studio.v1
import pyavd._cv.api.fmp
import pyavd._cv.api.arista.tag.v2
import pyavd._cv.api.arista.workspace.v1
import pyavd._cv.api.arista.time
import pyavd._cv.api.arista.changecontrol.v1
import pyavd._cv.api.arista.alert.v1
#######
from modules.sync_cc_templates import (
    getCcTemplates,
    getCcActionBundles,
    getCcPath,
    getCcPathVersions,
    publish,
)

class pgfCVClient():
    def configure():
        def _addArgument(*args, **kwargs):
            if kwargs.get('action', None) == 'store_true':
                kwargs.pop('action')
                kwargs["nargs"] = '?'
                kwargs.setdefault("default", False)
                kwargs.setdefault("const", True)

            config.parser.add_argument(*args, action=pgfAction, module="cv", **kwargs)

        _addArgument('-cvCleanup', default=False, action='store_true', help='do cleanup steps')
        _addArgument('-cvSetup', default=False, action='store_true', help='do setup steps')

        _addArgument('-cvCleanupNotifiers', default=False, action='store_true', help='only cleanup the event system')
        _addArgument('-cvThirdParty', default='', help='comma delimited list of 3rd party devices to configure')
        _addArgument('-cvTest', default=False, action='store_true', help='dev code')
        _addArgument('-cvAddAdmins', default='', nargs='+', help='space separated list of email address of new admin users')
        _addArgument('-cvAddImages', default='', nargs='+', help='space separated list of swi images to upload')
        _addArgument('-cvAddPackages', default=False, action='store_true', help='this option is only required for alraedy provisioned pods and will add the required packages.  these steps are automatically done on pods as they are provisioned moving forward')
        _addArgument('-cvAddCCStuff', default=False, action='store_true', help='this option is only required for already provisioned pods and will add actionBundles and ccTemplates only.  these steps are automatically done on pods as they are provisioned moving forward')

    def __init__(self, token):
        self.token = token
        self.tok = token["cv"]["key1"]
        self.tok2 = token["cv"].get("key2", self.tok)
        self.server = token["cv"]["server"]
        self.baseURL = f'https://{self.server}'

    # not a huge fan, but i'm out of time
    def findDeviceBySerial(self, deviceInventory, sn):
        for device in deviceInventory:
            if device["sn"] == sn:
                return device
        return None

    def findDeviceByName(self, deviceInventory, hostname):
        for device in deviceInventory:
            if device["hostname"] == hostname:
                return device
        return None


    async def scsCleanup(self, c, workspaceID):
        print(f"{config.currentPod} - scsCleanup")
        # cleanup here is a bit of a mess because we can't just use the configlet rapi
        #  we need to use the studios api too
        rootContainers = await c.get_studio_inputs(studio_id='studio-static-configlet', workspace_id=workspaceID)

        # let's loop over the array of roots and delete them
        if not rootContainers:
            print("there doesn't seem to be any scs config, skipping")
            return

        for containerID in rootContainers["configletAssignmentRoots"]:
            await c.delete_configlet_container(
                workspace_id=workspaceID,
                assignment_id=containerID
            )

        await c.set_studio_inputs(studio_id='studio-static-configlet', workspace_id=workspaceID, inputs={"configletAssignmentRoots": []})

        # delete all the configlets
        configlets = await c.get_configlets(workspace_id=workspaceID, configlet_ids=[])
        for configlet in configlets:
            #print(configlet.key.configlet_id)
            await c.delete_configlets(workspace_id=workspaceID, configlet_ids=[configlet.key.configlet_id])
        ###################### scs cleanup ####################

    async def inventoryCleanup(self, c, workspaceID):
        print(f"{config.currentPod} - inventoryCleanup")
        topologyInventory = await c.set_studio_inputs(studio_id="TOPOLOGY", workspace_id=workspaceID, inputs={'devices': []})

    async def tagsCleanup(self, c, workspaceID):
        print(f"{config.currentPod} - tagsCleanup")
        # first let's unassign all tags from both interfaces and devices
        tagAssignments = await c.get_tag_assignments(workspace_id=workspaceID, creator_type="user")

        for tag in tagAssignments:
            eType = "device" if tag.key.element_type == pyavd._cv.api.arista.tag.v2.ElementType.DEVICE else "interface"

            t = (tag.key.label, tag.key.value, tag.key.device_id, tag.key.interface_id)
            await c.delete_tag_assignments(
                workspace_id=workspaceID,
                tag_assignments=[t],
                element_type=eType)

        # now we can get all tags and delete them
        tags = await c.get_tags(workspace_id=workspaceID, creator_type="user")

        request = pyavd._cv.api.arista.tag.v2.TagConfigSetSomeRequest(values=[])
        for tag in tags:
            request.values.append(
                    pyavd._cv.api.arista.tag.v2.TagConfig(
                        key=pyavd._cv.api.arista.tag.v2.TagKey(
                            workspace_id=workspaceID,
                            element_type=tag.key.element_type,
                            label=tag.key.label,
                            value=tag.key.value
                        ),
                        remove=True
                    )
                )

        if len(request.values) > 0:
            inputKeys = []
            client = pyavd._cv.api.arista.tag.v2.TagConfigServiceStub(c._channel)
            responses = client.set_some(request, metadata=c._metadata, timeout=300)
            async for response in responses:
                inputKeys.append(response.key)

    async def onboardDevices(self, c, cvpRacClient, workspaceID, deviceInventory):
        # for this iteration of the workshop we are only onboarding leaf1a
        print(f"{config.currentPod} - onboardDevices")
        deviceList = {}
        devices = cvpRacClient.api.get_inventory()

        for device in devices:
            d = self.findDeviceBySerial(deviceInventory, device["serialNumber"])
            if not d:
                continue
            if d["hostname"] != f"campus-pod{config.currentPod:0>2}-leaf1a":
                continue

            newDevice = pgf.pgfDevice(device["serialNumber"], device["modelName"], device["systemMacAddress"], d["hostname"], self.tok, self.token["cv"])
            newDevice.fetchInterfaces()

            deviceList[device["serialNumber"]] = newDevice

            # because the topology api is currently broken, we need to hardcode the links
            #   this is specific out our workshop layout an is hardcoded
            #newDevice.addPeer("Ethernet1", "pimac", "eth0")
            newDevice.addPeer("Ethernet9", "d4:e5:c9:06:2f:0b", "Ge1")
            #newDevice.addPeer("Ethernet14",
            #newDevice.addPeer("Ethernet15",
            #newDevice.addPeer("Ethernet16",

        data = {
            "partialEqFilter": [
                {
                    "key": {
                        "workspaceId": workspaceID,
                        "studioId": "TOPOLOGY"
                    }
                }
            ]
        }

        # because the topology api is currently broken, we need to hardcode all the links
        if False:
            url = f'{self.baseURL}/api/resources/topology/v1/Edge/all'
            resp = requests.get(url, json=data, verify=False, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})

            edges = json_decoder(resp.text)
            for edge in edges:
                print(f"**********\n{edge}\n*********")
                left = deviceList.get(edge["result"]["value"]["key"]["from"], None)
                right = deviceList.get(edge["result"]["value"]["key"]["to"], None)
                for individualEdge in edge["result"]["value"].get("lldpLinks", {}).get("values", []):
                    lPort = individualEdge["key"]["srcPort"]
                    rPort = individualEdge["key"]["dstPort"]
                    if left:
                        left.addPeer(lPort, edge["result"]["value"]["key"]["to"], rPort)
                    if right:
                        right.addPeer(rPort, edge["result"]["value"]["key"]["from"], lPort)

        # now pull the current inputs from the studio
        request = pyavd._cv.api.arista.studio.v1.InputsConfigSetSomeRequest(values=[])

        topologyInventory = await c.get_studio_inputs(studio_id="TOPOLOGY", workspace_id=workspaceID)
        #for deviceIndex, device in enumerate(topologyInventory.get("devices", [])):
            #print(device)
            #pass

        idx = 0
        for deviceName, device in deviceList.items():
            request.values.append(
                pyavd._cv.api.arista.studio.v1.InputsConfig(
                    key=pyavd._cv.api.arista.studio.v1.InputsKey(
                        studio_id="TOPOLOGY",
                        workspace_id=workspaceID,
                        path=pyavd._cv.api.fmp.RepeatedString(values=["devices", str(idx)]),
                    ),
                    inputs = f"{device}"
                )
            )
            idx+=1

        inputKeys = []
        client = pyavd._cv.api.arista.studio.v1.InputsConfigServiceStub(c._channel)
        responses = client.set_some(request, metadata=c._metadata, timeout=300)
        async for response in responses:
            inputKeys.append(response.key)

    async def assignTags(self, c, workspaceID, deviceInventory):
        print(f"{config.currentPod} - assignTags")
        leaf1a = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1a")
        leaf1b = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1b")

        if not leaf1a or not leaf1b:
            raise Exception("could not find leaf1a or leaf1b in deviceInventory")

        tags = [
            ("Campus", f"Workshop"),
            ("Campus-Pod", f"IT-Bldg"),
            ("Access-Pod", f"IDF1"),
            ("Role", "Leaf"),
        ]
        tagAssignments = [
            ("Campus", f"Workshop", leaf1a["sn"],  None),
            ("Campus-Pod", f"IT-Bldg", leaf1a["sn"],  None),
            ("Access-Pod", f"IDF1", leaf1a["sn"],  None),
            ("Role", "Leaf", leaf1a["sn"],  None),
        ]
        # assign tags
        await c.set_tags(workspaceID, tags, "device", 300)
        await c.set_tag_assignments(workspaceID, tagAssignments, "device", 300)

    async def scsSetup(self, c, workspaceID, deviceInventory):
        print(f"{config.currentPod} - scsSetup")
        #configletContainers = await c.get_configlet_containers(workspace_id=workspaceID)
        #print(configletContainers)
        #return

        ###################### scs upload ####################
        leaf1a = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1a")
        leaf1b = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1b")

        if not leaf1a or not leaf1b:
            raise Exception("couldn't find leaf1a or leaf1b in deviceInventory")
        
        configlets = [
            {
                "filename": "Studios-campus-global-config.txt",
                "configletName": f"Studios-campus-pod{config.currentPod}-global-config",
                "container": "Device",
                "query": "device: *",
                "children": None
            },{
                "filename": "Studios-campus-radsec-config.txt",
                "configletName": f"Studios-campus-pod{config.currentPod}-radsec-config",
                "container": None,
                "query": None,
                "children": None
            }
        ]

        vals = {
            "podStr": f"{config.currentPod:0>2}",
            "podInt": int(config.currentPod)+100
        }
        for configlet in configlets:
            configletID = configlet["configletName"]

            f = open(f"files/campusConfiglets/{configlet['filename']}", "r")
            configletText = f.read().format(**vals)

            await c.set_configlet(
                workspace_id=workspaceID,
                configlet_id=configletID,
                display_name=configletID,
                description=configletID,
                body=configletText
            )

            if configlet["container"]:
                # let's create the assignment
                await c.set_configlet_container(
                        workspace_id=workspaceID,
                        container_id=configlet["container"],
                        display_name=configlet["container"],
                        description=configlet["container"],
                        configlet_ids=[configletID],
                        child_assignment_ids=configlet["children"],
                        query=configlet["query"],
                )
        await c.set_studio_inputs(studio_id='studio-static-configlet', workspace_id=workspaceID, inputs={"configletAssignmentRoots": ["Device"]})

        ###################### sms upload ####################
    async def smsSetup(self, c, workspaceID, deviceInventory):
        print(f"{config.currentPod} - smsStudioSetup")

        leaf1a = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1a")

        if not leaf1a:
            raise Exception("could not find leaf1a or leaf1b in deviceInventory")

        vals = {
            "leaf1": leaf1a["sn"],
        }
        f = open("files/campusWorkshop_softwareManagementInputs.txt", "r")
        smsStudio = yaml.safe_load(f.read().format(**vals))
        smsStudioID = "studio-software-management"
        await c.set_studio_inputs(
                studio_id=smsStudioID,
                workspace_id=workspaceID,
                inputs=smsStudio["inputs"])

        ###################### scs upload ####################

    async def aicStudioSetup(self, c, workspaceID, deviceInventory):
        print(f"{config.currentPod} - aicStudioSetup")

        #### to make this work you need to
        ####  replace {} as {{}}
        ####  replace serial references
        ####  replace pod number references in queries
        ####  replace pod number references in vlan ids

        leaf1a = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1a")

        if not leaf1a:
            raise Exception("could not find leaf1a or leaf1b in deviceInventory")

        vals = {
            "podStr": config.currentPod,
            "podInt": 100+int(config.currentPod),
            "leaf1a": leaf1a["sn"],
        }
        f = open("files/campusWorkshop_aicInputs.txt", "r")
        aicStudio = yaml.safe_load(f.read().format(**vals))

        aicStudioID = "studio-campus-access-interfaces"
        await c.set_studio_inputs(
            studio_id=aicStudioID,
            workspace_id=workspaceID,
            inputs=aicStudio["inputs"])

    async def campusStudioSetup(self, c, workspaceID, deviceInventory):
        print(f"{config.currentPod} - campusStudioSetup")
        #with open("files/campusWorkshop_campusFabricInputs.yml", "r") as f:
                #campusStudio = yaml.safe_load(f.read())

        #### to make this work you need to
        ####  replace {} as {{}}
        ####  replace serial references
        ####  replace pod number references in queries
        ####  replace pod number references in vlan ids

        leaf1a = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1a")
        leaf1b = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1b")

        if not leaf1a or not leaf1b:
            raise Exception("could not find leaf1a or leaf1b in deviceInventory")

        vals = {
            "podStr": config.currentPod,
            "podInt": 100+int(config.currentPod),
            "leaf1": leaf1a["sn"],
            "leaf2": leaf1b["sn"]
        }
        f = open("files/campusWorkshop_campusFabricInputs.txt", "r")
        campusStudio = yaml.safe_load(f.read().format(**vals))

        #  if there are third-party devices, register them
        #  this is horrible code
        t = campusStudio["inputs"]["campus"][0]["inputs"]["campusDetails"]["campusPod"][0]["inputs"]["campusPodFacts"]["thirdPartyDevices"]
        cnt = 1
        for device in config.args.cvThirdParty.split(','):
            t.append({
                "hostname": f"campus-spine{cnt}",
                "identifier": device,
                "nodeId": cnt,
                "role": "spine"
            })
            cnt += 1

        campusStudioID = "studio-avd-campus-fabric"
        await c.set_studio_inputs(
            studio_id=campusStudioID,
            workspace_id=workspaceID,
            inputs=campusStudio["inputs"])

    async def studioCleanup(self, c, workspaceID, studioID):
        print(f"{config.currentPod} - studioCleanup({studioID})")
        await c.set_studio_inputs(studio_id=studioID, workspace_id=workspaceID, inputs={})

    async def buildAndSubmitWorkspace(self, c, workspaceID, expectCC=True):
        print(f"{config.currentPod} - buildAndSubmit")
        result = await c.build_workspace(workspaceID)
        print("building workspace")
        buildResult, workspace = await c.wait_for_workspace_response(workspaceID, result.request_params.request_id)
        if buildResult.status != 1: # SUCCESS
            raise Exception(f"build failed for pod: {config.currentPod} {workspaceID}: {buildResult.status}")

        result = await c.submit_workspace(workspaceID, force=True)
        print("submitting workspace")
        submitResult, workspace = await c.wait_for_workspace_response(workspaceID, result.request_params.request_id)

        if submitResult.status != 1: #SUCCESS
            raise Exception(f"submit failed for pod: {config.currentPod} {workspaceID}: {submitResult.status}")

        #there is a better way to do this......
        if expectCC:
            return workspace.cc_ids.values[0]
        else:
            return

    async def executeChangeControl(self, c, ccID, wait=True):
        print(f"{config.currentPod} - executeChangeControl")
        # now that we were a success let's execute the cc
        changeControl = await c.get_change_control(change_control_id=ccID)

        result = await c.approve_change_control(
                change_control_id=ccID,
                timestamp=changeControl.change.time
        )

        result = await c.start_change_control(change_control_id=ccID)

        if wait:
            result = await c.wait_for_change_control_state(cc_id=ccID, state="completed")
            if result.status != 2: #SUCCESS
                raise Exception("cc didn't complete properly.")

    async def workspacesCleanup(self, c):
        request = pyavd._cv.api.arista.workspace.v1.WorkspaceStreamRequest(
            partial_eq_filter=[],
            time=pyavd._cv.api.arista.time.TimeBounds(start=None, end=None)
        )
        client = pyavd._cv.api.arista.workspace.v1.WorkspaceServiceStub(c._channel)

        try:
            responses = client.get_all(request, metadata=c._metadata, timeout=10.0)
            workspaces = [ response.value async for response in responses ]
        except Exception as e:
            raise Exception("eeror")

        print(workspaces)
        pass

    async def unprovisionDevicesCV(self, c, cvpRacClient, deviceInventory):
        print(f"{config.currentPod} - unprovisionDevices")
        #finishedCCID = "EdIgccX4e84nQanTqu731"
        #finishedChangeControl = await c.get_change_control(change_control_id=finishedCCID)

        with open("files/campusWorkshopDecomTemplate.txt", "r") as f:
            newCC = f.read()

        ccID = str(uuid.uuid4())
        rootID = str(uuid.uuid4())

        rootStage = {
            "name": "Change 2024-08-09-13-25-12 Root",
            "rows": {
                "values": [
                    {
                        "values": [ ]
                    }
                ]
            }
        }

        cc = {
            "key": { "id": ccID },
            "change": {
                "name": "finished",
                "rootStageId": rootID,
                "stages": {
                    "values": {
                        rootID: rootStage
                    }
                },
                "notes": ""
            }
        }

        stages = {}
        devices = cvpRacClient.api.get_inventory(provisioned=False)
        for device in devices:
            deviceStageID = str(uuid.uuid4())
            stages[deviceStageID] = {
                "name": "Enter ZTP",
                "action": {
                    "name": "enterZTP",
                    "timeout": 120,
                    "args": {
                        "values": {
                            "DeviceID": device["serialNumber"]
                        }
                    }
                },
                "rows": {}
            }
            rootStage["rows"]["values"][0]["values"].append(deviceStageID)
        
        cc["change"]["stages"]["values"].update(stages)

        url = f'{self.baseURL}/api/resources/changecontrol/v1/ChangeControlConfig'
        resp = requests.post(url, json=cc, verify=False, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})
        try:
            resp.raise_for_status()

            # from here on out, let's reconnect with the second token
            #  this allows for us to complete even if four-eyes is set
            c = pyavd._cv.client.CVClient(self.server, token=self.tok2)
            c._connect()
            print("executing the ztp change control")
            await self.executeChangeControl(c, ccID, wait=False)

            print("sleeping for 2m to hopefully give ztp time to kick in")
            time.sleep(120)
        except:
            # if we get an exception here, it's likely we didn't get any cc out of the submission.
            #  this is probably a valid scenario
            pass

        # we can now do the actual decom in cv
        devices = cvpRacClient.api.get_inventory(provisioned=False)
        for device in devices:
            print(f"decomming {device['hostname']}")
            cvpRacClient.api.device_decommissioning(device["serialNumber"], str(uuid.uuid4()))

    async def unprovisionDevicesCampus(self, c, cvpRacClient, deviceInventory):
        print(f"{config.currentPod} - unprovisionDevices")
        #finishedCCID = "EdIgccX4e84nQanTqu731"
        #finishedChangeControl = await c.get_change_control(change_control_id=finishedCCID)

        with open("files/campusWorkshopDecomTemplate.txt", "r") as f:
            newCC = f.read()

        leaf1aStageUUID = str(uuid.uuid4())
        leaf1a = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1a")
        leaf1bStageUUID = str(uuid.uuid4())
        leaf1b = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1b")
        #leaf1cStageUUID = str(uuid.uuid4())
        #leaf1c = self.findDeviceByName(deviceInventory, f"campus-pod{config.currentPod:0>2}-leaf1c")

        ccID = str(uuid.uuid4())
        vals = {
            "ccID": ccID,
            "rootID": str(uuid.uuid4()),
            "leaf1aStage": str(uuid.uuid4()),
            "leaf1bStage": str(uuid.uuid4()),
            #"leaf1cStage": str(uuid.uuid4()),
            "leaf1aSN": leaf1a["sn"],
            "leaf1bSN": leaf1b["sn"],
            #"leaf1cSN": leaf1c["sn"]
        }
        cc = json.loads(newCC.format(**vals))

        url = f'{self.baseURL}/api/resources/changecontrol/v1/ChangeControlConfig'
        resp = requests.post(url, json=cc, verify=False, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})
        resp.raise_for_status()

        # from here on out, let's reconnect with the second token
        #  this allows for us to complete even if four-eyes is set
        c = pyavd._cv.client.CVClient(self.server, token=self.tok2)
        c._connect()
        print("executing the ztp change control")
        await self.executeChangeControl(c, ccID, wait=False)

        print("sleeping for 2m to hopefully give ztp time to kick in")
        time.sleep(120)

        devices = cvpRacClient.api.get_inventory(provisioned=False)
        for device in devices:
            print(f"decomming {device['hostname']}")
            cvpRacClient.api.device_decommissioning(device["serialNumber"], str(uuid.uuid4()))

    async def notificationReceiverCleanup(self, c):
        print(f"{config.currentPod} - notificationReceiver")
        request = pyavd._cv.api.arista.alert.v1.AlertConfigStreamRequest()
        client = pyavd._cv.api.arista.alert.v1.AlertConfigServiceStub(c._channel)

        try:
            responses = await client.get_one(request, metadata=c._metadata, timeout=10.0)
        except:
            raise Exception("eeror")

        newRequest = pyavd._cv.api.arista.alert.v1.AlertConfigSetRequest(
            value=pyavd._cv.api.arista.alert.v1.AlertConfig(
                settings=pyavd._cv.api.arista.alert.v1.Settings(
                    slack=pyavd._cv.api.arista.alert.v1.SlackSettings(),
                    gchat=pyavd._cv.api.arista.alert.v1.GoogleChatSettings()
                ),
                rules=pyavd._cv.api.arista.alert.v1.Rules(values=[]),
                broadcast_groups=pyavd._cv.api.arista.alert.v1.BroadcastGroups(values={})
            )
        )
        await client.set(newRequest, metadata=c._metadata, timeout=10.0)

    async def deleteDevices(self, client):
        return
        print(f"{config.currentPod} - deleteDevices")
        devices = client.api.get_inventory(provisioned=False)

        for device in devices:
            res = client.api.reset_device('cleanup', device)
            print(device)
            print(res)
            for task in res.get('data', {}).get('taskIds', []):
                res = client.api.execute_task(task)
                print(res)
            print("****")

        time.sleep(60)
        for device in devices:
            client.api.device_decommissioning(device["serialNumber"], str(uuid.uuid4()))

    async def createRootPath(self, client, path):
        ccPtrs = getCcPath(client)
        if path not in list(ccPtrs.keys()):
            pathElts = ["changecontrol"]
            ptrData = {path: Path(keys=["changecontrol", path])}
            publish(client, 'cvp', pathElts, ptrData)
        ccVersions = getCcPathVersions(client, path)
        if ccVersions == {}:
            pathElts = ["changecontrol", path]
            ptrData = {"v1": Path(keys=["changecontrol", path, "v1"])}
            publish(client, 'cvp', pathElts, ptrData)

    async def doTemplates(self, client):
        try:
            f = open("files/campusWorkshop_ccTemplates.json", "r")
            templates = yaml.safe_load(f.read())
            f.close()
        except:
            return

        await self.createRootPath(client, 'template')
        for templateKey, templateData in templates.items():
            pathElts = ["changecontrol", "template", "v1", templateKey]
            update = {templateKey: templateData}
            publish(client, 'cvp', pathElts, update)
            ptrData = {templateKey: Path(keys=["changecontrol", "template", "v1", templateKey])}
            publish(client, 'cvp', pathElts[:-1], ptrData)

    async def doActionBundles(self, client):
        print(f"{config.currentPod} - doActionBundles")
        try:
            f = open("files/campusWorkshop_actionBundles.json", "r")
            bundles = yaml.safe_load(f.read())
            f.close()
        except:
            return

        await self.createRootPath(client, 'actionBundle')
        for bundleKey, bundleData in bundles.items():
            pathElts = ["changecontrol", "actionBundle", "v1", bundleKey]
            update = {bundleKey: bundleData}
            publish(client, 'cvp', pathElts, update)
            ptrData = {bundleKey: Path(keys=["changecontrol", "actionBundle", "v1", bundleKey])}
            publish(client, 'cvp', pathElts[:-1], ptrData)

    async def doAddImages(self):
        print(f"{config.currentPod} - doAddImages")
        headers = {
            'Authorization': f'Bearer {self.tok}',
        }

        existingImages = {}
        url = f'{self.baseURL}/api/resources/softwaremanagement/v1/Repository/all'
        resp = requests.get(url, verify=False, timeout=300, headers=headers)
        images = json_decoder(resp.text)
        for image in images:
            existingImages[image.get("result", {}).get("value", {}).get("key", {}).get("name", "")] = True

        url = f'{self.baseURL}/cvpservice/softwaremanagement/v1/uploads'
        for filepath in config.args.cvAddImages:
            filename = basename(filepath)
            if filename in existingImages:
                continue

            print(f" uploading {filename}")

            with open(filepath, "rb") as image:
                fields = {
                    "name": filename,
                    "rebootRequired": "True",
                    "file": (
                        filename,
                        image,
                        'application/octet-stream',
                        {
                            "Content-Transfer-Encoding": 'binary'
                        }
                    )
                }

                m = MultipartEncoder(fields=fields)

                headers['Content-Type'] = m.content_type
                resp = requests.post(url, data=m, verify=False, timeout=300, headers=headers)
                if resp.status_code in [ 200, 201, 409 ]:
                    continue

                resp.raise_for_status()

    async def doAdminUsers(self):
        print(f"{config.currentPod} - doAdminUsers")
        url = f'{self.baseURL}/cvpservice/user/addUser.do'

        for user in config.args.cvAddAdmins:
            userJson = {
                'roles': ["network-admin"],
                'user': {
                    'description': "",
                    'contactNumber': "",
                    'userType': "SSO",
                    'userStatus': "Enabled",
                    'currentStatus': "",
                    'addedByUser': "pfelt",
                    'profile': "",
                    'alternateLoginType': "RESTRICTED",
                    'userId': user,
                    'firstName': user,
                    'lastName': user,
                    'email': user
                }
            }
            resp = requests.post(url, json=userJson, verify=False, timeout=300, headers={'Authorization': f"Bearer {self.tok}"})
            resp.raise_for_status()

    async def doPackage(self, package):
        print(f"{config.currentPod} - doPackage")
        with open(package, "rb") as file:
            url = f'{self.baseURL}/cvpservice/packaging/v1/packages?dry-run=false&force=true'
            resp = requests.post(url, files={'file': file}, verify=False, timeout=300, headers={'Authorization': f"Bearer {self.tok}"})
            resp.raise_for_status()

    async def cleanupDashboards(self, client):
        print(f"{config.currentPod} - cleanupDashboards")
        url = f'{self.baseURL}/api/resources/dashboard/v1/Dashboard/all'

        resp = requests.post(url, data={}, verify=False, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})
        resp.raise_for_status()

        dashboards = json_decoder(resp.text)
        if not isinstance(dashboards, list):
            dashboards = [dashboards]

        for dashboard in dashboards:
            params = {
                "key.dashboardId" : dashboard["result"]["value"]["key"]["dashboardId"]
            }
            url = f'{self.baseURL}/api/resources/dashboard/v1/DashboardConfig'
            resp = requests.delete(url, params=params, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})

    async def doOAuthConfig(self):
        url = f'{self.baseURL}/api/resources/identityprovider/v1/OAuthConfig'
        resp = requests.get(f'{url}/all', verify=False, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})
        resp.raise_for_status()
        oAuthProviders = resp.json()
        print(oAuthProviders)
        permittedDomains = oAuthProviders.get("result", {}).get("value", {})
        permittedDomains["permittedEmailDomains"] = {"values": ["arista.com","gmail.com"]}

        params = {
            "key.providerId": "google"
        }

        data = {
            "key": {
                "providerId": "google"
            },
            "permittedEmailDomains":{"values":["arista.com", "gmail.com"]}
        }

        resp = requests.post(f'{url}', data=json.dumps(data), verify=False, timeout=300, headers={'Authorization': f'Bearer {self.tok}'})
        resp.raise_for_status()
        print(resp)
        print(resp.text)
        

    async def studios(self):
        # first get all the devices in the inventory
        deviceInventory = config.globalInventory.get(str(int(config.currentPod)), -1)
        #if deviceInventory == -1:
            #return

        cvpRacClient = CvpClient()
        cvpRacClient.connect(nodes=[self.server], username='', password='', is_cvaas=True, api_token=self.tok)

        c = pyavd._cv.client.CVClient(self.server, token=self.tok)
        c._connect()

        fp = tempfile.NamedTemporaryFile(mode="w")
        fp.write(self.tok)
        fp.flush()
        grpcClient = GRPCClient(self.server, token=fp.name)
        fp.close()

        workToDo = False
        expectCC = True

        if config.args.cvTest:
            print("connected")
            await self.unprovisionDevicesCV(c, cvpRacClient, deviceInventory)
            return

            await self.smsUploadImage("./files/images/act-vEOS-4.29.7M.swi")
            return

            await self.doOAuthConfig(deviceInventory)
            return

        if config.args.cvAddImages:
            await self.doAddImages()
            return

        if config.args.cvAddAdmins:
            await self.doAdminUsers()
            return

        if config.args.cvAddPackages:
            await self.doPackage("files/sleep_0.2.0.tar")
            await self.doPackage("files/cv-workshop_1.0.0.tar")
            return

        if config.args.cvAddCCStuff:
            await self.doActionBundles(grpcClient)
            await self.doTemplates(grpcClient)
            return

        if config.args.cvCleanupNotifiers:
            await self.notificationReceiverCleanup(c)
            return

        if config.args.cvCleanup:
            # start by creating a new workspace
            workspaceID = str(uuid.uuid4())
            workspace = await c.create_workspace(
                workspace_id=workspaceID,
                display_name="automation cleanup")

            expectCC = False
            workToDo = True

            ###### cleanup steps
            await self.cleanupDashboards(cvpRacClient)
            await self.tagsCleanup(c, workspaceID)
            await self.scsCleanup(c, workspaceID)
            for studio in ['studio-avd-campus-fabric', 'studio-campus-access-interfaces', 'studio-software-management', 'studio-authentication', 'studio-date-time', 'studio-dns-settings', 'studio-management-connectivity', 'studio-telemetry-config', 'studio-connectivity']:
                await self.studioCleanup(c, workspaceID, studio)

            await self.inventoryCleanup(c, workspaceID)
            await self.notificationReceiverCleanup(c)
            #done below
            #await self.buildAndSubmitWorkspace(c, workspaceID, expectCC=False)
            #await self.unprovisionDevices(c, cvpRacClient, deviceInventory)

            ######

        if config.args.cvSetup:
            # start by creating a new workspace
            workspaceID = str(uuid.uuid4())
            workspace = await c.create_workspace(
                workspace_id=workspaceID,
                display_name="automation setup")

            workToDo = True

            ###### setup steps
            await self.doActionBundles(grpcClient)
            await self.doTemplates(grpcClient)

            await self.doPackage("files/sleep_0.2.0.tar")
            await self.doPackage("files/cv-workshop_1.0.0.tar")

            await self.onboardDevices(c, cvpRacClient, workspaceID, deviceInventory)
            await self.assignTags(c, workspaceID, deviceInventory)
            await self.scsSetup(c, workspaceID, deviceInventory)
            await self.smsSetup(c, workspaceID, deviceInventory)
            await self.aicStudioSetup(c, workspaceID, deviceInventory)
            await self.campusStudioSetup(c, workspaceID, deviceInventory)

        if workToDo:
            ccID = await self.buildAndSubmitWorkspace(c, workspaceID, expectCC=expectCC)

            # from here on out, let's reconnect with the second token
            #  this allows for us to complete even if four-eyes is set
            c = pyavd._cv.client.CVClient(self.server, token=self.tok2)
            c._connect()

            if expectCC:
                await self.executeChangeControl(c, ccID, wait=False)

            if config.args.cvCleanup:
                #await self.deleteDevices(cvpRacClient)
                if config.args.type.lower() == 'campus':
                    await self.unprovisionDevicesCampus(c, cvpRacClient, deviceInventory)
                elif config.args.type.lower() == 'cv':
                    await self.unprovisionDevicesCV(c, cvpRacClient, deviceInventory)

    async def execute(self):
        await self.studios()
