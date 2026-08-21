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

5. Build Workspace
6. Review Configuration
8. Submit Workspace
7. Push CC
### Order of Operations
We are going to demonstrate how the order of operations works in Studios
1. Return to Studios **Provisioning > Studios**
2. Make have to select **Active Studio**
3. Navigate to the **Date and Time** Studio
4. Under **Device Time Zone**
  - Select **device:**
  - Under **Select Time Zone** Add anything other than MST
5. Build Workspace (No Changes shoudld be present)
6. Go to **Static Configuration Studio**
7. Remove the Timezone from the Base configurat **SHOULD WE HAVE A STATIC THAT IS ONLY TIMEZONE?**
8. Build (Maybe need a rebuild?)
9. Select the **?** in CVP Top Menu
   - Select the magnifying class
   - Search  **Configuration Hierarchy** and click the link
   - Review the Image
10. Push the workspace with the Time
11. Push CC


---


**LAB GUIDE COMPLETE**
