import sys
sys.path.insert(0, '/tmp')
from conversation_handler_v2 import handle_turn

test_cases = [
    ('I feel lost and alone', 'gentle-activation-reframe'),
    ('This is amazing I am so excited', 'amplify-momentum'),
    ('I am just checking in nothing special', 'small-prompts-warmth'),
    ('That makes me furious', 'prioritize-validation'),
    ('Lets brainstorm together on this', 'collaborative-ideation'),
    ('I feel overwhelmed and helpless', 'gentle-activation-reframe'),
    ('Everything is going perfectly', 'amplify-momentum'),
]

passed = 0
failed = 0
for text, expected in test_cases:
    r = handle_turn(text, 'user')
    actual = r['action']
    status = 'PASS' if actual == expected else 'MISS'
    if status == 'PASS':
        passed += 1
    else:
        failed += 1
    print('%s: %s -> %s (expected %s)' % (status, text, actual, expected))

print('\nResults: %d passed, %d missed out of %d' % (passed, failed, len(test_cases)))
