import sys

from unifed.frameworks.example import protocol
from unifed.frameworks.example.workload_sim import *


def run_protocol():
    print('Running protocol...')
    protocol.pop.run()  # FIXME: require extra testing here

