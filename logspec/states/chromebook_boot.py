# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Copyright (C) 2024 Collabora Limited
# Author: Ricardo Cañuelo <ricardo.canuelo@collabora.com>

import re
from logspec.fsm_classes import State
from logspec.fsm_loader import register_state

MODULE_NAME = 'chromebook_boot'


# State functions and helpers

def parse_bootloader_errors(text):
    data = {}
    return data


def detect_bootloader_start(text):
    """Detects the start of a Chromebook bootloader run in a boot log.

    Parameters:
      text (str): the log or text fragment to parse

    Returns a dict containing the extracted info from the log:
      'bootloader_found': True if the bootloader was detected, False
          otherwise
      'bootloader': name or tag that identifies the bootloader found
      'match_end': position in `text' where the parsing ended
    """
    # Patterns (tags) to search for. The regexp will be formed by or'ing
    # them
    tags = [
        "Starting depthcharge",
    ]
    data = {}
    regex = '|'.join(tags)
    match = re.search(regex, text)
    if match:
        data['match_end'] = match.end()
        data['bootloader_found'] = True
        data['bootloader'] = 'depthcharge'
    else:
        data['bootloader_found'] = False
    return data


def detect_bootloader_end(text):
    """Detects the end of a successful Chromebook bootloader execution
    in a text log and searches for errors during the process.

    Parameters:
      text (str): the log or text fragment to parse

    Returns a dict containing the extracted info from the log:
      'bootloader_ok': True if the bootloader was detected to boot
          successfuly, False otherwise
      'match_end': position in `text' where the parsing ended
    """
    # Patterns (tags) to search for. The regexp will be formed by or'ing
    # them
    tags = [
        "Starting kernel ...",
        "jumping to kernel",
    ]
    data = {}
    regex = '|'.join(tags)
    match = re.search(regex, text)
    if match:
        data['match_end'] = match.end()
        data['bootloader_ok'] = True
        # Search for errors up until the found tag
        data.update(parse_bootloader_errors(text[:match.start()]))
    else:
        data['bootloader_ok'] = False
    return data


# Create and register states

register_state(
    MODULE_NAME,
    State(
        name="Chromebook boot",
        description="Initial state for a Chromebook that was powered on",
        function=detect_bootloader_start),
    'chromebook_boot')

register_state(
    MODULE_NAME,
    State(
        name="Chromebook bootloader started",
        description="Chromebook bootloader found",
        function=detect_bootloader_end),
    'chromebook_bootloader_started')

register_state(
    MODULE_NAME,
    State(
        name="Chromebook boot (second stage)",
        description="Initial state for a Chromebook that was powered on (second stage)",
        function=detect_bootloader_start),
    'chromebook_boot_stage2')

register_state(
    MODULE_NAME,
    State(
        name="Chromebook bootloader (second stage) started",
        description="Chromebook bootloader (second stage) found",
        function=detect_bootloader_end),
    'chromebook_bootloader_stage2_started')