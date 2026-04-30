# Campus SD-02
## Activate SD-WAN Edge

<!-- TODO: Add Images -->

---

## This Lab Guide:
[Campus SD-02 VeloCloud Lab Guide - Activate SD-WAN Edge](https://github.com/arista-rockies/Workshops/blob/main/Campus/2026_Campus_Workshop/SD-02/2026_Campus_SD-02_VeloCloud_Lab_Guide_Activate_SD-WAN_Edge.md)

## Table of Contents
1. [Full Lab Topoology](#1-full-lab-topology)
2. [POD Topology](#2-pod-topology)

---

## 1. Full lab Topology

![Full Lab Topology](images/full-lab-topology.png)

---

## 2. POD Topology

![POD Topology](images/pod-lab-topology.png)

---

- Access the VeloCloud Orchestrator (VCO) at: https://veco12-kiad1.velocloud.net/ui/login
- Enter the username and password provided and click Login
- You will come to a Network Overview page.
- At the top of this screen, you have 4 main functions:
    - Monitor contains views that allow you to high level environment wide status as well as detailed status of individual edges and WAN links.
    - Configure is where you define the configuration of your WAN with Profiles and Edges.
    - Diagnostics allows you to get real-time information about the state of your SD-WAN edges for diagnostics purposes.
    - Service Settings contains some environment-wide settings related to Alerts, Notifications and Licensing.
- Select the Configure section and if necessary click on Edges in the left column.
- All the Pods in the Workshop have one VeloCloud Edge (VCE) and they are all part of the same Enterprise on the VCO. Please be aware that modifications to VCEs other than your assigned Pod will effect other participants.

---

- We are now going to activate your edge using the built-in Wi-Fi on the VCE.
- Select your Edge from the list.
- Click the Overview screen.
- Click Send Activation Email
- Find the link in the template email.
- Do not click it yet.
- There is a Wi-Fi network 
- Before clicking the link, connect to the Wifi network named "velocloud-XXX" where XXX is the last 3 digits of the serial number on your VCE. The password is "vcsecret".
- Once you are connected to that SSID, open the link from the "Activation Email" screen.
- The edge will activate and you will see the following screen.

--

- Once activation is complete, return to the VCO.
- Click on the Monitor screen.
- Click Edges
- If you don't see the status of Connected next to your Edge Name, click on Events on the left menu.
- You can filter to just your Edge by using "Edge Name" "is" "campus-vce##"
- You want to look for the following events:
    - Received Edge activation
    - Activated
    - Online
    - Link alive