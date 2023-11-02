from pyVmomi import vmodl, vim
from pyVim.connect import SmartConnect, Disconnect
from yaml import dump, Dumper
import os

LINUX_USER=os.getenv("LINUX_USER")
LINUX_KEY_PATH=os.getenv("LINUX_KEY_PATH")
LINUX_EXECUTOR=os.getenv("LINUX_EXECUTOR")
LINUX_AUTHENTICATION=os.getenv("LINUX_AUTHENTICATION")

WINDOWS_USER=os.getenv("WINDOWS_USER")
WINDOWS_PASSWORD_PATH=os.getenv("WINDOWS_PASSWORD_PATH")
WINDOWS_EXECUTOR=os.getenv("WINDOWS_EXECUTOR")
WINDOWS_WINRM_AUTHTYPE=os.getenv("WINDOWS_WINRM_AUTHTYPE")
WINDOWS_WINRM_PROTOCOL=os.getenv("WINDOWS_WINRM_PROTOCOL")
WINDOWS_WINRM_CMD=os.getenv("WINDOWS_WINRM_CMD")

service_instance = SmartConnect(host=os.getenv("VCENTER_HOSTNAME"), user=os.getenv("VCENTER_USERNAME"), pwd=os.getenv("VCENTER_PASSWORD"),disableSslCertValidation=True)
content = service_instance.RetrieveContent()


# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for managed_object_ref in container.view:
            obj.update({managed_object_ref: managed_object_ref.name})
    return obj

#Calling above method
getAllVms=get_all_objs(content, [vim.VirtualMachine])

inventory=[]
#Iterating each vm object and printing its name
for vm in getAllVms:
    inventoryObject = {}

    # Get general data
    inventoryObject["nodename"] = vm.name
    inventoryObject["hostname"] = vm.name
    inventoryObject["description"] = vm.config.annotation
    inventoryObject["osName"] = vm.guest.guestFullName
    inventoryObject["osFamily"] = vm.guest.guestFamily

    # Add OS to tags
    inventoryObject["tags"] = [vm.guest.guestFullName,vm.guest.guestFamily]

    # Add Networks to tags
    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard):
            try:
                dvs = content.dvSwitchManager.QueryDvsByUuid(dev.backing.port.switchUuid)
                pg_obj = dvs.LookupDvPortGroup(dev.backing.port.portgroupKey)
                inventoryObject["tags"].append("Net_%s" % pg_obj.config.name)
            except:
                pass
    
    # Setup Login
    if vm.guest.guestFamily is not None:
        if vm.guest.guestFamily.lower() == "linuxguest":
            inventoryObject["username"] = LINUX_USER
            inventoryObject["ssh-key-storage-path"] = LINUX_KEY_PATH
            inventoryObject["ssh-authentication"] = LINUX_AUTHENTICATION
            inventoryObject["node-executor"] = LINUX_EXECUTOR
            inventoryObject["file-copier"] = LINUX_EXECUTOR

        if vm.guest.guestFamily.lower() == "windowsguest":
            inventoryObject["username"] = WINDOWS_USER  
            inventoryObject["winrm-password-storage-path"] = WINDOWS_PASSWORD_PATH 
            inventoryObject["winrm-authtype"] = WINDOWS_WINRM_AUTHTYPE
            inventoryObject["winrm-auth-type"] = WINDOWS_WINRM_AUTHTYPE
            inventoryObject["winrm-protocol"] = WINDOWS_WINRM_PROTOCOL
            inventoryObject["winrm-cmd"] = WINDOWS_WINRM_CMD
            inventoryObject["node-executor"] = WINDOWS_EXECUTOR
            inventoryObject["file-copier"] = WINDOWS_EXECUTOR

    inventory.append(inventoryObject)



print(dump(inventory, Dumper=Dumper))