import json, os, sys
sys.path.insert(0, '/tmp')
import chromadb

class BackboneWorkspace:
    def __init__(self, chroma_path='/tmp/chroma_db', collection_name='nrc_vad_full'):
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.client.get_collection(collection_name)
        self.current_vad = [0.5, 0.5, 0.5]
        self.mode_stack = []
        self.shift_history = []
        self.vad_history = []
        self.turn_count = 0
        self.state_file = '/tmp/backbone_state.json'
        self._load_state()

    def _lookup_word(self, word):
        results = self.collection.get(where={'word': word})
        if results['ids']:
            m = results['metadatas'][0]
            return (m['valence'], m['arousal'], m['dominance'])
        return None

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                s = json.load(f)
                self.current_vad = s.get('current_vad', [0.5,0.5,0.5])
                self.mode_stack = s.get('mode_stack', [])
                self.shift_history = s.get('shift_history', [])
                self.vad_history = s.get('vad_history', [])
                self.turn_count = s.get('turn_count', 0)

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({'current_vad': self.current_vad, 'mode_stack': self.mode_stack, 'shift_history': self.shift_history, 'vad_history': self.vad_history, 'turn_count': self.turn_count}, f, indent=2)

    def _get_trajectory(self):
        window = self.vad_history[-5:]
        if len(window) < 2:
            return {'v_dir': 'insufficient', 'a_dir': 'insufficient', 'v_delta': 0.0, 'a_delta': 0.0}
        v_delta = window[-1][0] - window[0][0]
        a_delta = window[-1][1] - window[0][1]
        v_dir = 'rising' if v_delta > 0.1 else ('falling' if v_delta < -0.1 else 'stable')
        a_dir = 'escalating' if a_delta > 0.1 else ('settling' if a_delta < -0.1 else 'steady')
        return {'v_dir': v_dir, 'a_dir': a_dir, 'v_delta': round(v_delta, 3), 'a_delta': round(a_delta, 3)}

    def process_turn(self, text, speaker_id):
        words = text.lower().split()
        hits = []
        vals = []
        for w in words:
            vad = self._lookup_word(w)
            if vad:
                hits.append(w)
                vals.append(vad)
        if vals:
            new_vad = [round(sum(v[i] for v in vals)/len(vals), 3) for i in range(3)]
        else:
            new_vad = self.current_vad[:]
        shift = round(sum(abs(new_vad[i]-self.current_vad[i]) for i in range(3))/3, 3)
        self.current_vad = new_vad
        self.shift_history.append(shift)
        self.vad_history.append(new_vad[:])
        self.turn_count += 1
        trajectory = self._get_trajectory()
        modes = self._route_modes(new_vad, shift, trajectory)
        self.mode_stack = modes
        self.save_state()
        return {'vad': new_vad, 'hits': len(hits), 'words': len(words), 'shift': shift, 'modes': modes, 'turn': self.turn_count, 'hit_words': hits, 'trajectory': trajectory}

    def _route_modes(self, vad, shift, trajectory):
        v, a, d = vad
        modes = []
        if v < 0.35 and a > 0.5:
            modes.append('empathic-attunement')
        elif v < 0.35:
            modes.append('gentle-activation')
        if v > 0.6 and a > 0.5:
            modes.append('momentum-amplification')
        elif v > 0.5:
            modes.append('witnessing-celebration')
        if d > 0.55:
            modes.append('collaborative-exploration')
        if a < 0.35:
            modes.append('gentle-activation')
        if shift > 0.15 and self.turn_count > 1:
            modes.append('recalibration')
        # TRAJECTORY-AWARE ROUTING
        if trajectory['v_dir'] == 'falling' and v > 0.35:
            modes.append('stabilizing-presence')
        if trajectory['v_dir'] == 'rising' and v < 0.5:
            modes.append('momentum-amplification')
        if trajectory['a_dir'] == 'escalating' and a > 0.4:
            modes.append('grounding-presence')
        if not modes:
            modes.append('neutral-presence')
        return list(dict.fromkeys(modes))

    def get_guidance(self):
        trajectory = self._get_trajectory()
        return {'vad': self.current_vad, 'modes': self.mode_stack, 'turn_count': self.turn_count, 'recent_shift': self.shift_history[-1] if self.shift_history else 0.0, 'trajectory': trajectory}
