DEST_HERE = 'here'
DEST_OUT = 'out'
DEST_IN = 'in-'

DESTS = [DEST_HERE, DEST_OUT, DEST_IN]

def check_correct_dest(x):
    return (x in DESTS[:2]) or (x.startswith(DESTS[-1]))