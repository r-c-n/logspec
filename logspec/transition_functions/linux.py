# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Copyright (C) 2024 Collabora Limited
# Author: Ricardo Cañuelo <ricardo.canuelo@collabora.com>

from fsm_loader import register_transition_function

MODULE_NAME = 'linux'


register_transition_function(
    MODULE_NAME,
    lambda x: x['bootloader_ok'],
    'linux_start_detected')

register_transition_function(
    MODULE_NAME,
    lambda x: x['prompt_ok'],
    'linux_prompt_detected')
