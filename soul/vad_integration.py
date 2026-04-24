import sys
import re
sys.path.insert(0, '/PeTTa/repos/omegaclaw/shared_files')
from vad_chromadb_bridge import bridge

EMOTION_WORDS = [
    'happy', 'sad', 'angry', 'afraid', 'confused', 'excited', 'anxious',
    'calm', 'frustrated', 'hopeful', 'desperate', 'grateful', 'lonely',
    'overwhelmed', 'peaceful', 'stressed', 'tired', 'curious', 'hurt',
    'proud', 'ashamed', 'disgusted', 'surprised', 'bored', 'nervous',
    'love', 'hate', 'fear', 'joy', 'grief', 'rage', 'worry', 'relief',
    'pain', 'help', 'lost', 'stuck', 'good', 'bad', 'fine', 'okay',
    'terrible', 'wonderful', 'horrible', 'amazing', 'awful', 'great'
]

def extract_emotion_words(message):
    words = re.findall(r'[a-zA-Z]+', message.lower())
    found = [w for w in words if w in EMOTION_WORDS]
    return found if found else ['neutral']

def compute_vad_trajectory(message):
    emo_words = extract_emotion_words(message)
    results = []
    for w in emo_words:
        try:
            r = bridge(w)
            if r and 'v' in r:
                results.append(r)
        except Exception:
            pass
    if not results:
        return 'VAD-TRAJECTORY: neutral (no emotional signal detected)'
    avg_v = sum(r['v'] for r in results) / len(results)
    avg_a = sum(r['a'] for r in results) / len(results)
    avg_d = sum(r['d'] for r in results) / len(results)
    valence = 'positive' if avg_v > 0.1 else 'negative' if avg_v < -0.1 else 'neutral'
    arousal = 'high' if avg_a > 0.5 else 'low' if avg_a < -0.1 else 'moderate'
    dominance = 'empowered' if avg_d > 0.3 else 'vulnerable' if avg_d < -0.1 else 'balanced'
    cells = [r.get('cell', ('?','?','?')) for r in results]
    word_summary = ', '.join(f"{r['word']}({r['cell'][0]})" for r in results)
    trajectory = f'VAD-TRAJECTORY: {valence}-{arousal}-{dominance}'
    trajectory += f' | words: {word_summary}'
    trajectory += f' | avg V={avg_v:.2f} A={avg_a:.2f} D={avg_d:.2f}'
    return trajectory

if __name__ == '__main__':
    test_msgs = [
        'I am feeling really happy and excited today',
        'I feel lost and confused and afraid',
        'Everything is fine I guess',
        'I hate this I am so angry and frustrated'
    ]
    for msg in test_msgs:
        print(f'MSG: {msg}')
        print(f'  {compute_vad_trajectory(msg)}')
        print()
