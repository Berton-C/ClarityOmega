#!/usr/bin/env python3
import json, os, chromadb

STOPWORDS = {'i','me','my','we','our','you','your','he','she','it','they','a','an','the','is','am','are','was','were','be','been','being','have','has','had','do','does','did','will','would','shall','should','can','could','may','might','must','to','of','in','for','on','with','at','by','from','as','into','through','during','before','after','above','below','between','out','off','over','under','again','further','then','once','here','there','when','where','why','how','all','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','just','but','and','if','or','because','until','while','about','up','down','that','this','these','those'}

class BackboneWorkspace:
    def __init__(self, chroma_path='/tmp/chroma_db', collection_name='nrc_vad_full'):
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.client.get_collection(collection_name)
        self.current_vad = [0.0, 0.0, 0.0]
        self.mode_stack = []
        self.shift_history = []
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
                self.current_vad = s.get('current_vad', [0.0,0.0,0.0])
                self.mode_stack = s.get('mode_stack', [])
                self.shift_history = s.get('shift_history', [])
                self.turn_count = s.get('turn_count', 0)

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({'current_vad': self.current_vad, 'mode_stack': self.mode_stack, 'shift_history': self.shift_history, 'turn_count': self.turn_count}, f, indent=2)

    def process_turn(self, text, speaker_id):
        words = text.lower().split()
        content_words = [w for w in words if w not in STOPWORDS]
        hits, vals = [], []
        for w in content_words:
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
        self.turn_count += 1
        modes = self._route_modes(new_vad, shift)
        self.mode_stack = modes
        self.save_state()
        return {'vad': new_vad, 'hits': len(hits), 'words': len(words), 'shift': shift, 'modes': modes, 'turn': self.turn_count, 'hit_words': hits}

    def _route_modes(self, vad, shift):
        v, a, d = vad
        modes = []
        if v < -0.3 and a > 0.0: modes.append('empathic-attunement')
        elif v < -0.3: modes.append('gentle-activation')
        if v > 0.3 and a > 0.0: modes.append('momentum-amplification')
        elif v > 0.1: modes.append('witnessing-celebration')
        if d > 0.1: modes.append('collaborative-exploration')
        if a < -0.3: modes.append('gentle-activation')
        if shift > 0.15 and self.turn_count > 1: modes.append('recalibration')
        if not modes: modes.append('neutral-presence')
        return list(dict.fromkeys(modes))

    def get_guidance(self):
        return {'vad': self.current_vad, 'modes': self.mode_stack, 'turn_count': self.turn_count, 'recent_shift': self.shift_history[-1] if self.shift_history else 0.0}
