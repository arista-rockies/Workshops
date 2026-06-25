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
4. [Creating Interface Profiles](#4-creating-interface-profiles)
5. [Assigning Interface Profiles for AP and RPI](#5-assigning-interface-profiles-for-ap-and-rpi)

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

## 4. Creating Interface Profiles

This lab will help you create 2 interface profiles and apply them to interfaces in your Lab network. An interface profile is a templatized interface configuration, that when applied to an interface, will inherit all the configuration present in the interface profile.

### Wireless AP Interface Profile ###

1. Navigate to **Network Hierarchy**


![Hierarchy Navigation](images/hierarchy-navigation.png)

2. Navigate to the Interface Profile Configuration Section.
    - Select **Network**
    - Select the **Configuratoin** tab to the right
    - Select **Interface Profiles**

![Hierarchy Front Panel](images/quick-action1.png)

3. Select **+ Add Porfile**

![Hierarchy Front Panel](images/quick-action2.png)

When creating these **Interface Profiles** any field that is not explicity identified should remain Blank or with the Default selection.

4. **General Section**
    - Name: **Wireless-Access-Point**
    - Enabled: **Yes**
    

![Interface Profile Quick Actions](images/wireless-profile-configuration1.png)

5. Under the **Mode** Section
    - Mode: **Access**
    - VLANs: **1##** where **##** is a 2 digit character assigned to your lab/Pod. e.g Pod01 is VLAN101, Pod13 is VLAN113  

![Interface Profile Quick Actions](images/wireless-profile-configuration2.png)

6. Under the **PoE** Section
    - Reboot Action: **Maintain** 
    - Link Down Action: **Maintain** 
    - Shutdown Action: **Maintain** 

![Interface Profile Quick Actions](images/wireless-profile-configuration3.png)

7. Under the **Port-Channel** Section
    - Port-Channel: **Yes** (Additional Settings will appear)
    - Description: **Wireless Access Point Port-Channel**
    - Enabled: **Yes**
    - Mode: **Active**
    - MLAG: **Yes**
    - LACP Fallback Mode: **Individual**

*The Wireless Access Point has the capability to run a port channel but is not currently configured as such. We will use LACP fallback so we may provision the Access Point with its current configuration*

![Interface Profile Quick Actions](images/wireless-profile-configuration4.png)

8. Select **Create**

![Interface Profile Quick Actions](images/submit-profile-configuration1.png)

9. This will generate a workspace and validate all of your inputs. You may see a spinning blue circle while the workspace is built. When completed that circle will turn **Green** and you can then Select **Close**

![Close Quick Action](images/submit-profile-configuration2.png)

10. Returning to the **Interface Profile** section select **+ Add Profile**

![Profile Quick Action](images/wired-port-profile1.png)

11. Under the **General** Section
    - Description: **Wired-RasPi**
    - Enabled: **Yes**  

![Interface Profile Quick Actions](images/wired-port-profile2.png)

12. Under the **Mode** Section
    - Mode: **Access**
    - VLANs: **1##** where **##** is a 2 digit character assigned to your lab/Pod. e.g Pod01 is VLAN101, Pod13 is VLAN113  

![Interface Profile Quick Actions](images/wired-port-profile3.png)

13. Under the **Spanning Tree** Section
    - Portfast: **Edge**
    - BPDU Guard: **Enabled**

![Interface Profile Quick Actions](images/wired-port-profile4.png)

14. Under the **PoE** Section
    - Reboot Action: **Maintain** 
    - Link Down Action: **Maintain** 
    - Shutdown Action: **Maintain** 

![Interface Profile Quick Actions](images/wired-port-profile5.png)

15. Under the **802.1x > General** Section
    - Enabled: **Yes** 


![Interface Profile Quick Actions](images/wired-port-profile6.png)

16. Under the **802.1x > MAC-Based Authentication** Section
    - Enabled: **Yes** 

![Interface Profile Quick Actions](images/wired-port-profile7.png)



17. Select **Create**

![Interface Profile Quick Actions](images/submit-profile-configuration1.png)

18. This will add to the existing workspace and validate all of your inputs. You may see a spinning blue circle while the workspace is built. When completed that circle will turn **Green** and you can then Select **Close**

![Close Quick Action](images/submit-profile-configuration2.png)

19. Select the **Clipboard Icon** to review your workspace.

![Interface Profile Quick Actions](images/submit-profile-configuration3.png)

29. Select **Submit Workspace** to save the proposed interface profile.

*Note at this time no configuration changes are being made. You have only configured that Interface Profiles that we will use in the next next section to configure our interfaces*

![Interface Profile Quick Actions](images/submit-profile-configuration4.png)

20. Select **Exit Workspace**

![Interface Profile Quick Actions](images/submit-profile-configuration5.png)

**LAB SECTION COMPLETE**

---

## 5. Assigning Interface Profiles for AP and RPI

Assign the configured interface profiles to the switches access ports

1. Navigate to **Network Hierarchy**
    - Navigate through 
      - **Network**  
      - **Workshops** 
      - **IT-Bldg**  
      - **IDF1**

![Hierarchy Navigation](images/assign-profile-1.png)

2. Select the **Front Panel** tab

![Hierarchy Front Panel](images/assign-profile-2.png)

3. Select **Ethernet1** on **leaf1b**. Additional options will now be available on the right of the screen.
    - Under **Inferace Configuration** select **Configure**

![Set Interface Profiles](images/assign-profile-3.png)

4. A new **Interface Configuration** section should be available where you selected Configure. 
    - Profile: **Wired-RasPi**
    - Select **Save**

![Set Interface Profiles](images/assign-profile-4.png)



5. A new workspace has been generated.
    -  De-Select **Ethernet1** on **leaf1b**  
    - Select **Ethernet10** on **leaf1a** and **leaf1b**
    - Select **Configure**

![Set Interface Profiles](images/assign-profile-5.png)

6. A new **Interface Configuration** section should be available where you selected Configure. 
    - Profile: **Wireless-Access-Point**
    - Select **Save**

![Set Interface Profiles](images/assign-profile-6.png)

9.  Select the **Clipboard Icon** on you Worskspace Island Tool Bar

![Set Interface Profiles](images/assign-profile-7.png)

10. This will bring you to the Workspace Review Page.
    -  Review the proposed changes 
    -  Select **Submit Workspace**

![Set Interface Profiles](images/assign-profile-8.png)

11. Select **View Change Control**

![Set Wired Profile](images/assign-profile-9.png)

12. This will bring you to the Change Control. 
     - Select **Review and Approve**

![Set Wired Profile](images/assign-profile-10.png)

13. Review the proposed changes and select **Approve and Execute**

![Set Wired Profile](images/assign-profile-11.png)

14. Once the Change Control completes, that switches now have the interface profiles active in their configuration.

![Set Wired Profile](images/assign-profile-12.png)

**LAB GUIDE COMPLETE**
