import sys

inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels

    def __repr__(self):
        return str(self.__dict__)

class Tunnel:
    def __init__(self, target, length=1):
        self.target = target
        self.length = 1

    def __repr__(self):
        return str(self.__dict__)

valves = []
network = {}
for line in inputs:
    l = line.split()
    valve = Valve(l[1], int(l[4][5:-1]), {t.strip(','): 1 for t in l[9:]})
    valves.append(valve)
    network[valve.name] = valve

print(network)

for valve in network.values():
    for tunnel, length in valve.tunnels.items():
        if network[tunnel].rate == 0 and tunnel != 'AA':
            network[tunnel].tunnels[
        pass
