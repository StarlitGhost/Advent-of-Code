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
        tree_node['size'] = size
        return size

    total_size(tree)

    def sum_sizes(tree_node):
        size_sum = 0
        if tree_node['size'] <= 100000:
            size_sum += tree_node['size']
        for _, subdir in tree_node['subdirs'].items():
            size_sum += sum_sizes(subdir)
        return size_sum

    size_sum = sum_sizes(tree)
    print(size_sum)
