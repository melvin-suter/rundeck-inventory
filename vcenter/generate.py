from pyVmomi import vmodl, vim
from pyVim.connect import SmartConnect, Disconnect
from yaml import dump, load, Dumper, Loader
import os

LINUX_USER=os.getenv("LINUX_USER")
LINUX_COPIER=os.getenv("LINUX_COPIER")
LINUX_EXECUTOR=os.getenv("LINUX_EXECUTOR")
LINUX_SETTINGS=os.getenv("LINUX_SETTINGS")

WINDOWS_USER=os.getenv("WINDOWS_USER")
WINDOWS_COPIER=os.getenv("WINDOWS_COPIER")
WINDOWS_EXECUTOR=os.getenv("WINDOWS_EXECUTOR")
WINDOWS_SETTINGS=os.getenv("WINDOWS_SETTINGS")

OTHER_USER=os.getenv("OTHER_USER")
OTHER_COPIER=os.getenv("OTHER_COPIER")
OTHER_EXECUTOR=os.getenv("OTHER_EXECUTOR")
OTHER_SETTINGS=os.getenv("OTHER_SETTINGS")

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
    hit=False
    if vm.guest.guestFamily is not None:
        if vm.guest.guestFamily.lower() == "linuxguest":
            inventoryObject["username"] = LINUX_USER
            inventoryObject["node-executor"] = LINUX_EXECUTOR
            inventoryObject["file-copier"] = LINUX_COPIER
            inventoryObject.update(load(LINUX_SETTINGS, loader=Loader))
            hit=True

        if vm.guest.guestFamily.lower() == "windowsguest":
            inventoryObject["username"] = WINDOWS_USER  
            inventoryObject["node-executor"] = WINDOWS_EXECUTOR
            inventoryObject["file-copier"] = WINDOWS_COPIER
            inventoryObject.update(load(WINDOWS_SETTINGS, loader=Loader))
            hit=True

    if(not hit):
        inventoryObject["username"] = OTHER_USER  
        inventoryObject["node-executor"] = OTHER_EXECUTOR
        inventoryObject["file-copier"] = OTHER_COPIER
        inventoryObject.update(load(OTHER_SETTINGS, loader=Loader))

    inventory.append(inventoryObject)



print(dump(inventory, Dumper=Dumper))