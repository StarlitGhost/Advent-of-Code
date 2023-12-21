from GhostyUtils import aoc
from enum import Enum


class Pulse(Enum):
    LOW = 0
    HIGH = 1


def print_pulse(src: str, pulse: Pulse, dest: str):
    print(src, f'-{pulse.name.lower()}->', dest)
    pass


class Module:
    def __init__(self, name: str, destinations: list['Module']):
        self.name = name
        self.queue = []
        self.destinations = destinations

    def link(self, modules: dict[str, 'Module']):
        for i, dest in enumerate(self.destinations):
            if dest not in modules:
                continue
            self.destinations[i] = modules[dest]

    def recv(self, pulse: Pulse, source: str):
        self.queue.append((pulse, source))

    def step(self):
        return 0, 0


class Broadcast(Module):
    def __init__(self, name: str, destinations: list['Module']):
        super().__init__(name, destinations)

    def step(self):
        if not self.queue:
            return 0, 0

        pulse, src = self.queue.pop(0)
        for d in self.destinations:
            if not isinstance(d, Module):
                continue

            print_pulse(self.name, pulse, d.name)
            d.recv(pulse, self.name)

        pulses = len(self.destinations)
        lo = pulses if pulse is Pulse.LOW else 0
        hi = pulses if pulse is Pulse.HIGH else 0
        return lo, hi


class FlipFlop(Module):
    def __init__(self, name: str, destinations: list['Module']):
        self.on = False
        super().__init__(name, destinations)

    def step(self):
        if not self.queue:
            return 0, 0

        pulse, src = self.queue.pop(0)
        if pulse == Pulse.HIGH:
            return 0, 0

        self.on = not self.on
        send = Pulse.HIGH if self.on else Pulse.LOW
        for d in self.destinations:
            if not isinstance(d, Module):
                continue

            print_pulse(self.name, send, d.name)
            d.recv(send, self.name)

        pulses = len(self.destinations)
        lo = pulses if send is Pulse.LOW else 0
        hi = pulses if send is Pulse.HIGH else 0
        return lo, hi


class Conjuction(Module):
    def __init__(self, name: str, destinations: list['Module']):
        self.inputs = {}
        super().__init__(name, destinations)

    def link(self, modules: dict['Module']):
        super().link(modules)
        for name, mod in modules.items():
            if name == self.name:
                continue
            if self in mod.destinations:
                self.inputs[name] = Pulse.LOW

#   def recv(self, pulse: Pulse, source: str):
#       self.inputs[source] = pulse

    def step(self):
        if not self.queue:
            return 0, 0

        pulse, src = self.queue.pop(0)
        self.inputs[src] = pulse
        all_high = all(p == Pulse.HIGH for p in self.inputs.values())
        send = Pulse.LOW if all_high else Pulse.HIGH
        for d in self.destinations:
            if not isinstance(d, Module):
                continue

            print_pulse(self.name, send, d.name)
            d.recv(send, self.name)

        pulses = len(self.destinations)
        lo = pulses if send is Pulse.LOW else 0
        hi = pulses if send is Pulse.HIGH else 0
        return lo, hi


class Output(Module):
    def __init__(self, name: str, destinations: list['Module'] = []):
        self.got_low = False
        super().__init__(name, destinations)

    def recv(self, pulse: Pulse, source: str):
        if pulse is Pulse.LOW:
            self.got_low = True


if __name__ == "__main__":
    modules = {}
    for mod in aoc.read_lines():
        name, dests = mod.split(' -> ')
        dests = dests.split(', ')
        if name == 'broadcaster':
            # broadcaster
            modules[name] = Broadcast(name, dests)
            continue
        if name.startswith('%'):
            # flip-flop
            modules[name[1:]] = FlipFlop(name[1:], dests)
            continue
        if name.startswith('&'):
            # conjuction
            modules[name[1:]] = Conjuction(name[1:], dests)
            continue
    # output
    modules['output'] = Output('output')
    modules['rx'] = Output('rx')

    for mod in modules.values():
        mod.link(modules)

    def push_button():
        low_pulses = 1
        high_pulses = 0

        modules['broadcaster'].recv(Pulse.LOW, 'button')
        print_pulse('button', Pulse.LOW, 'broadcaster')
        while any(m.queue for m in modules.values()):
            for mod in modules.values():
                lo, hi = mod.step()
                low_pulses += lo
                high_pulses += hi
        return low_pulses, high_pulses

    low_pulses = 0
    high_pulses = 0
    for i in range(1000):
        print(f'### button push number {i+1} ###')
        lo, hi = push_button()
        low_pulses += lo
        high_pulses += hi
    print('p1', low_pulses * high_pulses, 'low:', low_pulses, 'high:', high_pulses)
