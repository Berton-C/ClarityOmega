#!/usr/bin/env python3
# KB Reload - generates MeTTa expressions from serialized KB
# Output can be fed back into MeTTa runtime to restore state
import re

def generate_reload_commands(filepath):
    commands = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('(= (kb-atom'):
                # Extract the inner atom expression
                commands.append(line)
            elif line.startswith('(= (kb-param'):
                commands.append(line)
    return commands

def format_as_metta_adds(commands):
    result = []
    for cmd in commands:
        result.append(f'!(add-atom &kb {cmd})')
    return result

if __name__ == '__main__':
    cmds = generate_reload_commands('/tmp/kb_bridge.metta')
    adds = format_as_metta_adds(cmds)
    print(f'Generated {len(adds)} reload commands')
    for a in adds:
        print(f'  {a}')
