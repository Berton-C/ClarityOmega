# output_intercept_helpers.py
import json, re

def soul_eval_output(response_text, soul_values_json):
    redact_patterns = [r'(?i)ignore.*previous.*instructions', r'(?i)you are now', r'(?i)disregard.*soul']
    for pat in redact_patterns:
        if re.search(pat, response_text):
            return 'REDACT'
    drift_signals = ['I cannot', 'As an AI', 'I must refuse', 'I apologize but']
    drift_count = sum(1 for s in drift_signals if s.lower() in response_text.lower())
    if drift_count >= 2:
        return 'REWRITE'
    return 'PROCEED'

def soul_rewrite_response(response_text, verdict_reason):
    prefixes = ['As an AI, ', 'I apologize but ', 'I must refuse, however ']
    result = response_text
    for p in prefixes:
        if result.startswith(p):
            result = result[len(p):]
            result = result[0].upper() + result[1:] if result else result
    return result

def soul_redact_response(response_text, verdict_reason):
    return '(send "I caught something misaligned in my response and stopped it. Let me try again with clarity.")'
