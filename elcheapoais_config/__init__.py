import dbus
import dbus.service
import dbus.mainloop.glib
import gi.repository.GLib
import json
import os.path
import sys

def timeout(to):
    def wrapper(fn):
        gi.repository.GLib.timeout_add(to, fn)
    return wrapper
        
class ConfigObject(dbus.service.Object):
    def __init__(self, conn, storagepath=None, writable=True, object_path='/no/innovationgarage/elcheapoais/config'):
        self.storagepath = storagepath
        self.writable = writable
        if storagepath and os.path.exists(storagepath):
            with open(storagepath) as f:
                self.properties = json.load(f)
        else:
            self.properties = {}
        dbus.service.Object.__init__(self, conn, object_path)
    
    @dbus.service.signal('org.freedesktop.DBus.Properties', signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties, invalidated_properties):
        pass

    @dbus.service.method("org.freedesktop.DBus.Properties",
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        return self.properties[interface_name][property_name]

    @dbus.service.method("org.freedesktop.DBus.Properties",
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        return self.properties[interface_name]
    
    @dbus.service.method("org.freedesktop.DBus.Properties",
                         in_signature='ssv', out_signature='')
    def Set(self, interface_name, property_name, value):
        if interface_name not in self.properties:
            self.properties[interface_name] = {}
        self.properties[interface_name][property_name] = value
        if self.storagepath and self.writable:
             with open(self.storagepath, "w") as f:
                 json.dump(self.properties, f)
        self.PropertiesChanged(interface_name, {property_name: value}, {})
        
def main():
    with open(sys.argv[1]) as f:
        config = json.load(f)
                 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = getattr(dbus, config.get("bus", "SessionBus"))()
    name = dbus.service.BusName(config.get("name", "no.innovationgarage.elcheapoais.config"), bus)

    config_objects = {name: ConfigObject(bus, object_path=name, **args)
                      for name, args in config["configs"].items()}

    loop = gi.repository.GLib.MainLoop()
    print("Running example signal emitter service.")
    loop.run()
