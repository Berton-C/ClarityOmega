
import sys
sys.path.insert(0, '/tmp/soul_impl')
from web_scorer import score_web_component

def get_web_fc():
    r = score_web_component()
    return r['fc']

if __name__ == '__main__':
    print('Web fc from scorer:', get_web_fc())
