from difflib import *
from load_texts import *  

print("Loading data...")
corpus = read_text_files()[0]
print(len(corpus), "minutes")

minute0 = corpus[-1]
minute1 = corpus[-2]

print(' '.join(list(context_diff(minute1.split(), minute0.split(), fromfile="last",tofile="before"))))


def diff_strings(a: str, b: str, *, use_loguru_colors: bool = False) -> str:
    """
    Adapted from "https://gist.github.com/ines/04b47597eb9d011ade5e77a068389521"
    """
    output = []
    matcher = SequenceMatcher(None, a, b)
    green = '\x1b[38;5;16;48;5;2m'
    red = '\x1b[38;5;16;48;5;1m'
    endgreen = '\x1b[0m'
    endred = '\x1b[0m'

    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            output.append(a[a0:a1])
        elif opcode == 'insert':
            output.append(f'{green}{b[b0:b1]}{endgreen}')
        elif opcode == 'delete':
            output.append(f'{red}{a[a0:a1]}{endred}')
        elif opcode == 'replace':
            output.append(f'{green}{b[b0:b1]}{endgreen}')
            output.append(f'{red}{a[a0:a1]}{endred}')
    return ''.join(output)

print(diff_strings(minute1, minute0))