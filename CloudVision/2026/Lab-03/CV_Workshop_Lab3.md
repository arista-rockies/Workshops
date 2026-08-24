# CloudVision Lab 03
## Inventory and Topology
![CloudVision](images/cv-logo.png)

## This Lab Guide:

[CloudVision Workshop Lab Guide 03 - Inventory and Topology](https://github.com/arista-rockies/Workshops/blob/main/CloudVision/2026/Lab-03/CV_Workshop_Lab3.md)

---

## Table of Contents
1. [Lab Topology](#1-lab-topology)
2. [Accessing the Lab](#2-accessing-the-lab)
3. [Lab Details](#3-lab-details)

---

# 1. Lab Topology

![Full Lab Topology](images/a-topology.png)

---

# 2. Accessing the Lab

VERY ELABORATE LOGIN SECTION TO FOLLOW - Need to verify how we are doing this first. Here is a picture of a dog as a placeholder.

![Login](images/login-1.png)

---

# 3. Lab Details

## Lab Overview
Use studios to build some stuff

### Building the Fabric

1. Navigate to Studios **Provision > Studios**

![Studio Navigation](images/studio-nav.png)

2. Select the **Campus Fabric (L2/L3/EVPN)** Studio

![Campus Fabric Studio](images/cf-studio.png)

3. Under **Campus Fabrics** section
   - Select **+ Add Campus Fabric**
   - Name the fabric **Workshop**
   - Select the **+ Create "Workshop"**
   - Select the Blue **>** 

![Create Campus Fabric](images/create-campus-fabric.png)

4. Create a Campus Pod
   - Select **+ Add Campus Pod**
   - Name your Campus-Pod  **+ Create "CAMPUSNAME"**
   - Select the Blue **>**

![Create Campus Pod](images/create-campus-pod.png)

5. Design
   - Select the dropdown under **Campus Type**
   -  Select **L2**

![L2 Campus](images/campus-L2.png)

6. Add The Spines 
   - Select **+ Add Spine**
   - Locate and Select the Spine
   - A pop up will be presented to add tags to the device. Select **Confirm** 
   - Repeat step 6 for the second spine

![Add Spines](images/add-spines.png)

7. Add Access-Pods
    - Select **+ Add Access Pod**
    - Input a PodName of your Choosing
    - Select **+ Create "PodName"**
    - Repeat Step 7 to create a 2nd Access-Pod

![Add Access Pods](images/add-access-pods.png)

8. Navigate to the Access-Pod by sselecting the Blue **>** on the first pod created

![Add Access Pods](images/enter-access-pod.png)

9. Add Devices to Access-Pods
   - Select **+ Add Device**
   - Select **Leaf1a** 
   - A pop up will be presented to add tags to the device. Select **Confirm** 
   - Repeat steps in step 9 to add the 2nd leaf

![Add Leafs](images/pod-add-leaf.png)

10. Add Member Leaf
    - Within the same Access-Pod select **+ Add Member Leaf**
    - Select the **Member Leaf Device**
    - A pop up will be presented to add tags to the device. Select **Confirm** 

![Add Member Leaf](images/pod-add-member-leaf.png)

11. Using the Studios Breadcrumbs locate the dropdown next to the Access-Pod. Select the 2nd Access-Pod

![Switch to Second Pod](images/pod-nav.png)

12. Add Device to 2nd Pod
    - Select **+ Add Device**
    - Select **Leaf2a** 
    - A pop up will be presented to add tags to the device. Select **Confirm** 

![Add Leafs](images/pod-add-leaf2.png)

 13. Add Node-IDs
     - Using the Studios Breadcrumbs, select **Campus-Pod:Campus**
     - Locate **Design** section and select the **Lighning Bolt**
       - *This will auto assign node-ids to devices*

![Add Leafs](images/node-id.png)

---

### Adding VLANs

1. Navigate back to the beginning of the Campus Fabric Studio
   - Locate the Section labeld Campus Services (Non-VXLAN)
   - Select the **>** next to Workshop


![Add VLANS](images/add-vlan-1.png)

2. Select the **>** next to the CampuPod

![Add VLANS](images/add-vlan-2.png)

3. Under **Campus Type** Select **L2**

![Add VLANS](images/add-vlan-3.png)

4. Create Vlans
   - Locate the VLAN section and select **+ Add VLAN**
   - Input a VLAN ID of your Choosing
   - Continuing this process add 2 Additional **VLAN IDs**
   - Select the Blue **>** next to the first VLAN created

![Add VLANS](images/add-vlan-4.png)

5. Input the Following
   - Routed VLAN **Routed**(DEFAULT)
   - Enabled **Yes**
   - Name **Choose a Name**

![Add VLANS](images/add-vlan-5.png)

6. VLAN Assignment
   - In the **Pods** section select **+ Add Pod**
   - Add Both Pods

![Add VLANS](images/add-vlan-6.png)

7. Provide a Unique IP subnet in CIDR Notation
   - *The first available IP address will be used as the configured IP address*

![Add VLANS](images/add-vlan-7.png)

8. Using the Studios Breacrumbs Select the Dropdown Next to the VLAN ID to Navigate to another VLAN

![Add VLANS](images/add-vlan-8.png)

9. Repeat the previous steps for each VLAN. 
   - Assign the 2nd VLAN only to the first POD
   - Assing the 3rd VLAN only to the second POD
   - Ensure each VLAN uses Unique IP Subnets

10. After all 3 VLANs have been added locate the **Workspace Island** toolbar at the bottom of you screen. Select the **Clipboard Icon** to Review your Workspace.

![Workspace Island](images/wsi-review.png)

11. After the Workspace has finished building, review the proposed configuration and Select **Submit**

![Workspace Review](images/ws-review.png)

12. Select **View Change Control**

![View Change Control](images/view-cc.png)

13. You are now presented with a Change Control that will push the configuration to the devices.
    - Select **Review and Approve**

![Review Change Control](images/review-cc.png)

14. Select **Approve and Execute**

![Review Change Control](images/execute-cc.png)

15. When the change control is completed succesfully the intended configuration will be present on the devices.

![Complete Change Control](images/cc-complete.png)

---

### Order of Operations
In this lab seciton we are going to demonstrate an example of how the order of operations works is handled in Studios
1. Navigate to Studios **Provision > Studios**

![Studio Navigation](images/studio-nav.png)

2. Locate and Select the Studio named **Date and Time**

![Studio Date and Time](images/dt-studio.png)

3. Under **Device Time Zone**
   - Select **+Add Device Time Zone**
   - Under **Device Time Zone** add your Campus Devices using  **Campus-Pod:** Tag you created earlier
   - Under **Select Time Zone** Select anything other than MST

![Date and Time Timezone](images/dt-time-zone.png)

5. Select the **Clipboard** icon on Workspace Island toolbar at the bottom of your screen.

![Date and Time Review Workspace](images/dt-wsi-review.png)

6. After the Workspace has finished building you should see not proposed configuration changes.
   - Close the Workspace Review Window

![Date and Time No Changes](images/dt-no-changes.png)

7. Select the blue **Studios** breadcrumb to return to the main Studios Page

![Date and Time Studios Navigation](images/dt-back-to-studios.png)

8. Open the **Static Configuration** Studios

![Date and Time Static Configuration](images/dt-static-config.png)

9. Select the top container in your heirarchy structure where the configlet **CampusA_Base** is applied.
   - Locate the **clock timezone** command in the static configuration **Line14**
   - Add a **!** to the beginning of that line to comment out the command

![Date and Time Static Configuration](images/dt-static-changes.png)

11. One again select the **Clipboard** icon on Workspace Island toolbar at the bottom of your screen.

![Date and Time Review](images/dt-wsi-review2.png)

12. Now that we have removed the static configuration line, we should see the proposed configuration change for the new timezone.
    - Select Submit 

![Date and Time Review](images/dt-ws-changes.png)  

13. Select **View Change Control**

![Date and Time Review](images/dt-view-cc.png)  

14. Select **Review and Approve**

![Date and Time Review](images/dt-review-approve.png)  

15. Select **Approve and Execute** to push the configuration to the devices

![Date and Time Approve/Execute](images/dt-approve-execute.png)  

15. When the Change Control is complete, you have now succesfully pushed the date and time to the devices.

![Date and Time Change](images/dt-cc-complete.png)  

---


**LAB GUIDE COMPLETE**
