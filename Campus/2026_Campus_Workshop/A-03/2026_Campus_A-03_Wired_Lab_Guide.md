# Campus A-03 Wired Lab Guide

## Day-2 Operations, Dashboards, and Events

![CloudVision](images/CVP_logo.png)

## This Lab Guide:

[Campus A-03 Wired Lab Guide - Day-2 Operations, Dashboards, and Events](https://github.com/arista-rockies/Workshops/blob/main/Campus/2026_Campus_Workshop/A-03/2026_Campus_A-03_Wired_Lab_Guide.md)

---

## Table of Contents

1. [Full Lab Topology](#1-full-lab-topology)
2. [POD Topology](#2-pod-topology)
3. [Accessing CloudVision as a Service](#3-accessing-cloudvision-as-a-service)
4. [Operations: Add a VLAN](#4-operations-add-a-vlan)
5. [Rollback a Change Control](#5-rollback-a-change-control)
6. [Dashboards (Built-in and Custom)](#6-dashboards-built-in-and-custom)
7. [Events](#7-events)
8. [Customize Notifications](#8-customize-notifications)

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

## 4. Operations: Add a VLAN

Adding a VLAN is a common provisioning task. Let’s use the existing Campus Fabric Studio to add an incremental configuration (add a VLAN). This VLAN will be specific to your pod and not routable outside.

1. Select **Provisioning**, then **Studios**

![Provisioning Studios](images/provisioning-studios.png)

2. Create a new Workspace 
     - Select the **+** on the Workspace bar on the bottom of the page
     - name the workspace  “<add-vlan2##>” where ## is your pod number. Examples:

        Pod 1 = VLAN 201  
        Pod 2 = VLAN 202  
        …  
        Pod 13 = VLAN 213  
        etc.

![Create Workspace](images/create-workspace.png)

3. Once the workspace is created, select **Campus Fabric (L2/L3/EVPN)** studio. 

*If the Studios main page is not present you may have to select the blue Studios breadcrumb towards the top left of the page*

![Campus Fabric Studio](images/campus-fabric-studio.png)

4. Within the Campus Fabric studio, validate that the Device Selection still applies to All Devices. Select the **down arrow** under **Device Selection**

![Device Selection All Devices](images/device-selection-all.png)

5. Within the **Campus Services (Non-VXLAN)** select the **Campus:Workshop expand arrow** on the right

![Campus Services Expand](images/campus-services-expand.png)

6. Add new VLAN and add to the **IT-Bldg** Campus POD.

     -  Within the Campus: Workshop section, click the Campus-Pod: **IT-Bldg name** or the **expand arrow** on the right

![Campus Pod Expand](images/campus-pod-expand.png)

7. click the **+ Add VLAN** 

![Add VLAN Button](images/add-vlan-button.png)

8. In the newly created section under **VLAN ID** input VLAN number **200+POD#**, click the **arrow expand** on the right

![Expand New VLAN](images/expand-new-vlan.png)

9. Createing a new VLAN
     * For the purpose of this lab we will create an L2 VLAN. Select **L2 Only** 
     * Add a **name** for your VLAN with **no spaces** 

*Notice the avaialble inputs change based on L2 Only and Routed selections*

![Customize VLAN Name](images/customize-vlan-name.png)

10. Assigning VLANs to devices
    * Select **+ Add Pod**
    * Select the **dropdown** from the new line that was created
    * Select **IDF1**

![Add Pod IDF1](images/add-pod-idf1.png)

You can skip entries for all of the remaining vlan configuration sections.

11. Select the **Clipboard Icon** on the bottom of the page to **Review Workspace** and see the proposed changes.

![Review Workspace](images/review-workspace.png)

12. Notice that the Studio is adding the VLAN to all devices within the Pod as well as adding the newly created VLAN to the trunk interfaces.

![Review Workspace2](images/review-workspace2.png)

13. Once you review the changes, click **Submit Workspace**

![Submit Workspace](images/submit-workspace.png)

14. Click **View Change Control**

![View Change Control](images/view-change-control.png)

15. Review the Change Control and select **Review and Approve**

![Review and Approve](images/review-and-approve.png)

16. If necessary toggle the Execute Immediately button and select **Approve and Execute**

![Approve and Execute](images/approve-and-execute.png)

17. Verify the VLAN has been added to the device configuration by using the Devices Comparison function.

     - Select ***Devices** and then **Comparison** menu
  
 ![Navigate Comparison](images/navigate-comparison.png) 

18. Time Comparison
    - Select a **Time Comparison**
    - Choose a device from the list. example leaf1a
    - Select a **time period**, for example 30 minutes ago 
    - Click the **Compare** button 

![Devices Comparison](images/devices-comparison.png)

19. Time Comparison (Continued)
    - The first screen presented shows the overview:
    - Select the **Configuration** section

![Comparison Overview](images/comparison-overview.png)

*Note: Notice that the configuration has been updated. Feel free to explore other comparisons by feature. Since this VLAN was localized only, no new IP routes or MAC addresses should be learned.*

![Config Comparison](images/config-comparison.png)


**LAB SECTION COMPLETE**

 In the next lab section you will see how to roll back a previous change control

---
## 5. Rollback a Change Control

A common operational task is to roll back a specific configuration and restore back to previous state. You may need to do this for all devices affected by a change, or only a subset of devices under troubleshooting.

CloudVision change controls allow this flexibility for granular change management per device and fleet-wide

Let’s roll back the change control we used to add a VLAN via Studios.

1. First go to **Provisioning** then **Change Control** menu. Select the **completed change control corresponding to your VLAN addition**

![Select Change Control](images/select-change-control.png)

2. Click the **Rollback** button

![Rollback Button](images/rollback-button.png)

3. In the next screen, **select all the devices** and click **Create Rollback Change Control**

![Create Rollback Change Control](images/create-rollback-cc.png)

4. Verify the Configuration Changes section by clicking **View Diff**  Once you have reviewed the change, click the **Review and Approve** button

![View Diff](images/view-diff.png)

5. You’ll be presented with one more opportunity to review the changes. Select **Execute Immediately** if not already toggled on and then click **Approve and Execute**

![Execute Rollback](images/execute-rollback.png)

6. Monitor the change control for completion to ensure the added VLAN is cleaned up on both switches.

![Rollback Completed](images/rollback-completed.png)

*You have now successfully added a VLAN through Studios and then rolled back that change across all switches.*

A rollback of a change control does not change the CloudVision Designed Configuration. Currently your devices will show as out of compliance. 

Let's update the Studio so that current running configuration matches the designed configuration.

7. Select **Provisioning**, then **Studios**

 ![Provisioning Studios](images/provisioning-studios.png)

8. Create a new Workspace 
     - Select the **+** on the Workspace bar on the bottom of the page
     - name the workspace  “<remove-vlan2##>” where ## is your pod number. Examples:

        Pod 1 = VLAN 201  
        Pod 2 = VLAN 202  
        …  
        Pod 13 = VLAN 213  
        etc.

![Campus Fabric Studio](images/studio-remove-vlan1.png)

9. Once the workspace is created, select **Campus Fabric (L2/L3/EVPN)** studio. 

![Campus Fabric Studio](images/campus-fabric-studio.png)

10. Within the **Campus Services (Non-VXLAN)** select the **Campus:Workshop expand arrow** on the right

![Campus Fabric Studio](images/campus-services-expand.png)

11. Within the Campus: Workshop section, click the Campus-Pod: **IT-Bldg name** or the **expand arrow** on th

![Campus Fabric Studio](images/campus-pod-expand.png)

12. Locate the **VLANs** section. Click the **Trash Can** icon next to VLAN **2[POD#]**

![Campus Fabric Studio](images/studio-remove-vlan2.png)

13. Select the **Clipboard Icon** in your Workspace Island bar to review your workspace.

![Campus Fabric Studio](images/studio-remove-vlan3.png)

14. Because we have already removed **VLAN 2[POD#]** from the running configuration, there should be no proposed changes to the network. Select **Submit Workspace**

![Campus Fabric Studio](images/studio-remove-vlan4.png)

15. Since no changes are occurring there is no change control created. Select **Exit Workspace**

![Campus Fabric Studio](images/studio-remove-vlan5.png)

*Now your running configuration and CloudVision's Designed configuration are aligned*

**LAB SECTION COMPLETE**
---

## 6. Dashboards (Built-in and Custom)

Dashboards are an important way to visualize commonly requested information. This lab section shows you how to navigate the built-in dashboards and customize your own.

### Built in Dashboard: Campus Health Overview

1. Navigate to **Dashboards** to arrive at the Dashboards landing page.

![Dashboards Landing Page](images/dashboards-landing.png)

2. Select the built-in **Campus Health Overview dashboard**

![Campus Health Overview](images/campus-health-overview1.png)

3. You’ll be presented with a curated selection of common campus related monitoring tools

![Campus Health Overview](images/campus-health-overview2.png)
*Note: We will explore the Quick Actions interactive functions of this dashboard in another lab section.* 

4. Feel free to explore the Campus Health dashboard briefly and then navigate back to the Dashboards landing page by selecting **Dashboards** in the upper left.

![Explore Dashboards](images/explore-dashboards.png)

### Built in Dashboard: “Device Hardware”

1. Next, Select the **Device Hardware** dashboard

![Device Hardware Dashboard](images/device-hardware-dashboard.png)

2. By default, this dashboard selects all devices. 
  
  ![Device Hardware Dashboard2](images/device-hardware-dashboard2.png)
  
3. Change the dashboard to select only **leaf1a** by deleting the current query device:*. Replace with the query **device:campus-pod[pod#]leaf1a**

![Device Query Edit](images/device-query-edit.png)

4. Once you’ve selected an individual device, the dashboard will filter to results for only this device.

![Dashboard Filter](images/dashboard-filter.png)

5. Navigate back to the Dashboards landing page by clicking **Dashboards** in upper left.

![Dashboard Navigate](images/dashboard-navigate.png)

---
 ### Customized dashboard.

1. Click the **New Dashboard** button.

![New Dashboard](images/new-dashboard.png)

2. New Dashboard
    - Select the **pencil** next to Untitled dashboard
    - Provide a useful name for the Dashboard, such as **Workshop Dashboard**

![Rename Dashboard](images/rename-dashboard.png)

3. Next, let’s add some metrics to display from the workshop devices.

![Change Metrics to Summaries](images/add-metrics.png)

4. Within new metrics tile now added to your dashboard, select either the **3 dots > Configure** or **Click to Configure**

![Metrics Configure](images/metrics-configure.png)

5. Within the right side menu bar, locate the device metric **Memory > Memory Usage** 

![Metrics Configure](images/metrics-configure2.png)

6. Review the availabe Visualization options. Select each of them to determine which would best suit your personal preference. 

*Note: sometimes when changing the visualization you will have to re-select the metric you would like displayed*

![Metrics Configure](images/metrics-visualization-table.png)

![Metrics Configure](images/metrics-visualization-bar.png)

![Metrics Configure](images/metrics-visualization-line.png)

7. Close the dashboard editor by selecting the **X** towards the top right of the **Configure Metric Panel**

![Close Metrics Configure](images/close-metrics-configure.png)

8. Create another metric by selecting **Metrics** panel and configure the new dashboard tile.

![Metrics Configure](images/metrics-configure3.png)

9. Within the Configure Metrics Panel menu,
   - Select the dropdown under **Data Sources**
   - Select **Interfaces**

![Metrics Configure](images/metrics-configure4.png)

10. Additional Dashboard Tile
    - Under the available metrics scroll down and locate **Bitrate In** and **Bitrate Out**
    - Under Dataset select **Ethernet13** on both **leaf1a and leaf1b**. Ensure between each interface you include a **|** or an **OR** so that both interface will be displayed.

![Metrics Configure](images/metrics-configure5.png)

11. Interface Dashboard Tile
    - In the dashboard tile select the Pencil Icon and change the tile name to **Pod Uplinks Bitrate**
    - Select the visualization style that you believe best displays this data

*Note: sometimes when changing the visualization you will have to re-select the metric you would like displayed*

![Metrics Configure](images/metrics-configure6.png)

12. Dismiss the customization menu with the **X** button in upper right

![Close Metrics](images/close-metrics.png)

*You can resize an individual tile by dragging the lower right corner. To move the tile location you can drab the op middle of the tile and re-locate it to it's desired location.*

*Take some time to explore additional dashboard tile options*

![Moving Tiles](images/moving-tiles.png)

13. When done save and complete the dashboard customization by clicking the **Done** button in upper menu bar

![Done Dashboard](images/done-dashboard.png)

### Exporting and Importing Dashboards Sharing your Dashboard across Cloudvision systems!

1. In the upper right corner, select the **three-dots** menu and click Export as JSON
   - Click **Download** in the lower right corner. This will download a file you can share with others.

![Export JSON](images/export-json.png)

2. To demonstrate the ability to import a dashboard we will delete our custom dashboard
    - After exporting your dashboard in the previous step
    - Select the **Dashboard** breadcrumb at the top of the page
    - Select the Check Box next to the **Workshop Dashboard**
    - Select the **Delete**

![Delete Dashboard](images/del-dashboard.png)

3. Import Dashboard
    - In the top corner select **Import**
    - Click **Select File**
    - Locate the dashboard downloaded to your local PC.
    - Select **Upload**

![Import Dashboard](images/import-dashboard1.png)

4. Import Dashboard (Continued)
    - Review the Dashboard Name and the Status displays **Ready to Upload**
    - Select **Import**
    - Select **Finish**

![Import Dashboard](images/import-dashboard2.png)


**LAB SECTION COMPLETE**

---

## 7. Events

In this section, we will explore the CloudVision Events. We will reivew the tools and filters to help process and manage critical errors versus informational data.

1. First navigate to the **Events** section in CloudVision:

![Events Menu](images/events-menu.png)

2. Filter Events
    - To filter and only display more recent events, select the dropdown next to the displayed timeframe
    - Select **1 Hour**
    - You can select how the events are displayed in the menu by selecting the icon for either a **graphical view** or a **table view**

![Change Timeframe](images/change-timeframe.png)


3. Focusing on the Event List next, Note the **Export** button to download the current Event list as CSV. Notice you can **Download All Events** or **Only Selected**:

![Export Events CSV](images/export-events-csv1.png)

4. Select the Gear icon to toggle Event List **Roll Up**. *This setting combines repeated events into groups.* Toggle this On and Off, watch the effect this has on the list of Events.

![Event Rollup Toggle](images/event-rollup-toggle.png)

5. Next, utilizing the Event Filters on the right you can reduce the amount of data displayed.

    - Ensure that **Critical** and **Warning** are the only highlighted event severity by toggling off all other severity levels.
    - Select the dropdown under Type. Search for **Device Clock Out of Sync** and **Unexpected Link Failure**

*We are now only seeing events associated with the filter we have established*

![Severity Filter](images/severity-filter.png)

6. Acknowledge and Unacknowledging events

    - Review the events displayed. You can acknoledge events by selecting the radial button next to the displayed event.
    - Select **Acknowledge X**
    - A pop up window will be displayed. You can **Acknowledge** these events and include a note to provide additional context on root cause or fix action.

![Acknowledge Events](images/acknowledge-events.png)


7. Acknowledged events are not deleted from the event list, only flagged as acknowledged and can be referenced by changing the filtered Acknowledgement State. Click Acknowledgement State and select Acknowledged

![Acknowledgement State](images/acknowledgement-state.png)

8. You can also **Un-acknowledge** an event.
    - While reviewing the Acknowledged events, select the check box next to the events. 
    - Select **Unacknowledge X**
    - Select **Unacknowledge**

![Unacknowledge Events](images/unacknowledge-events.png)

**Events and filtering lab section complete!**

---

## 8. Customize Notifications
In this section we will show you how to customize the notifications that can be generated (e.g. email, chat, SNMP, Syslog, etc) from the events.

### Configure SendGrid email service.

1. Navigate to the **Events** menu

![Events Menu](images/events-menu.png)

2. Navigate to Notificaiton
    - Select the **Configure** dropdown 
    - Select **Event Notifications** 

![Notifications Button](images/notifications-button.png)

3. Add Receiver
    - Select **Receivers**
    - Select **+ Add Receiver**

![Add Receiver](images/add-receiver.png)

4. Receiver Configuration
    - Provide a name for the reciever Example: **SendGrid for Campus Workshop**
    - Select **+Add Configuration**
    - Select **SendGrid** from the list

![SendGrid Configuration](images/sendgrid-configuration.png)

5. Receiver Configuration(Continued) 
    - Provide your email address under **Recipient Email**
    - Select **Save**

![SendGrid Configuration](images/sendgrid-configuration2.png)

6. Configure Rules to identify what events are sent
    - Select **Rules** from the Menu
    - Select **+ Add Rule**

![Add Rule](images/add-rule.png)

7. Configure Rule Conditions
    - Select **+ Device**
    - under the dropdown select **leaf1a**

![Rule Device Selection](images/rule-device-selection.png)

8. Select **+ Event Type** 
    - Select Events **Change Control Created, Change Control Executed, Change Control Failed, Device Designed Configuration Changed, Change Control Succeeded, Device Clock Out of Sync, and Device Stopped Streamining** feel free to add additional event types
    - Under the dropdown for Receiver Select **SendGrid for Campus Workshop**

![Add Event Type](images/add-event-type.png)

9. Make sure to save your changes in this screen with the **Save** button along the top of your screen.

![Receiver Save Changes](images/receiver-save-changes.png)

10. Now test your new receiver and rule.

    - Select **Status** on the left navigation pane
    - Under Event Type locate **Device Stopped Streaming** in the dropdown
    - Under Devic select **Leaf1a** from the dropdown
    - Select **Send Test Notification**

![Test Notification Sender](images/test-notification-sender.png)

11. After a minute or two, you should receive the email alert at the email address you configured in the Receiver.

![Test Notification Email](images/test-notification-email.png)

**Congratulations, you’ve completed the Event Notification Lab!**


**LAB GUIDE COMPLETE**

---
