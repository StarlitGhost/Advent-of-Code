from GhostyUtils import aoc


if __name__ == "__main__":
    print('p1:', sum(mod // 3 - 2 for mod in map(int, aoc.by_lines())))

    total_fuel = 0
    for mod in map(int, aoc.by_lines()):
        mod_fuel = mod // 3 - 2
        fuel_fuel = mod_fuel
        while fuel_fuel > 0:
            fuel_fuel //= 3
            fuel_fuel -= 2
            if fuel_fuel > 0:
                mod_fuel += fuel_fuel
        total_fuel += mod_fuel
    print('p2:', total_fuel)
