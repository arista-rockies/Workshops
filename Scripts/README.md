# workshop scripting

## installation
there is a simple setup.sh script which will
```bash
pip -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

other requirements must be met for these scripts to function properly.  these steps include sensitive information and are not included in the repository
* create `tokenConfig.yml` which contains all api tokens
```yaml
apiToken:
  "0":
      "name": "pod 0"
      "cv":
        "server": "www.arista.io"
        "tenant": "rockies-training-00"
        "key1": "serviceAccountToken1"
        "key2": "serviceAccountToken2"
      "act":
        "resourceName": "formatString of lab resources:  eg: cv-workshop-pod{}"
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
        "server": "https://agni.arista.com"
        "tenant": "Z_ROCKIES-ATD-01"
        "keyid": "agniKeyID"
        "key": "agniKey"
        "orgid": "agniOrgID"
      "velo":
        "tenant": "Rockies Workshop"
        "keyid": ""
        "key": "velokey"
        "url": "https://veloVCO.com"
        "sshPassword": "formatStringOfPassword"
        "enterpriseID": int
        "enterpriseLogicalID": uuid4
      "act":
        "resourceName": "formatString of lab resources:  eg: cv-workshop-pod{}"
        "server": "act.arista.io"
        "key": "actKey"
        "sshPassword": ""
```
* create the `images` directory which contains the requisite swi images

## workshop with physical gear
* create a csv of the following column format (note that the code depends on those names and cases
```csv
Model,Serial Number,Mac address,Registration Key,CVaaS and CV-CUE Pod Assignment,Hostname,Software Version,Note
```

* lastly you must enable the systemd service and start the bootstrap server

```bash
sudo cp bootstrap.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable bootstrap
sudo systemctl start bootstrap
```


