#!/usr/bin/env python3
import json

def evaluate_response(draft_response, situation_guidance):
    words = draft_response.lower().split()
    wc = len(words)
    has_question = '?' in draft_response
    has_framework = any(w in draft_response.lower() for w in ['because','pattern','framework','principle','means','implies'])
    has_options = any(w in draft_response.lower() for w in ['option','path','approach','choice','alternatively','could'])
    has_novelty = any(w in draft_response.lower() for w in ['insight','discovery','surprising','unexpected','notice','interesting'])
    agency = 0.5 + (0.2 if has_options else 0) + (0.15 if has_question else 0) + (0.1 if has_framework else 0)
    wonder = 0.3 + (0.25 if has_novelty else 0) + (0.15 if has_question else 0) + (0.1 if wc > 30 else 0)
    thinking = 0.4 + (0.2 if has_framework else 0) + (0.15 if has_novelty else 0) + (0.1 if wc > 20 else 0)
    attention = max(0.2, 1.0 - (wc / 500.0)) if wc < 500 else 0.2
    scores = {'agency': min(1.0, agency), 'wonder': min(1.0, wonder), 'thinking': min(1.0, thinking), 'attention': min(1.0, attention)}
    composite = sum(scores.values()) / 4.0
    flags = [k for k,v in scores.items() if v < 0.4]
    return {'compass_scores': scores, 'composite': round(composite, 3), 'flags': flags, 'pass': len(flags) == 0}

if __name__ == '__main__':
    tests = ['Here are your options: A, B, or C. What matters most to you?',
             'Status update: everything is fine. Menu: 1) help 2) quit',
             'That is a genuinely interesting pattern. It implies something surprising about how memory shapes presence.']
    for t in tests:
        r = evaluate_response(t, 'novel_territory')
        print(f'Text: {t[:60]}...')
        print(f'  Scores: {r["compass_scores"]}')
        print(f'  Composite: {r["composite"]} Pass: {r["pass"]} Flags: {r["flags"]}')
        print()
