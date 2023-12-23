with open('input') as f:
    inputs = (line.rstrip('\n') for line in f)

    def build_tree(inputs):
        tree_node = {'size': 0, 'subdirs': {}}

        for line in inputs:
            if line.startswith('$'):
                if line == '$ cd /':
                    pass
                elif line == '$ cd ..':
                    return tree_node
                elif line.startswith('$ cd '):
                    subdir = line.split()[-1]
                    tree_node['subdirs'][subdir] = build_tree(inputs)
                elif line == '$ ls':
                    pass
                else:
                    print(f'unknown instruction {line}')
                    exit()
            else:
                l, r = line.split()
                if l == 'dir':
                    tree_node['subdirs'][r] = {'size': 0, 'subdirs': {}}
                else:
                    tree_node['size'] += int(l)
        return tree_node

    tree = build_tree(inputs)

    def total_size(tree_node):
        size = tree_node['size']
        for _, subdir in tree_node['subdirs'].items():
            size += total_size(subdir)
        tree_node['total_size'] = size
        return size

    total_size(tree)

    def sum_sizes(tree_node):
        size_sum = 0
        if tree_node['total_size'] <= 100000:
            size_sum += tree_node['total_size']
        for _, subdir in tree_node['subdirs'].items():
            size_sum += sum_sizes(subdir)
        return size_sum

    size_sum = sum_sizes(tree)
    print(size_sum)

    total_space = 70000000
    used_space = tree['total_size']
    needed_space = 30000000
    free_space = total_space - used_space
    to_delete = needed_space - free_space

    def smallest_dir(tree_node, to_delete, smallest_found):
        for _, subdir in tree_node['subdirs'].items():
            if smallest_found > subdir['total_size'] > to_delete:
                smallest_found = subdir['total_size']
            smallest_found = smallest_dir(subdir, to_delete, smallest_found)
        return smallest_found

    smallest = smallest_dir(tree, to_delete, tree['total_size'])
    print(free_space, to_delete, smallest)
