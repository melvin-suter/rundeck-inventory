from pyVmomi import vmodl, vim
from pyVim.connect import SmartConnect, Disconnect
from yaml import dump, Dumper
import os

defaultUsername="rundeck"

service_instance = SmartConnect(host=os.getenv('VCENTER_HOSTNAME'), user=os.getenv('VCENTER_USERNAME'), pwd=os.getenv('VCENTER_PASSWORD'),disableSslCertValidation=True)
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
    inventoryObject["nodename"] = vm.name
    inventoryObject["hostname"] = vm.name
    inventoryObject["username"] = defaultUsername
    inventoryObject["description"] = vm.config.annotation
    inventoryObject["osName"] = vm.guest.guestFullName
    inventoryObject["osFamily"] = vm.guest.guestFamily
    inventoryObject["tags"] = [] # [vm.guest.guestFullName,vm.guest.guestFamily]

    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard):
            try:
                dvs = content.dvSwitchManager.QueryDvsByUuid(dev.backing.port.switchUuid)
                pg_obj = dvs.LookupDvPortGroup(dev.backing.port.portgroupKey)
                inventoryObject["tags"].append("Net_%s" % pg_obj.config.name)
            except:
                pass
    inventory.append(inventoryObject)



print(dump(inventory, Dumper=Dumper))