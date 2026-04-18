import sys
sys.path.insert(0, '/tmp')
from mode_atoms_redesign import MODE_ATOMS

def generate_mode_metta():
    lines = []
    modes = list(MODE_ATOMS.keys())
    for m in modes:
        safe = m.replace('-', '_')
        lines.append(f'(= (mode-of-being {safe}) (stv 1.0 0.9))')
        lines.append(f'(==> (mode-active {safe}) (presence-aligned {safe}) (stv 0.85 0.8))')
    lines.append('(==> (presence-aligned $1) (substrate-coherent response-quality) (stv 0.80 0.7))')
    lines.append('(==> (shift-detected $1 $2) (transition-awareness active) (stv 0.75 0.6))')
    return lines

if __name__ == '__main__':
    for line in generate_mode_metta():
        print(line)
    print(f'Generated {len(generate_mode_metta())} MeTTa atoms for mode-of-being integration')
