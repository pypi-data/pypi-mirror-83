# -*- encoding: utf-8 -*-
# zenfilter v0.6.3
# Filter stdin to avoid excessive output
# Copyright © 2016, Shlomi Fish.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Filter stdin to avoid excessive output

:Copyright: © 2016, Shlomi Fish.
:License: BSD (see /LICENSE).
"""

__title__ = 'zenfilter'
__version__ = '0.6.3'
__author__ = 'Shlomi Fish'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ()

# import gettext
# G = gettext.translation('zenfilter', '/usr/share/locale', fallback='C')
# _ = G.gettext
#!/usr/bin/env python3
# * Write "zenfilter" (working title) for:
# - Displaying a "COUNT\t\d+" message every --count-step=\d+ lines.
# - Displaying the last --last=\d+ lines as "LAST\t.*"
# - Displaying lines matching --filter=.* (regex) as "FOUND\t.*"
# "make | python zenfilter.py [args]"

import sys
import argparse
import re


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count-step", type=int)
    parser.add_argument("--last", type=int)
    parser.add_argument("--filter")
    parser.add_argument("--suppress-last-on")
    return parser.parse_args()


def zenfilter():
    args = getArgs()
    lastlines = []
    last = args.last
    count_step = args.count_step
    suppress = args.suppress_last_on
    filt = None
    if args.filter:
        filt = re.compile(args.filter)
    for index, line in enumerate(sys.stdin):
        if last:
            # Append a line to the last lines queue
            lastlines.append(line)
            if len(lastlines) > last:
                # Overflow reached. Remove the first line in the queue.
                lastlines.pop(0)

        if count_step and index % count_step == 0:
            # Line counter
            print("COUNT\t{}".format(index))

        if filt and re.search(filt, line):
            # Regex match. Print the line with the "FOUND" prefix.
            print("FOUND\t{}".format(line), end="")

    # Now we print the last lines queue
    if ((not suppress) or (not re.search(suppress, ''.join(lastlines)))):
        for line in lastlines:
            print("LAST\t{}".format(line), end="")


if __name__ == "__main__":
    zenfilter()
