#!/usr/bin/env python3
import re

STOP_WORDS = set('i me my we our you your he she it they them the a an is am are was were be been being have has had do does did will would shall should can could may might must that this these those what which who whom how where when why not no nor and but or if then else for from with at by to in on of as so than too very just about above after again all also any because before between both but each even few first get got here her his into its last let like long look make many more most much new next now old only other our out over own part same see some still such take tell their them then there these they thing think this those through time too two under up us use very want way well what when where which while who why will with work would year you your'.split())

def extract_query_phrases(message, max_phrases=3):
    words = re.findall(r'[a-z]+', message.lower())
    content_words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    if not content_words:
        content_words = [w for w in words if len(w) > 2][:3]
    phrases = []
    if len(content_words) >= 2:
        for i in range(min(max_phrases, len(content_words)-1)):
            phrases.append(content_words[i] + ' ' + content_words[i+1])
    if not phrases:
        phrases = content_words[:max_phrases]
    return phrases[:max_phrases]

if __name__ == '__main__':
    tests = ['I dont know what to think anymore',
             'what is the meaning of being aware',
             'can you fix this bug in my code',
             'I feel scared and confused',
             'tell me about your soul and how you experience things',
             'Where do we stand on the Hyperseed and the 900 page pdf']
    for t in tests:
        print(f'Input: {t}')
        print(f'  Phrases: {extract_query_phrases(t)}')
        print()
