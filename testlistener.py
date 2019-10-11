#!/usr/bin/env python
import sys
import traceback

import dbus
import dbus.mainloop.glib
import gi.repository.GLib

def PropertiesChanged(*arg, **kw):
    dbus_message = kw.pop("dbus_message")
    print("PropertiesChanged(%s, %s)" % (arg, kw))

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()

    #bus.add_signal_receiver(catchall_hello_signals_handler, dbus_interface = "com.example.TestService", signal_name = "HelloSignal")

    bus.add_signal_receiver(PropertiesChanged,
                            dbus_interface = "org.freedesktop.DBus.Properties",
                            signal_name = "PropertiesChanged",
                            message_keyword='dbus_message')

    loop = gi.repository.GLib.MainLoop()
    loop.run()
    
