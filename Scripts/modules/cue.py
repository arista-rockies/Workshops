#TODO: need to move the cue server to the tokenFile
from modules import config
import requests, json
from modules.pgf import pgfAction

class CueService():
    def __init__(self, serviceType, serviceServer, serviceURI):
        self.type = serviceType
        self.server = serviceServer
        self.baseURL = f'{self.server}{serviceURI}'
        self.cookies = None

class CueClient():
    def configure():
        def _addArgument(*args, **kwargs):
            if kwargs.get('action', None) == 'store_true':
                kwargs.pop('action')
                kwargs["nargs"] = '?'
                kwargs.setdefault("default", False)
                kwargs.setdefault("const", True)

            config.parser.add_argument(*args, action=pgfAction, module="cue", **kwargs)

        config.parser.add_argument('-cueCleanup', default=False, action='store_true', help='do cue cleanup steps')
        config.parser.add_argument('-cueTest', default=False, action='store_true', help='dev code')

    def __init__(self, token):
        self.token = token
        self._connected = False
        self._services = {}

        self._authenticate()

        if not self._connected:
            raise Exception("authentication to cue failed")

    def _authenticate(self) -> bool:
        result = True

        authData = {
            "type": "apiKeyCredentials",
            "keyId": self.token["cue"]["keyid"],
            "keyValue": self.token["cue"]["key"],
            "timeout": 3600,
        }
        url = f'https://launchpad.wifi.arista.com/api/v2/session'
        resp = requests.post(url, json=authData)
        try:
            resp.raise_for_status()
        except:
            return

        authCookies = resp.cookies
        url = f'https://launchpad.wifi.arista.com/api/v2/services'
        resp = requests.get(url, cookies=authCookies)
        try:
            resp.raise_for_status()
        except:
            return

        for service in resp.json().get('data', {}).get('customerServices', []):
            if service["service"]["service_type_id"] == 2:
                self._services["wm"] = CueService(2, service["service"]["service_url"], '/wifi/api/')

                # do the auth
                url = f'{self._services["wm"].baseURL}session'
                resp = requests.post(url, json=authData)
                try:
                    resp.raise_for_status()
                except:
                    return

                self._services["wm"].cookies = resp.cookies
            elif service["service"]["service_type_id"] == 3:
                self._services["gm"] = CueService(3, service["service"]["service_url"], '/api/v1.21/')

                # do the auth
                url = f'{self._services["gm"].baseURL}site/keylogin'
                params = {
                    "key_id": self.token["cue"]["keyid"],
                    "key_value": self.token["cue"]["key"]
                }
                resp = requests.get(url, params=params)
                try:
                    resp.raise_for_status()
                except:
                    return

                self._services["gm"].cookies = resp.cookies

        self._connected = True

    def _doReq(self, reqType: str = 'GET', service: str = "wm", subsystem: str = None, params=None, data=None) -> dict():
        service = self._services.get(service, None)
        if not self._connected or not service:
            return

        url = f'{service.baseURL}{subsystem}'

        resp = requests.request(reqType, url=url, params=params, json=data, cookies=service.cookies)
        resp.raise_for_status()
        if reqType in ['GET']:
            return resp.json()

        return {}

    def _doDeleteEvents(self):
        print(f"{config.currentPod} - cue/deleteEvents")
        self._doReq(reqType='DELETE', subsystem='events/bulkdelete')

    def _doDeleteLocations(self):
        print(f"{config.currentPod} - cue/deleteLocations")
        locations = self._doReq(reqType='GET', subsystem='locations')
        if not locations:
            return
        for location in locations.get("children", []):
            if location["id"]["id"] > 0:
                data = location["id"]
                self._doReq(reqType='DELETE', subsystem='locations', data=data)

    def _doDeleteRogueAPs(self):
        print(f"{config.currentPod} - cue/deleteRogue")
        try:
            self._doReq(reqType='DELETE', subsystem='aps/inactiveauthorized')
        except:
            pass

    def _doRenameAPs(self):
        print(f"{config.currentPod} - cue/renameAPs")
        aps = self._doReq(reqType='GET', subsystem='manageddevices/aps')
        if not aps:
            return
        for ap in aps.get("managedDevices", []):
            data = {
                "name": f'Arista_{ap["macaddress"][-8:]}',
                "locationId": { "type": "locallocationid", "id": -1}
            }
            params = {
                "fields": [ "name", "locationId" ],
            }
            self._doReq(reqType='PUT', subsystem=f'manageddevices/aps/{ap["macaddress"]}', params=params, data=data)

    def _doDeleteGMPortals(self):
        print(f"{config.currentPod} - cue/delete GM Portals and users")
        portals = self._doReq(reqType='GET', service="gm", subsystem='portals')
        if not portals:
            return
        for portal in portals.get('data', {}).get('portal', []):
            if portal['is_default'] == 1:
                continue

            # delete the portal
            subsystem = f'portals/{portal["pid"]}'
            self._doReq(reqType='DELETE', service="gm", subsystem=subsystem)

    def execute(self):
        if config.args.cueTest:
            self.test()

        if config.args.cueCleanup:
            self.cleanup()

    def test(self):
        print("inside cueTest")

    def _doCreateLocations(self):
        with open('files/cue/locations.json', 'r') as f:
            locations = json.load(f)
            self._doReq(reqType='POST', subsystem='locations', data=locations)
        return

    def _doDeleteSSIDs(self, doDelete=True):
        def _doLocationCache(l):
            if not l:
                return
            locationCache[l["id"]["id"]] = l["name"]
            for child in l.get("children", []):
                _doLocationCache(child)

        print(f"{config.currentPod} - cue/deleteSSIDs")

        locationCache = {}
        _doLocationCache(self._doReq(reqType='GET', subsystem='locations'))
        if not locationCache:
            return

        params = {
                "fetchSubTreeTemplates": True
        }

        ssidProfiles = self._doReq(reqType='GET', subsystem='/deviceconfiguration/ssidprofiles', params=params)
        for profile in ssidProfiles:
            print(f'{config.currentPod}/{locationCache[profile["createdAtLocationId"]["id"]]} - {profile["templateName"]}')
            p = {
                "templateid": profile["templateId"],
                "deleteusedssidprofile": True
            }

            if doDelete:
                self._doReq(reqType='DELETE', subsystem=f'deviceconfiguration/ssidprofiles/{profile["templateId"]}', params=p)

    def cleanup(self):
        self._doDeleteEvents()
        self._doRenameAPs()
        self._doDeleteLocations()
        self._doDeleteRogueAPs()
        self._doDeleteSSIDs()
        self._doDeleteGMPortals()

        return
