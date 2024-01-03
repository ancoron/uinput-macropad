#!/usr/bin/env python3
# -*- coding: utf-8 *-*
#
# This script disables the G-keys default mapping on the standard keyboard
# device (reported as "Logitech G510 Gaming Keyboard").
#
# By default, the G1-G12 keys are mapped to F1-F12 and G13-G18 to 1-6 and this
# default mapping interferes with any custom behavior attached to the G-keys
# using the separate "Logitech Gaming Keyboard Gaming Keys" device as events
# come in at two devices but only one device is handled through macropad.
#
import sys
import time
import hid

VENDOR_ID = 0x046d
SUPPORTED_PRODUCT_IDS = [
    0xc22d,  # G510
    0xc22e,  # G510 with headphones and/or mic plugged in
]

# found here: https://github.com/zocker-160/keyboard-center/blob/17ac41a91fc8541d127a6d779ad25dc20dedd71c/src/devices/keyboard.py#L216-L220
DISABLE_GKEYS_MESSAGES = [
    bytes([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    bytes([7, 3, 0]),
    bytes([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
]


def find_keyboard():
    for h in hid.enumerate():
        if h["vendor_id"] != VENDOR_ID:
            continue

        if h["product_id"] not in SUPPORTED_PRODUCT_IDS:
            continue

        if h["interface_number"] != 1:
            continue

        print("Using device at: %(path)s" % {"path": h["path"].decode("utf8")})
        return h["path"]
    return None


def disable_keys(dev_path: bytes):
    hid_dev = hid.device()
    try:
        hid_dev.open_path(dev_path)
        print(
            "Device: %(vendor)s %(product)s" % {
                "vendor": hid_dev.get_manufacturer_string(),
                "product": hid_dev.get_product_string(),
            },
        )

        for msg in DISABLE_GKEYS_MESSAGES:
            hid_dev.send_feature_report(msg)
            time.sleep(0.1)

        print("G-Keys disabled")
    finally:
        hid_dev.close()

if __name__ == "__main__":
    dev_path = None
    if len(sys.argv) < 2:
        dev_path = find_keyboard()
    else:
        dev_path = sys.argv[1].encode("utf8")

    if dev_path is None:
        raise Error("No supported device found")

    disable_keys(dev_path)
