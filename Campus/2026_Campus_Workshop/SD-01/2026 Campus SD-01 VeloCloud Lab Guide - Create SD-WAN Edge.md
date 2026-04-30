# Campus SD-01
## Create SD-WAN Edge

<!-- TODO: Add Images -->

---

## This Lab Guide:
[Campus SD-01 VeloCloud Lab Guide - Create SD-WAN Edge](https://github.com/arista-rockies/Workshops/blob/main/Campus/2026_Campus_Workshop/SD-01/2026_Campus_SD-01_VeloCloud_Lab_Guide_Create_SD-WAN_Edge.md)

## Table of Contents

1. [Full Lab Topology](#1-full-lab-topology)
2. [Pod Topology](#2-pod-topology)
3. Login to the VCO
4. Create an Edge

---

## 1. Full Lab Topology

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

- The first step in creating an SD-Branch is to enable your WAN connectivity. Each POD has conenctivity from two ISPs named ISP1 and ISP2.
- First, we need to create an Edge.
- Click Add Edge.
- The Name of your Edge will be "campus\-vce**\#\#**" where "\#\#" is the number of your Pod.
- The Model is "Edge 710"
- The Profile is "Workshop-Branch"
- The License is "POC"
- Click Add Edge
- In the Edge configuration, there are four screens:
    - Device which contains most Networking parameters.
    - Business Policy which contains the Application based routing and prioritization policies.
    - Firewall contains the stateful firewal configuration.
    - Overview contains the high-level configuration for the VCE.

---

- The LAN interface on the  will be a Link Aggregation Group (LAG) comprised of interfaces GE1 and GE2. 
- In the Device screen, look in the Connectivity section and expand Interfaces.
- Click LAG1
- Where is says Select Interfaces, select GE1 and GE2.
- Click the X in the Yellow Box to acknowledge the warning.
- In the LAG Interface Settings, uncheck "Enable WAN Link"
- In the IPv4 Settings section, set the Addressing Type to Static and filling the following:
    - IP Address: 10.0.1XX.1
    - CIDR Prefix: 25
- Advertise should be Enabled (checked) and NAT Direct Traffic shoudl be Disabled (unchecked)
- Set the IPv4 DHCP Server to RELAY and enter the IP Address as 100.64.0.1

---

- For the WAN interfaces, GE3 will be connected to ISP1 and GE4 will be connected to ISP2.
- The Profile already defines GE3 and GE4 to use DHCP for IP addressing.
- We are using a user-defined private WAN link so we need to define those WAN links.
- In the Interface configuration, there is WAN Link Configuration. Click on ADD USER DEFINED WAN LINK.
- Configure the following settings:
    - Link Type: Private
    - Name: isp1
    - SD-WAN Service Reachable: Activated (checked)
    - Interfaces: GE3 (checked)
- Expand the View advanced settings configuration
- In "Existing Private Network Name", select "WAN1"
- Click ADD LINK.
- For the second WAN link, click ADD USER DEFINED WAN LINK.
- Configure the following settings:
    - Link Type: Private
    - Name: isp2
    - SD-WAN Service Reachable: Activated (checked)
    - Interfaces: GE4 (checked)
- In "View advanced settings", select "WAN2".
- Click ADD LINK.
- Click SAVE CHANGES.

---

- At this point, we have created an Edge in the VCO for an Edge 710 hardware device.
- We've enabled it to use a LAG to communicate with the branch switch.
- We've manually created two WAN links for connectivity to the Internet and to the Datacenter in Pod00.
- Scroll down to the VPN Services section and expand "Cloud VPN".
- You will see that Profile we selected earlier has enabled the Cloud VPN and configured the Edge to connect to campus-vce00 as a Hub.
- Allows us to access the Datacenter services used in later labs.
- In our next lab, we will activate the hardware edge using this configuration.