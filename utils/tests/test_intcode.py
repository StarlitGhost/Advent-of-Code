from GhostyUtils.intcode.cpu import IntCode


def test_cpu():
    programs = [
        {
            'mem_in': "1,9,10,3,2,3,11,0,99,30,40,50",
            'input': [],
            'output': [],
            'mem_out': "3500,9,10,70,2,3,11,0,99,30,40,50",
        },
        {
            'mem_in': "1,0,0,0,99",
            'input': [],
            'output': [],
            'mem_out': "2,0,0,0,99",
        },
        {
            'mem_in': "2,3,0,3,99",
            'input': [],
            'output': [],
            'mem_out': "2,3,0,6,99",
        },
        {
            'mem_in': "2,4,4,5,99,0",
            'input': [],
            'output': [],
            'mem_out': "2,4,4,5,99,9801",
        },
        {
            'mem_in': "1,1,1,4,99,5,6,0,99",
            'input': [],
            'output': [],
            'mem_out': "30,1,1,4,2,5,6,0,99",
        },
        {
            'mem_in': "1002,4,3,4,33",
            'input': [],
            'output': [],
            'mem_out': "1002,4,3,4,99",
        },
        {
            'mem_in': "1101,100,-1,4,0",
            'input': [],
            'output': [],
            'mem_out': "1101,100,-1,4,99",
        },
        {
            # position mode, input == 8
            'mem_in': "3,9,8,9,10,9,4,9,99,-1,8",
            'input': [8],
            'output': [1],
            'mem_out': "3,9,8,9,10,9,4,9,99,1,8",
        },
        {
            # position mode, input < 8
            'mem_in': "3,9,7,9,10,9,4,9,99,-1,8",
            'input': [7],
            'output': [1],
            'mem_out': "3,9,7,9,10,9,4,9,99,1,8",
        },
        {
            # immediate mode, input == 8
            'mem_in': "3,3,1108,-1,8,3,4,3,99",
            'input': [8],
            'output': [1],
            'mem_out': "3,3,1108,1,8,3,4,3,99",
        },
        {
            # immediate mode, input < 8
            'mem_in': "3,3,1107,-1,8,3,4,3,99",
            'input': [7],
            'output': [1],
            'mem_out': "3,3,1107,1,8,3,4,3,99",
        },
    ]

    for prog in programs:
        output = []
        cpu = IntCode(prog['mem_in'],
                      input=prog['input'].pop,
                      output=output.append)
        cpu.process()
        assert output == prog['output']
        assert cpu.str_memory() == prog['mem_out']
