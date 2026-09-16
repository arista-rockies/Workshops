# CloudVision Lab 05
## Campus Fabric Studio
![CloudVision](images/cv-logo.png)

## This Lab Guide:



[CloudVision Workshop Lab Guide 05- Inventory and Topology ](NEEDLINK!!!!)

---

## Table of Contents
1. [Lab Topology](#1-lab-topology)
2. [Lab Topology](#2-accessing-lab)


---

# 1. Lab Topology

![Full Lab Topology](images/a-topology.png)

---

# 2. Accessing the Lab

To authenticate to CloudVision you will need to visit the following page:

[CloudVision Auth](https://labs.arista.com/ignition/event/9gk8a4d3)

Each attendee will be provided with a unique access key. Enter you access key and select the Blue Arrow


![Ignition Login](images/ignition-login.png)

After succesfully authenticated you will should see **CVaaS** avaialble under Services. Selecting the CVaaS tile will authenticate you directly to the Lab CVaaS environment

![Ignition Login](images/cvaas-tile.png)

![CVaaS Home](images/cvaas-access.png)

---

# 3. Lab Details

## Lab Overview

In this lab, we will setup CloudVision's tags and Events system to create a customized email alert when leaf to spine uplinks or specific devices go offline.

### Customize Events and Notifications

Set customized tags
  -  Create a new workspace
  -  Navigate to **Provisioning > Tags**

![Tags Navigation](images/tags-nav.png)

- Select Create Tag
![Create Tag](images/create-tag.png)

- Set a new tag Name and a value for devices you wish to receive an alert for.
- Create the tag as Assignment Type - Device tag
- Click Create
![Device Tag](images/dev-tag.png)

- Next, click the **"+ Assign"** (right side) 
![Assign Tag](images/assign-tag.png)

- Assign CampusB-Leaf2A device to this tag and click Assign
- ![Leaf2A-B Tag](images/leaf2a-tag.png)

- Notice the Leaf2A is now a member of the Associated Devices Column
- Additionally, purple diamonds indicate which tags have modifications. This indicator is helpful when making changes to multiple tag keys within a single workspace. 
- ![Associated Tag](images/associated-tag.png)

- Next, Verify Interface Tags by selecting the Interface Tags button (upper left)
- ![Interface Tag](images/int-tag.png)

- Within the Interface Tags tree, browse for **Link-type** expand the key and then select **Uplink** value.
- This view displays the tags which are auto-assigned by the provisioning process
- ![Uplink Tag](images/uplink-tags.png)

In the Tag Selected Column on the right, verify your CampusB-Leaf2A device shows its uplink interfaces as members.
- ![Uplink Tag Verified](images/uplink-verified.png)

- Note -- if you desire, your own custom interface tags can be set to further customize filtering events and dashboards by interface tags--for example you may wish to tag an application which uses these infrastructure components. Since we are using one of the automatically provisioned interface tags, we know it will get configured for us on all future devices following the same provisioning procedure.

- Now that you have verified the custom device tag and auto-assigned interface tags are in place, review and submit your workspace. No studios are modified, only a single device tag update.
- ![Submit Tag Workspace](images/submitws-tag.png)

---


**LAB GUIDE COMPLETE**
