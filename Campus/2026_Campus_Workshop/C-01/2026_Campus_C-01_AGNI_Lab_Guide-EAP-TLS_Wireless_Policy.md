# Campus C-01 AGNI Lab Guide 
## EAP-TLS Wireless Policy

![image1](images/CVCUE_logo.png) 
![image2](images/AGNI_logo.png)

---

This Lab Guide:

https://github.com/arista-rockies/Workshops/blob/main/Campus/2026_Campus_Workshop/C-01/2026_Campus_C-01_AGNI_Lab_Guide-EAP-TLS_Wireless_Policy.md

---

## Table of Contents

[Full Lab Topology](#full-lab-topology)  
[POD Topology](#pod-topology)  

---

**NAC Lab #1 - Create EAP-TLS Wireless Policy**  
1. [CloudVision Cognitive Unified Edge CV-CUE Access](#1-cloudvision-cognitive-unified-edge-cv-cue-access)  
2. [Create an EAP-TLS SSID](#2-create-an-eap-tls-ssid)  
3. [CloudVision AGNI Access](#3-cloudvision-agni-access)  
4. [Create AGNI Networks & Segments for the EAP-TLS Wireless Policy](#4-create-agni-networks--segments-for-the-eap-tls-wireless-policy) 

**Additional Information**  
1. [Setting up RadSec with a TPM AP Certificate](#1-setting-up-radsec-with-a-tpm-ap-certificate)  
2. [Setting up RadSec with a Custom AP Certificate](#2-setting-up-radsec-with-a-custom-ap-certificate)  

---

## Full Lab Topology

![image3](images/full-lab-topology.png)

---

## POD Topology


![image4](images/pod-lab-topology.png)
---

## NAC Lab #1 - Create EAP-TLS Wireless Policy

---

### 1. CloudVision Cognitive Unified Edge CV-CUE Access

1. Go to the Arista Ignition GUI via: https://ignition.campus-atd.net/ 
- Enter the 6 digit Access Code found on the Pod Handout Worksheet 

- Click ![image4a](images/image4a.png)


![image5](images/Ignition1.png)


2. Click the **CV-CUE and AGNI Launchpad** tile

![image5a](images/Ignition_launchpad.png)

**Launchpad**

- When you open the Launchpad, you are presented with multiple applications. Each of these applications, with the exception of CloudVision and AGNI, are included with the CV-CUE subscription. CloudVision and AGNI are available from the LaunchPad with their respective subscriptions.

**Dashboard tab**

![image6](images/image6.png)

**Descriptions for the tiles are below:**

- CV-CUE (CloudVision WiFi) this is the Wireless Manager  
- Packets is an online .pcap debug allowing you to examine the packet information.  
- Nano allows you to manage your environment from your smartphone  
- WiFi Device Registration is the process for importing APs onto your account  
- AGNI - Beta Arista Guardian for Network Identity (Network Access Control)

3. Select **CV-CUE (CloudVision WiFi)**

---

### 2. Create an EAP-TLS SSID

- The **Configure** section of CV-CUE is broken into several parts, including **WiFi**, **Alerts**,**WIPS**, etc.  **Alerts** is where syslog and other alert related settings are configured, and **WIPS** is where the policies are configured for the WIPS sensor.

- In this lab, we will be working in the **WiFi** configuration area. Create an SSID (WPA3 Transition Mode - WPA3 Enterprise) with your **ATD-##-EAP** as the name (where **##** is a 2 digit character between 01-20 that was assigned to your lab/Pod).

1. Hover your cursor over the **Configure** menu option on the left side of the screen, then click **WiFi**.

![image7](images/image7.png)

2. At the top of the screen, you will see where you are in the location hierarchy. If you aren’t on **Corp**, click on the three lines (hamburger icon) next to **Locations** to expand the hierarchy and choose/highlight the **Corp** folder.  
3. Now click the “Add SSID” button on the right hand side of the screen.

- With the hierarchy menu collapsed:

![image8](images/image8.png)

- Or, with the hierarchy menu expanded:

![image9](images/image9.png)

- Once on the **SSID** page, configuration sub-category menu options will appear across the top of the page related to WiFi (the defaults are **Basic**, **Security**, and **Network**). You can click on these sub-category names to change configuration items related to that area of the configuration.

- To make additional categories visible, click on the 3 dots next to **Network** and you can see the other categories that are available to configure (i.e. **Analytics**, **Captive Portal**, etc.).

![image10](images/image10.png)


4. In the **Basic** sub-category option, name the SSID **ATD-##-EAP** (where **##** is a 2 digit character between 01-20 that was assigned to your lab/Pod). The **Profile Name** is used to describe the SSID and should have been auto-filled for you. 

![image11](images/image11.png)

5. Since this is our corporate SSID, leave the **Select SSID Type** set to **Private**, but note this is where you would change it to **Guest** if needed.  Select **Next** at the bottom.

![image12](images/image12.png)

6. In the **Security** sub-category, select **WPA3 Transition Mode** and change the association type to **WPA3 Enterprise**.

![image13](images/image13a.png)

7. Next, under **RADIUS Settings** check **RadSec** and select **AGNI** in the drop down box under Authentication and Accounting Server

![image14](images/image14.png)

8. Select **Next** at the bottom of the screen.

![image15](images/image15.png)

9. In the **Network** configuration sub-category, we’ll leave the **VLAN ID** set to **0**, which means it will use the native VLAN. If the switchport the AP is attached to is trunked, you could change this setting to whichever VLAN you want the traffic mapped to.

- We are using **Bridged** mode in this lab.

![image16](images/image16.png)

- You could use “NAT” (often done for Guest) or “L2 Tunnel” / “L3 Tunnel” (as you would see for a Guest Anchor or tunneled corporate traffic).

- The rest of the settings can be left at the default values.


10. Click the **Save & Turn SSID On** button at the bottom of the page.

![image17](images/image17.png)

11. On the pop-up page, click **Customize** if that option appears, otherwise skip to the next step.

12. Only select the **5 GHz** option on the next screen (uncheck the 2.4 GHz box if it’s checked), then click **Turn SSID On**.

![image18](images/image18.png)

13. After you turn on the SSID, hover your cursor over **Monitor** in the left hand side menu, and then click **WiFi**.


![image19](images/image19.png)

14. Check the **Active SSIDs** menu at the top of the screen.  Is your SSID listed?

![image20](images/image20.png)

---

### 3. CloudVision AGNI Access
#### Launchpad ####
1. Return to the **LaunchPad**, and select the **AGNI - Trial** tile.

![image22](images/image22.png)  

---

### 4. Create AGNI Networks & Segments for the EAP-TLS Wireless Policy

1. Click on **Networks** and select **+ Add**

![image24](images/image24.png)
![image25](images/image25.png)


2. Type in the **Name** - **Wireless-EAP-TLS**

3. Select **Connection Type**: **Wireless**

4. **SSID** needs to match what you created in CV-CUE type **ATD-##-EAP**

![image26](images/image26.png)

5. Under **Authentication**, select **Authentication Type - 802.1X EAP**

6. And **EAP Methods - EAP-TLS**

![image27](images/image27.png)

7. Under **EAP-TLS Authenticaiton Settings**, **Enabled** Trust External Certificates
8. And Select **Required** for User Identity Binding

**NOTE:** The Raspberry Pi's are using External Certificates that are Trusted by AGNI.

**User Identity Binding**
- **Required** - When set, the certificate has a valid query-able user identity for
request authorizations.
- **Optional** - When set, the certificate contains any identity that is optionally bound or not bound
to the user. For example, this option can be set to honor appliance authentication where the
certificates are not bound to any user but set to machine identity.  

![image27-2](images/image27-2.png)  

9. Click on **Add Network** at the bottom of the screen.

![image28](images/image28.png)

10. Next, click on **Segments** and then **+ Add**

![image29](images/image29.png)
![image30](images/image30.png)  

11. Next, type in the name: **Wireless-EAP-TLS** and the Description as well.

![image32](images/image32.png)

12. Next, let’s **Add Conditions**.  

**Note:** Adding more than one condition means **MATCH ALL**

![image33](images/image33.png)

13. Select, **Network, Name, Is, Wireless-EAP-TLS** from the drop down lists.

![image34](images/image34.png)

14. Let’s add one more condition.

![image35](images/image35.png)

15. Select, **Network, Authentication Type, Is, Client Certificate (EAP-TLS)** from the drop down lists.

![image36](images/image36.png)

16. Your Conditions should now look like this.

![image37](images/image37.png)

17. Under Actions select **Add Action**.

![image38](images/image38.png)

18. Select **Allow Access**.

![image39](images/image39.png)


19. Finally, select **Add Segment** at the bottom of the page.

![image40](images/image40.png)

20. You should now be able to expand and review your segment.

![image41](images/image41.png)

21. Next, click on **Sessions** to see if your **ATD Raspberry Pi** has a connection via the Wireless connection.  

**Note**: The Client Certificate has already been applied to the Raspberry Pi and is configured to connect to the SSID **ATD-##-EAP**. 

- If you don’t see any new sessions within 2 minutes AGNI, power cycle the Raspberry Pi.

![image42](images/image42.png)

## End of EAP-TLS Wireless Policy Lab
---

## Additional Information

### 1. Setting up RadSec with a TPM AP Certificate


**NOTE**: The following example is for TPM Based AP’s. The Arista’s C-2xx (except the C-250/C-260), C-3xx, and C-4xx Series APs include a TPM chip.

What is RadSec?
CloudVision AGNI integrates with network infrastructure devices (wired switches and wireless access points) through a highly secure TLS-based RadSec tunnel. 
Port 2083
The highly secure and encrypted tunnel offers complete protection to the communications that happen in a distributed network environment. This mechanism offers much greater security to AAA workflows when compared with traditional RADIUS environment workflows, which are not encrypted. 

https://www.arista.com/en/support/toi/eos-4-27-0f/14891-radius-dynamic-authorization-over-tls






Click on the **CV-CUE** and **AGNI - Beta** Tiles from the LaunchPad and they will open in a new Tab.


![image43](images/image43.png)
![image44](images/image44.png)

In **AGNI** - Click on **Configuration - System - RadSec Settings** on the left hand side.

![image45](images/image45.png)
![image46](images/image46.png)

Copy the FQDN **(radsec.beta.agni.arista.io)** and Download the Certificate at the bottom.

![image47](images/image47.png)

Next, go back to **CV-CUE** and let’s set up a RadSec Server.


**Configure → Network Profiles → RADIUS → Add RADIUS Server**

![image48](images/image48.png)
![image49](images/image49.png)
![image50](images/image50.png)

Note: Once the Radius Profile is assigned to a SSID, the RadSec Connection will come up.

Next, in **AGNI click on Access Devices** and then **Devices** look at the **RadSec Status**.

![image51](images/image51.png)

If the AP does not connect, issue a reboot.



For more information see the video below.

**RadSec Tunnel with TPM chip APs**

![image52](images/image52.png)
https://www.youtube.com/watch?v=9kxJDjRnVnE


---

### 2. Setting up RadSec with a Custom AP Certificate

NOTE: The following example is for non-TPM Based AP’s. The Arista C-250 and C-260 APs are non-TPM Based APs.

Click on the **CV-CUE** and **AGNI - Beta** Tiles from the LaunchPad and they will open in a new Tab.

![image53](images/image53.png)
![image54](images/image54.png)

*Note:  When applying the Certificate to the AP it is recommended to have both the CV-CUE and AGNI windows opened side by side.

First we **Generate a CSR in CV-CUE**.  Click on **Monitor, WiFi** and then **Access Points**

![image55](images/image55.png)

**On Right hand side on top** and click on **Certificate Actions**

![image56](images/image56.png)

Next, **Right Click on the AP** and select **Generate CSR** and select your **Certificate Tag**.

![image57](images/image57.png)

Next, **Right Click on the AP** and select **Download CSR** and select your **Certificate Tag**.

![image58](images/image58.png)

Next, **Right Click on the AP** and select **Download CSR** and select your **Certificate Tag**.


![image59](images/image59.png)
![image60](images/image60.png)
![image61](images/image61.png)

**Unzip the CSR File**

![image62](images/image62.png)

AGNI - Click on **Access Devices** and Select the **AP**.

**Access Devices → Devices → Select AP → Get Client Certificate**

![image63](images/image63.png)
![image64](images/image64.png)

Select **Get Client Certificate**.

Next, Select **Generate Certificate: Use CSR (Single Device)**, and **Select Action: Upload CSR File**, and browse to and **select the CSR file** that you unzipped earlier in the process.

Select **Generate Certificate** and the AP Client Certificate will be created and downloaded to your device.

![image66](images/image66.png)

**CV-CUE - Upload the Device Certificate**

Go to **Monitor → WiFi → Access Points → Select AP → Certificate → Upload Device Certificate**, and **upload the Client/Device Certificate** that was downloaded to your device. **Use the same Certificate Tag** as when you Downloaded the CSR above.

![image67](images/image67.png)
![image68](images/image68.png)

**Note**: Once the Radius Profile is assigned to a SSID, the RadSec Connection will come up.

Next, in AGNI click on **Access Devices** and then **Devices** look at the **RadSec Status**.

![image69](images/image69.png)

If the AP does not connect, issue a reboot.

For more details see the video below.

**RadSec Tunnel with Arista AP using Custom certificate (non-TPM chip AP's)**

![image70](images/image70.png)
https://www.youtube.com/watch?v=kFJ24zRHYJ8&t=75s

---

**NAC LAB #1 COMPLETE**
