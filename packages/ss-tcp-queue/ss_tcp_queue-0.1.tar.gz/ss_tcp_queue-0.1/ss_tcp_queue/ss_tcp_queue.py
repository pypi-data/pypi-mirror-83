import distutils.spawn
import os
import re
import socket
from collections import defaultdict

import psutil
from six import PY3, iteritems, itervalues

from datadog_checks.base import AgentCheck, ConfigurationError, is_affirmative
from datadog_checks.base.utils.common import pattern_filter
from datadog_checks.base.utils.platform import Platform
from datadog_checks.base.utils.subprocess_output import SubprocessOutputEmptyError, get_subprocess_output

try:
    import datadog_agent
except ImportError:
    from datadog_checks.base.stubs import datadog_agent

__version__ = "1.0.0"

class ss_tcp_queue(AgentCheck):

    SOURCE_TYPE_NAME = 'system'

    PSUTIL_TYPE_MAPPING = {socket.SOCK_STREAM: 'tcp', socket.SOCK_DGRAM: 'udp'}

    PSUTIL_FAMILY_MAPPING = {socket.AF_INET: '4', socket.AF_INET6: '6'}

    def check(self, instance):
        if instance is None:
            instance = {}

        cmd = "ss --numeric --listening --tcp"
        output, _, _ = get_subprocess_output(["sh", "-c", cmd], self.log, raise_on_empty_output=True)

        # Run "ss --numeric --listening --tcp" command on host.
        # Expected output:
        # State             Recv-Q             Send-Q                          Local Address:Port                          Peer Address:Port
        # LISTEN            0                  128                                 127.0.0.1:6062                               0.0.0.0:*
        # LISTEN            0                  128                                   0.0.0.0:111                                0.0.0.0:*
        # LISTEN            0                  128                                   0.0.0.0:22                                 0.0.0.0:*
        # LISTEN            0                  100                                 127.0.0.1:25                                 0.0.0.0:*
        # LISTEN            0                  128                                 127.0.0.1:8126                               0.0.0.0:*
        # LISTEN            0                  128                                 127.0.0.1:5000                               0.0.0.0:*
        # LISTEN            0                  128                                 127.0.0.1:5001                               0.0.0.0:*
        # LISTEN            0                  80                                          *:3306                                     *:*
        # LISTEN            0                  128                                      [::]:111                                   [::]:*
        # LISTEN            0                  128                                      [::]:22                                    [::]:*


        lines = output.splitlines()

        # Parse the output into Datadog metrics
        for l in lines[1:]:
            cols = l.split()

            ip, port=cols[3].rsplit(':', 1)
            #print(cols[1], cols[2], cols[3], port)
            self.gauge("ss.listening.recvq", cols[1], tags=["port:"+str(port), "type:tcp"])
            self.gauge("ss.listening.sendq", cols[2], tags=["port:"+str(port), "type:tcp"])
