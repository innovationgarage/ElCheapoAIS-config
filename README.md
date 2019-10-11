# ElCheapoAIS-config

A simple [DBus properties](https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces-properties) storage
container with optional json based file backing.

    elcheapoais-config config.json

config.json:

    {
        "bus": "SessionBus",
        "name": "no.innovationgarage.elcheapoais.config", // Bus name

        "configs": {
            "/no/innovationgarage/elcheapoais/downsampler": { // object path
                "storagepath": "data/downsampler.json",       // load and store properties here
                "writable": true                              // allow Set()
            },
            "/no/innovationgarage/elcheapoais/status": {
            }
        }
    }


Each config specified under "configs" in the json file appears as a separate object path. If "storagepath" is set for the
config, properties will be persisted as a json file with the specified path. The json file will contain an object with one
member per interface name, each being another object with property names and member names and property values as member
values.

