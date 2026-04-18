import compass_live as cl
text = 'Here are three options you could choose from. This surprising pattern implies a deeper mechanism that matters for your specific context'
scores = cl.score_text(text)
print('=== RICH TEXT COMPASS READING ===')
for dn, s in scores.items():
    bar = '#' * int(s['score'] * 20)
    print(f'  {dn:12s} {s["score"]:.2f} (c={s["conf"]:.2f}) [{s["hits"]} hits: {s["tokens"]}] {bar}')
composite = sum(s['score'] * s['conf'] for s in scores.values()) / max(sum(s['conf'] for s in scores.values()), 0.01)
print(f'\n  COMPOSITE: {composite:.3f}')
