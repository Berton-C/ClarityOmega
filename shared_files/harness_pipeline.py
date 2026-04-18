#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from backbone_workspace import BackboneWorkspace

class HarnessPipeline:
    def __init__(self):
        self.workspace = BackboneWorkspace()

    def ingest_turn(self, text, speaker_id='unknown'):
        result = self.workspace.process_turn(text, speaker_id)
        return result

    def get_guidance(self):
        return self.workspace.get_guidance()

    def format_for_response(self, guidance):
        modes = guidance.get('modes', [])
        v, a, d = guidance.get('vad', [0.5, 0.5, 0.5])
        shift = guidance.get('recent_shift', 0.0)
        lines = []
        lines.append('VAD: v=%.2f a=%.2f d=%.2f shift=%.3f' % (v, a, d, shift))
        lines.append('Modes: %s' % ', '.join(modes) if modes else 'Modes: none')
        return ' | '.join(lines)

if __name__ == '__main__':
    h = HarnessPipeline()
    r = h.ingest_turn('I am really excited about the progress we are making together', 'test-user')
    print('Ingest result:', json.dumps(r))
    g = h.get_guidance()
    print('Guidance:', json.dumps(g))
    print('Formatted:', h.format_for_response(g))
