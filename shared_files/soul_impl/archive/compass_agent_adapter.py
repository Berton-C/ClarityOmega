import json

def make_compass_metta_fn(metta_skill):
    """Wrap the agent loop metta skill into the callback compass_integration expects.
    
    metta_skill: callable that takes a MeTTa s-expression string
                 and returns the parsed result list.
    Returns: function compatible with compass_score(text, metta_fn)
    """
    def metta_fn(expr):
        try:
            result = metta_skill(expr)
            if result is None:
                return None
            # The metta skill returns nested structure:
            # [[(-->, score-X, compass-X), (stv, f, c)], ...]
            # compass_integration expects this exact format
            parsed = []
            for item in result:
                if hasattr(item, '__len__') and len(item) >= 2:
                    term = list(item[0]) if hasattr(item[0], '__iter__') else item[0]
                    stv = list(item[1]) if hasattr(item[1], '__iter__') else item[1]
                    parsed.append([term, stv])
            return parsed if parsed else result
        except Exception as e:
            return None
    return metta_fn


def compass_evaluate(text, metta_skill):
    """Single entry point for agent loop.
    
    text: response text to evaluate
    metta_skill: the raw metta skill callable from agent loop
    Returns: dict with four compass dimension scores
    """
    from compass_integration import compass_score
    metta_fn = make_compass_metta_fn(metta_skill)
    return compass_score(text, metta_fn)


if __name__ == '__main__':
    # Simulate what the agent loop would do
    def fake_skill(expr):
        print('SKILL CALLED:', expr)
        return [(['-->', 'score-agency', 'compass-agency'], ['stv', 0.775, 0.895])]
    
    scores = compass_evaluate('You might consider alternatives', fake_skill)
    print('RESULT:', json.dumps(scores, indent=2))
