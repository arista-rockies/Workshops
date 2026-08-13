# CloudVision Lab 02
## Static Configuration Studio
![CloudVision](images/cv-logo.png)

## This Lab Guide:

[CloudVision Workshop Lab Guide 02- Inventory and Topology ](NEEDLINK!!!!)

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


# 4. Static Configuration Studio
The static configuration studio allows you to apply static configuration "configlets" to devices. Configlets can be assigned directly to a device or to a container. Containers are arranged in a hierarchical structure. This allows devices lower in the heirarchy to inherit all off the configlets applied in containers higher in the heirarchy. The end result is the complete designed configuration of the device within the static configuration studio. 

There is not right or wrong way to design this heirarchy and each organization may have a different methodolgy to accomplish this. 
# 5. Lab Exercise
1. Navigate to Provisioning > Studios

2. Select the **Static Configuration Studio**

3. Begin your Heirarchy design by selecting **+Configuration Container**
  - Create a Tagging Structure using Key Vlaue : Pair
    - The Key:Value Tag by default will be the name of the container you create.

  - Develop your own heirarchy how you see fit. In this environment there is only a base configuration that all apply to all devices in CampusA and a unique configlet that will be applied to each device. Below are 2 examples that accomplish the same end result. Developing a more in depth heirarchy provides additional locations that configuration could be applied.
  *NOTE: Avoid using the Devices:All Tag in your heirarchy as we will have CampusB that will not utilize the static configuration studio.*

4. After you have created your heirarchy structure;
  - Selec the root container
  - On the right side of the screen select **+Configlet**
  - Select **Configlet Library**
  - Locate and Select the configlet **CampuA_Base**.
  - Select **Assign**

5. Assign all devices to their intended containers.
  - locate the container that each device belongs under. 
  - In each devices container select the **3 dots**. Then select **Add Device**
  - All Devices that have been registered in the Inventory and Topology Studio are available for selection
  - Select the device(s) that will be added under that container in the heirarchy. Select **Add**
  - Ensure that every device in CampusA is associated with the Base Configlet 

  6. Accomplish the following for each device within CampusA
   - Select the device. 
   - Select **+ Configlet**
     - Select **Configlet Library**
   - The per device configlets have been named based on the serial number of the device. Locate the **mgmt_$Device** configlet to associate to your device.
   *Note: This is going to update the hostname. If you are so inclinded to use your own hostnames you can edit the hostname field in each device specific configlet*
   
   7.After all devices have their per device configlet and base configlet associated, select the **Clipboard Icon**

   8. After the Workspace has finished building, review the configuration proposed. 

   9. After you have reviewed the proposed configuration, select **Submit Workspace**

   10. Select **View Change Control**

   11. You are now presented with a change control that will push the configuration to the devices. 

   12. Select **Review and Approve**

   13. Select **Approve and Execute**

   14. The devices taken out of Zero Touch Provisioning mode and will relaod. After they have relaoded (may take a few minutes). 


---


**LAB GUIDE COMPLETE**
