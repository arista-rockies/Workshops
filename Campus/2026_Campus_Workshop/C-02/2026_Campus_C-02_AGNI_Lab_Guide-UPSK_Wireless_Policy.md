# Campus C-02 AGNI Lab Guide - UPSK Wireless Policy


![image1](images/CVCUE_logo.png)
![image2](images/AGNI_logo.png)


#### This Lab Guide:
Campus/2026_Campus_Workshop/C-02/Rockies Campus C-02 AGNI Lab Guide - UPSK Wireless Policy

---

## Table of Contents

[Full Lab Topology](#full-lab-topology)  
[POD Topology](#pod-topology)  

**NAC Lab #2 - Create UPSK Wireless Policy**
1. [Create Identity UPSK SSID](#1-create-identity-upsk-ssid)  
2. [Create UPSK Network and Segment](#2-create-upsk-network-and-segment)  
3. [Create an AGNI Local User and Enroll Personal Device](#3-create-an-agni-local-user-and-enroll-personal-device)  
4. [Create an AGNI Client Group](#4-create-an-agni-client-group)  

---

## Full Lab Topology

![image3](images/full-lab-topology.png)

---

## POD Topology


![image4](images/pod-lab-topology.png)
---

## NAC Lab #2 - Create UPSK Wireless Policy

---

### 1. Create Identity UPSK SSID:

1. Return to the **LaunchPad**, and select the **CV-CUE** tile, or go to your **CV-CUE** tab in your browser.

![image5](images/image5.png)

2. Next, we will modify the PSK SSID we created in the CV-CUE lab.

3. While on the **Corp** folder, Click on **Configure** and then **WiFi**

![image6](images/image6.png)

4. Next, click on the 3 Dots and select **Create a Copy** on the SSID **ATD-##-PSK** where **##** is a 2 digit character between 01-20 that was assigned to your lab/Pod

![image7](images/image7.png)

5. **Select - Currently Selected Folders** and then **Continue**.

![image9](images/image9.png)

6. Click on the **Pencil icon** in the new copied SSID to **Edit** the SSID.  

**NOTE**: The Profile Name will show **Copy of**

![image10](images/image10.png)

7. On the Basic Tab rename the SSID to **ATD-##-UPSK**, and copy the SSID Name and paste it in the Profile Name field.

![image11](images/image11.png)

8. Next, click on the Security Tab and change the Security Level to **WPA3 Transition Mode** - **USPK**

![image12](images/image12.png)

**NOTE**: For more information on UPSK click here: https://arista.my.site.com/AristaCommunity/s/article/Unique-PSKs

9. Next, Click on the **Access Control** tab.  Under **RADIUS Settings**, select **RadSec** and then **AGNI** for the Authentication and Accounting Servers, and select **Send DHCP Options and HTTP User Agent**.

![image14](images/image14.png)

10. Confirm the **Username and Password, Called Station, COA information**.

![image15](images/image15.png)
![image16](images/image16.png)

11. Click **Save**.

![image17](images/image17.png). 

**Please Read!**

12. **Only select the “5 GHz” option** on the next screen (**uncheck** the 2.4 GHz box if it’s checked), then click **Turn SSID On**.

![image18](images/image18.png)  

---

### 2. Create UPSK Network and Segment:

1. Return to the **LaunchPad**, and select the **AGNI - Trial** tile, or go to your **AGNI** tab in your browser.

![image19](images/image19.png)

2. Click on **Networks** and then **+ Add**.

![image20](images/image20.png)
![image21](images/image21.png)

3. Add the following:

- Name: **Wireless-UPSK**  
- Connection Type: **Wireless**  
- SSID: **ATD-##-UPSK**  
- Authentication Type: **Unique PSK (UPSK)**

4. **Click Add Network**

![image22](images/image22.png)

5. You should now see this listed in your **Networks**  .

![image23](images/image23.png)

6. **Next**, we will add a **Segment**.

7. Under Access Control, click on **Segments** and then **+ Add**

![image24](images/image24.png)
![image25](images/image25.png)

- Name: **Wireless-UPSK**  
- Description: **Wireless-UPSK**

8. Click on **+ Add Condition**

![image26](images/image26.png)

- Conditions: **Network:Authentication Type is UPSK**

**Note:** Conditions are always **MATCHES ALL**.

![image27](images/image27.png)
![image28](images/image28.png)
![image29](images/image29.png)
![image30](images/image30.png)
![image31](images/image31.png)

9. Click on **+ Add Action**

![image32](images/image32.png)

- Actions: **Allow Access**

![image33](images/image33.png)
![image34](images/image34.png)
![image35](images/image35.png)

10. Finally, click on **Add Segment**.

11. You should now see **Wireless-UPSK** in the list of segments.

![image36](images/image36.png)

---

### 3. Create an AGNI Local User and Enroll Personal Device

In this section you will create a local user and enroll the MAC of your device.

1. In AGNI, under Identity, click on **User** and then **+ Add User**.

![image37](images/image37.png)
![image38](images/image38.png)

2. Fill out the sections.  Use **Arista01!** for the password.

3. **Disable** - User must change password at next login:


![image40](images/image40.png)

4. Click **Add User**

**NOTE: You will notice that Password has now changed to UPSK Passphrase**

5. **Copy** and write down or save to text file the new **UPSK Passphrase**.

![image41](images/image41.png)

6. Next, connect your client to **ATD-##-UPSK**using your **UPSK Passphrase**.

7. Click on **Monitoring - Sessions** and validate your device connection.

![image42](images/image42.png)
![image43](images/image43.png)

8. Next, validate your device by clicking on **User** and then **Users.  Select your user**.

![image44](images/image44.png)

9. Click on **Show Clients**

![image46](images/image46.png)

---

### 4. Create an AGNI Client Group

In this section, you will simulate your device as an IoT device.

1. **Disable and forget previously saved lab networks** so your wireless connection on your test device does not auto connect.  

2. Under your user client list, **Delete** your device.

![image47](images/image47.png)
![image48](images/image48.png)
![image49](images/image49.png)

2. Next, you will **add your client device as an IoT device in a Client Group.**

First, we will need to create the Client Group.

3. In **AGNI**, under **Identity**, click on **Client Groupsv and then **+ Add**.

![image50](images/image50.png)
![image51](images/image51.png)

- Name: **Corp Approved Devices**  
- Description: **Corp Approved Devices**  
- User Association: **Not user associated**  

4. **Enable the Group UPSK.  Copy the UPSK Passphrase**

5. Then click on **Add Group**

![image52](images/image52.png)
![image53](images/image53.png)

6. Next, connect your client to **ATD-##-UPSK** using the Client Group UPSK Passphrase.

7. Click on Sessions and validate your device connection.

![image54](images/image54.png)
![image55](images/image55.png)

8. Next **Click on your Client**.

![image56](images/image56.png))
![image57](images/image57.png)

**Notice your Client Group.**  Here you have the option to change the Client Group your device belongs to.

![image58](images/image58.png)

9. Next, delete your device from the **Client Group - Corp Approved Devices.**

![image59](images/image59.png)
![image60](images/image60.png)

10. Next, under Identity, click on **Clients** and then **+ Add Client**.

![image61](images/image61.png)
![image62](images/image62.png)

11. Select the Client Group: **Corp Approved Devices**

12. Add in the **MAC Address of your test device** like your phone that is not randomized.

13. Then select **Add Client**

![image63](images/image63.png)

**You should see your Client was added to the Group.**

![image64](images/image64.png)

14. **Validate and Verify your connection using the Client Group UPSK Passphrase.**

![image65](images/image65.png)
![image66](images/image66.png)
---

**NAC LAB #2 COMPLETE**
