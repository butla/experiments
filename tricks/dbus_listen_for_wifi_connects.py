#!/usr/bin/python

import pprint

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


def run_dbus_capture():
    DBusGMainLoop(set_as_default=True)

    system_bus = dbus.SystemBus()

    loop = GLib.MainLoop()
    system_bus.add_signal_receiver(dbus_handler)
    print('trying to show all dbus signals...')
    loop.run()


def dbus_handler(*args, **kwargs):
    pprint.pprint(args)
    pprint.pprint(kwargs)


if __name__ == '__main__':
    run_dbus_capture()
