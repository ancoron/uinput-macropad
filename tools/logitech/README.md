# Logitech Tools

This directory contains tools that are useful in combination with this project.

## Keyboards

### Logitech G510

This keyboard presents multiple input devices:

1. Logitech G510 Gaming Keyboard (standard keyboard device)
2. Logitech G510 Gaming Keyboard Consumer Control (media control keys)
3. Logitech Gaming Keyboard Gaming Keys (M, G, headphone and LCD keys)

By default, the G1-G18 keys are mapped to other standard keys on device
"Logitech G510 Gaming Keyboard":

| Keys | Mapping |
| G1 - G12 | F1 - F12 |
| G13 - G18 | 1 - 6 (numbers) |

Since there are 2 input devices handling the G keys, the OS also receives
2 events.

Commonly, we choose the device "Logitech Gaming Keyboard Gaming Keys" for being
handled by this project, because only that produces events for M1-M3, MR and
the LCD keys in addition to the G keys.

As a result, even if we grab this device, the events from the standard keyboard
device "Logitech G510 Gaming Keyboard" will still reach the OS and are being
handled, resulting into opening the help of the currently focused application
if you press G1 in addition to the action that you've configured for
uinput-macropad.

But Logitech allows to disable those keys using a control command.

To do this, copy the file `logitech-g510-disable-g-keys.py` of this directory
to you system (e.g. in `/usr/local/bin/logitech-g510-disable-g-keys.py`),
ensure it is executable and ensure you have the Python hidapi installed
globally (from here: https://github.com/trezor/cython-hidapi/).

Then, create a new udev rule to have this script being executed whenever the
keyboard is being added to the system (e.g. into
`/etc/udev/rules.d/logitech-g510.rules`):

```
ACTION=="add", KERNEL=="hidraw*", SUBSYSTEM=="hidraw", \
    ATTRS{manufacturer}=="Logitech", ATTRS{product}=="G510 Gaming Keyboard", \
    ENV{MINOR}=="1", \
    RUN+="/usr/local/bin/logitech-g510-disable-g-keys.py /dev/%k"
```

After reboot or sleep/resume (reload if necessary using
`sudo udevadm control --reload`), the G keys now only produce events for the
input device "Logitech Gaming Keyboard Gaming Keys".
