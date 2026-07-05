# Campus A-02 Wired Lab Guide

## Access Interface Configuration

![CloudVision](images/CVP_logo.png)

## This Lab Guide:
[Campus A-02 Wired Lab Guide - Access Interface Configuration](https://github.com/arista-rockies/Workshops/blob/main/Campus/2026_Campus_Workshop/A-02/2026_Campus_A-02_Wired_Lab_Guide.md)


---

## Table of Contents

1. [Full Lab Topology](#1-full-lab-topology)
2. [POD Topology](#2-pod-topology)
3. [Accessing CloudVision as a Service](#3-accessing-cloudvision-as-a-service)
4. [Creating Port Profiles](#4-creating-port-profiles)
5. [Assigning Port Profiles for AP and RPI](#5-assigning-port-profiles-for-ap-and-rpi)

---

## 1. Full Lab Topology

![Full Lab Topology](images/full-lab-topology.png)

---

## 2. POD Topology

![POD Topology](images/pod-lab-topology.png)

---

## 3. Accessing CloudVision as a Service

1. Go to the Arista Ignition GUI via: https://ignition.campus-atd.net/ 
- Enter the 6 digit Access Code found on the Pod Handout Worksheet 
- Click.  ![Submit Passcode](images/ignition_submit.png)

![image5](images/Ignition1.png)

2. Click the **CVaaS** tile

![image5a](images/Ignition_cvaas.png)

3. You will now be logged into CloudVision

![CloudVision Dashboard](images/cloudvision-dashboard.png)

---

## 4. Creating Port Profiles

This lab will help you create 2 port profiles and apply them to interfaces in your Lab network.

### Wireless AP Port Profile ###

1. Assign the configured port profiles to the switches access ports

    - Navigate to **Network Hierarchy**
    - Navigate through 
      - **Network**  
      - **Workshops** 
      - **IT-Bldg**  
      - **IDF1**

![Hierarchy Navigation](images/hierarchy-navigation.png)

2. Select the **Front Panel** tab

![Hierarchy Front Panel](images/quick-action1.png)

3. Select **Ethernet1** on **leaf1b**
    - Select **Configure**

![Hierarchy Front Panel](images/quick-action2.png)

4. Under the profile section Select **+ Create New Profile**

![Hierarchy New Port Profile](images/hier-port-profile1.png)

4. Under the **General** Section 
    - Name: **Wireless-Access-Point**
    - Enabled: **Yes**

![Interface Profile Quick Actions](images/wireless-profile-configuration2.png)

5. Under the **Mode** Section
    - Mode: **Access**
    - VLANs: **1##** where **##** is a 2 digit character assigned to your lab/Pod. e.g Pod01 is VLAN101, Pod13 is VLAN113  

![Interface Profile Quick Actions](images/wireless-profile-configuration3.png)

6. Under the **PoE** Section
    - Reboot Action: **Maintain** 
    - Link Down Action: **Maintain** 
    - Shutdown Action: **Maintain** 

![Interface Profile Quick Actions](images/wireless-profile-configuration4.png)

7. Under the **Port-Channel** Section
    - Port-Channel: **Yes**
    - Description: **Wireless Access Point Port-Channel**
    - Enabled: **Yes**
    - Mode: **Active**
    - MLAG: **Yes**
    - LACP Fallback Mode: **Individual**

*The Wireless Access Point has the capability to run a port channel but is not currently configured as such. We will use LACP fallback so we may provision the Access Point with its current configuration*

![Interface Profile Quick Actions](images/wireless-profile-configuration5.png)

8. Select **Create**

![Interface Profile Quick Actions](images/submit-profile-configuration1.png)

9. Select **Close**

![Close Quick Action](images/close-quick-action.png)

10. Return to the **Interface Configuration** section and Under the profile Section once again select **+ Create New Profile**

![Profile Quick Action](images/hier-port-profile2.png)

11. Under the **General** Section
    - Name: **Wired-RasPi**
    - Enabled: **Yes**  

![Interface Profile Quick Actions](images/wired-profile-configuration2.png)

12. Under the **Mode** Section
    - Mode: **Access**
    - VLANs: **1##** where **##** is a 2 digit character assigned to your lab/Pod. e.g Pod01 is VLAN101, Pod13 is VLAN113  

![Interface Profile Quick Actions](images/wired-profile-configuration3.png)

13. Under the **Spanning Tree** Section
    - Portfast: **Edge**
    - BPDU Guard: **Enabled**

![Interface Profile Quick Actions](images/wired-profile-configuration4.png)

14. Under the **PoE** Section
    - Reboot Action: **Maintain** 
    - Link Down Action: **Maintain** 
    - Shutdown Action: **Maintain** 

![Interface Profile Quick Actions](images/wired-profile-configuration5.png)

15. Under the **802.1x > General** Section
    - Enabled: **Yes** 


![Interface Profile Quick Actions](images/wired-profile-configuration6.png)

16. Under the **802.1x > MAC-Based Authentication** Section
    - Enabled: **Yes** 

![Interface Profile Quick Actions](images/wired-profile-configuration7.png)

17. Select **Create**

![Interface Profile Quick Actions](images/submit-profile-configuration1.png)

18. After the Workspace has built Select **Review**

![Interface Profile Quick Actions](images/submit-profile-configuration2.png)

19. Select **Submit Workspace** to save the proposed port profile.

*Note at this time no configuration changes are being made. You have only configured that Port Profiles that we will use in the next next section to configure our interfaces*

![Interface Profile Quick Actions](images/submit-profile-configuration3.png)

20. Select **Visit Studios**

![Interface Profile Quick Actions](images/submit-profile-configuration4.png)

**LAB SECTION COMPLETE**

---

## 5. Assigning Port Profiles for AP and RPI

Assign the configured port profiles to the switches access ports

1. Navigate to **Network Hierarchy**
    - Navigate through 
      - **Network**  
      - **Workshops** 
      - **IT-Bldg**  
      - **IDF1**

![Hierarchy Navigation](images/hierarchy-navigation.png)

2. Select the **Front Panel** tab

![Hierarchy Front Panel](images/quick-action1.png)

3. Select **Ethernet1** on **leaf1b**
    - Select **Configure**

![Set Port Profiles](images/quick-action2.png)

4. A new **Interface Configuration** section should be available where you selected Configure. 
    - Profile: **Wired-RasPi**
    - Select **Save**

![Set Port Profiles](images/quick-action3.png)



5. De-Select **Ethernet1** on **leaf1b** and Select **Ethernet14** on **leaf1a**
    - Select **Configure**

![Set Port Profiles](images/set-profile1.png)

6. A new **Interface Configuration** section should be available where you selected Configure. 
    - Profile: **Wireless-Access-Point**
    - Select **Save**

![Set Port Profiles](images/set-profile2.png)

7. De-Select **Ethernet14** on **leaf1a** and Select **Ethernet14** on **leaf1b**
    - Select **Configure**

![Set Port Profiles](images/set-profile3.png)

8. A new **Interface Configuration** section should be available where you selected Configure. 
    - Profile: **Wired-Access-Poin**
    - Select **Save**

![Set Port Profiles](images/set-profile4.png)

9. Towards the bottom center of your screen you should see a black bar. Select the **Clipboard Icon**

![Set Port Profiles](images/set-profile5.png)

10. This will bring you to the Workspace Review Page.
    -  Review the proposed changes 
    -  Select **Submit Workspace**

![Set Port Profiles](images/set-profile6.png)

11. Select **View Change Control**

![Set Wired Profile](images/set-profile7.png)

12. This will bring you to the Change Control. 
     - Select **Review and Approve**

![Set Wired Profile](images/set-profile8.png)

13. Review the proposed changes and select **Approve and Execute**

![Set Wired Profile](images/set-profile9.png)

14. Once the Change Control completes, that switches now have the interface profiles active in their configuration.

![Set Wired Profile](images/set-profile10.png)

**LAB GUIDE COMPLETE**
