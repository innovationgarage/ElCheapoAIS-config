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

def dbusify(obj):
    if isinstance(obj, (tuple, list)):
        return dbus.Array([dbusify(value)
                           for value in obj],
                          variant_level=1)
    elif isinstance(obj, dict):
        return dbus.Dictionary({name: dbusify(value)
                                for name, value in obj.items()},
                               variant_level=1)
    elif isinstance(obj, int):
        return dbus.Int64(obj, variant_level=1)
    elif isinstance(obj, float):
        return dbus.Double(obj, variant_level=1)
    elif isinstance(obj, str):
        return dbus.String(obj, variant_level=1)
    elif isinstance(obj, bytes):
        return dbus.ByteArray(obj, variant_level=1)
    else:
        return obj

class ConfigObject(dbus.service.Object):
    def __init__(self, conn, storagepath=None, persistable=True, writable=True, object_path='/no/innovationgarage/elcheapoais/config'):
        self.object_path = object_path
        self.storagepath = storagepath
        self.persistable = persistable
        self.writable = writable
        if storagepath and os.path.exists(storagepath):
            with open(storagepath) as f:
                self.properties = dbusify(json.load(f, object_hook=dbusify))
        else:
            self.properties = {}
        dbus.service.Object.__init__(self, conn, object_path)
        for interface_name, properties in self.properties.items():
            self.PropertiesChanged(interface_name, properties, [])
    
    @dbus.service.signal('org.freedesktop.DBus.Properties', signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties, invalidated_properties):
        print("%s:\n  %s:\n    %s" % (self.object_path, interface_name, "\n    ".join(
            ["%s=%s" % (name, json.dumps(value)) for name, value in changed_properties.items()]
            + ["%s.del" % name for name in invalidated_properties])))

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
        if not self.writable:
            raise Exception("Read only attribute: %s.%s" % (interface_name, property_name))
        if interface_name not in self.properties:
            self.properties[interface_name] = {}
        self.properties[interface_name][property_name] = value
        if self.storagepath and self.persistable:
             with open(self.storagepath, "w") as f:
                 json.dump(self.properties, f)
        self.PropertiesChanged(interface_name, {property_name: value}, {})
        
def main():
    with open(sys.argv[1]) as f:
        config = json.load(f)
                 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = getattr(dbus, os.environ.get("ELCHEAPOAIS_DBUS", "SystemBus"))()
    name = dbus.service.BusName(config.get("name", "no.innovationgarage.elcheapoais.config"), bus)

    config_objects = {name: ConfigObject(bus, object_path=name, **args)
                      for name, args in config["configs"].items()}

    loop = gi.repository.GLib.MainLoop()
    print("Config server running...")
    loop.run()
