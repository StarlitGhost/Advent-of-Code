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
        {
            # quine
            'mem_in': "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
            'input': [],
            'output': [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],  # noqa: E231
            'mem_out': "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
        },
        {
            # large mul
            'mem_in': "1102,34915192,34915192,7,4,7,99,0",
            'input': [],
            'output': [1219070632396864],
            'mem_out': "1102,34915192,34915192,7,4,7,99,1219070632396864",
        },
        {
            # large output
            'mem_in': "104,1125899906842624,99",
            'input': [],
            'output': [1125899906842624],
            'mem_out': "104,1125899906842624,99",
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
