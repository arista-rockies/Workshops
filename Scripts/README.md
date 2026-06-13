# workshop scripting

## installation
there is a simple setup.sh script which will
1) create a venv
2) activate it
3) pip install requirements

other requirements must be met for these scripts to function properly.  these steps include sensitive information and are not included in the repository
* create `tokenConfig.yml` which contains all api tokens
* create the `p12` directory which contains `radsec_ca_certificate.pem` for agni in it
* create the `images` directory which contains the requisite swi images

lastly you must enable the systemd service and start the bootstrap server

```
sudo cp bootstrap.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable bootstrap
sudo systemctl start bootstrap
```


