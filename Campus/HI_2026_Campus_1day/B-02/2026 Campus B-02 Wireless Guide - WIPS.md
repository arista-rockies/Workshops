# Campus B-02 Wireless Lab Guide 
## WIPS  

![CloudVision Cue](images/image1.png)   

---
## This Lab Guide: 

[Campus B-01 Wireless Lab Guide - WiFi Setup](https://github.com/arista-rockies/Workshops/blob/main/Campus/2026_Campus_Workshop/B-02/2026%20Campus%20B-02%20Wireless%20Guide%20-%20WIPS.md)  

---
## Floor Plan Download:  
[Floor Plan Download](https://tinyurl.com/wififloorplan)

---
## Table of Contents

1. [Full Lab Topology](#1-full-lab-topology)
2. [POD Topology](#2-pod-topology)
3. [Accessing CloudVision Cognitive Unified Edge CV-CUE](#3-accessing-cloudvision-cognitive-unified-edge-cv-cue) 
4. [WIPS Wireless Intrusion Prevention System ](#4-wips-wireless-intrusion-prevention-system)

---
## 1. Full Lab Topology

![Full Lab Topology](images/full-lab-topology.png)

---
## 2. POD Topology

![POD Topology](images/pod-lab-topology.png)

---
## 3. Accessing CloudVision Cognitive Unified Edge CV-CUE

Go to the Arista Ignition GUI via: [https://ignition.campus-atd.net/](https://ignition.campus-atd.net/)

* Enter the 6 digit Access Code found on the Pod Handout Worksheet
  
* Click  ![](images/image4a.png)

![](images/Ignition1.png)

Click the **CV-CUE and AGNI Lauchpad** tile

![](images/Ignition_launchpad.png)

### Launchpad

Within the Launchpad Dashboard tab:

**Select CV-CUE (CloudVision WiFi).** This is the WiFi management and monitoring application.

![](images/image4.png)

---
## 4. WIPS Wireless Intrusion Prevention System 

Arista Wireless Intrusion Prevention System (WIPS) leverages RF broadcast and protocol properties including packet formats like probe requests and beacons common to all 802.11 standards(including 802.11ac and 802.11ax) to detect and prevent unauthorized access.

For more information about how Arista’s WIPS feature works, refer to this whitepaper: [https://www.arista.com/assets/data/pdf/Whitepapers/Arista-Marker-Packet-Whitepaper.pdf](https://www.arista.com/assets/data/pdf/Whitepapers/Arista-Marker-Packet-Whitepaper.pdf)

Wi-Fi threats include an ever changing landscape of vulnerabilities, such as:

* Rogue APs  
* Unauthorized BYOD Client  
* Misconfigured APs  
* Client misassociation  
* Unauthorized association  
* Ad-hoc connections  
* Honeypot AP or evil twin “Pineapple”  
* AP MAC spoofing 
* DoS attack  
* Bridging client

![](images/ARP-Request.png)

In the menu on the left hand side of the screen, hover your cursor over “**Monitor”** and then click **“WIPS”**.  Now click on **“Access Points”** and “**Clients**” in the menu at the top of the screen and explore if any Rogue APs or Clients are connected to other APs in the area.

![](images/image21.png)

![](images/image22.png)

Access points that have been detected by WIPS but are not managed within Arista CV-CUE, they are designated as Rogue or External Access Points.

![](images/image23.png)

Next, let’s explore the information we can gather about the wireless environment using Arista’s WIPS.  
Select **Monitor,**  **WIPS**:

![](images/image24.png)

In the simple lab environment, only your pod’s single AP is part of your managed wireless infrastructure. All of the other access points and clients on the network are like crowded neighbors or businesses in a shared office work space.

Under **Monitor, WIPS, Access Points** you can see all of the detected Rogue Access points. From this screen you can reclassify, set auto-prevention, add to ban list, name or move the AP. 

![](images/image25.png)

Additional information about WIPS AP classification can be found here:  
[https://www.arista.com/en/ug-cv-cue/cv-cue-wireless-intrusion-prevention-techniques](https://www.arista.com/en/ug-cv-cue/cv-cue-wireless-intrusion-prevention-techniques)

**Authorized APs**  
Access Points (APs) that are wired to the corporate network and are compliant with the Authorized Wireless LAN (WLAN) configuration defined by the Administrator in CV-CUE are classified as Authorized APs. Typically, these will be Arista APs, but the administrator can configure the Authorized WiFi policies for any AP vendors.

**Rogue Access Point**  
APs that are wired to the corporate network and do not follow the Authorized WiFi configuration defined in CV-CUE are classified as Rogue APs.  
Even if this AP is disconnected from the network, it will continue to be classified as a Rogue. These APs are a potential threat to the corporate environment and can be used for intrusion into the corporate network over Wi-Fi. It is recommended to enable Intrusion Prevention for Rogue APs so that Wi-Fi communication with these APs is always disrupted. Using the Location Tracking ability of Arista WIPS, Rogue APs should be tracked down and physically removed from the network.  
Rogue APs are displayed in Red rows on the console.

**External Access Point**  
APs that are not wired to your corporate network are classified as External APs.  
Through the connectivity tests performed by the WIPS Sensors, Wireless Manager is able to determine that these APs are not connected to the wired network. These are neighboring APs that share the same spectrum as the Authorized APs and may cause interference with your Authorized WLAN. A site survey and channel optimization should be performed to reduce radio interference from the External APs. These APs are not always a threat and hence they should not be quarantined/prevented by default, as it would disrupt neighboring Wi-Fi activity. Intrusion Prevention policies can be configured to prevent Authorized clients from connecting to External APs.

A Rogue Access point can be reclassified, moved or named from the 3-dots menu for each detected AP.

![](images/image26.png)

Within an existing campus WiFi environment or one with a mix of wireless solutions, these discovered APs can be explicitly allowed to show the most accurate security profile.

For this lab you do not need to authorize any APs.

### WIPS - Classify and Prevent individual client 

Next, let’s use the WIPS system to identify and prevent an example problematic client from connecting to your network.

Within **WIPS**, **Clients** Menu.  
Find your smartphone device connected to the previous Lab PSK. Reconnect it now to the PSK SSID, if it has been disconnected.

![](images/image27.png) 
Since this client is associated with the correct PSK for the SSID, it is automatically classified as Authorized.

Next, click the 3**\-dots menu** for the device, **Change Classification**, **Rogue**  
![](images/image28.png)

Now, **sort the clients menu by Classification column (left)** and find the red marked Rogue device.

Next, Select the **3-dots menu** for the Rogue client and click “**Prevent This Device”**

# ![](images/image29.png)

![](images/image30.png) 

Click Prevent to start the WIPS prevention mechanism to disrupt the selected client from sending and receiving traffic.

Try to connect to a public website with your test client device with the prevention setting enabled versus disabled (be sure to disable backup wireless/LTE radios).   
The test device should fail to connect to other devices through the protected WiFi network when prevention is active.

When you are finished, **STOP the client prevention**   
![](images/image31.png)

🛑   –  When you are finished, **STOP the client prevention** so that you can use this test device in upcoming labs, optionally.🛑   
 

**LAB GUIDE COMPLETE**

