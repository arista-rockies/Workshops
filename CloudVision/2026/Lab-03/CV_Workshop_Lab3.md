# CloudVision Lab 03
## Campus Fabric Studio
![CloudVision](images/cv-logo.png)

## This Lab Guide:



[CloudVision Workshop Lab Guide 03- Inventory and Topology ](NEEDLINK!!!!)

---

## Table of Contents
1. [Lab Topology](#1-lab-topology)
2. [Lab Topology](#2-accessing-lab)


---

# 1. Lab Topology

![Full Lab Topology](images/lab-topology.png)

---
# 2. Accessing Lab

# 3. Accessing CloudVision as a Service

# 4. Campus Fabric Studio
Configure the Campus Fabric Studio
1. Navigate to Studios **Provision > Studios**
2. Select the **Campus Fabric (L2/L3/EVPN)** Studio
3. Under Campus Fabrics
   - Create call Workshop
   - Select the **>** 
   - Create a Campus POD for Campus A
   - Type **L2**
   - Add The Spines
   - Add to Access-Pods
     - One for Leafa/b/c
     - One for Leaf2
       - Add devices to leaf pods
       - Leafc will be added as a Member Leaf
4. Navigate back to the beginning of the Campus Fabric Studio
  - Locate the Section Campus Services (Non-VXLAN)
  - Select the **>** next to Workshop
  - Select the **>** next to the CampuPod
  - Create some VLANs
    - A few routed
      - Include a subnet for each L3 VLAN
    - A few L2 Only
      - Provide VLAN Names
      - Assign all VLANs to both AccessPods
5. Build Workspace
6. Review Configuration
8. Submit Workspace
7. Push CC
# 5. Order of Operations
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
