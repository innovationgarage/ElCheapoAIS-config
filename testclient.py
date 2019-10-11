import dbus
bus = dbus.SessionBus()
config = bus.get_object('no.innovationgarage.elcheapoais.config', '/no/innovationgarage/elcheapoais/downsampler')
config.Set("foo.bar", "fie", 1234)
config.Set("foo.bar", "hehe", {"X": "nananan"})
print("Current config", config.GetAll("foo.bar"))
