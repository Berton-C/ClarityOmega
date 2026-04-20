lines = [
    ';; lib_clarity_reasoning.metta -- ClarityClaw reasoning extension entry point',
    ';; Single import point: add one line to lib_omegaclaw.metta',
    ';; !(import! &self (library omegaclaw lib_clarity_reasoning))',
    '',
    ';; Build on lib_nal foundation (already imported by lib_omegaclaw)',
    ';; Core spec libs (6 per architecture spec)',
    '!(import! &self (library omegaclaw lib_nal_extended))',
    '!(import! &self (library omegaclaw lib_paraconsistent))',
    '!(import! &self (library omegaclaw lib_quantale))',
    '!(import! &self (library omegaclaw lib_web_detect))',
    '!(import! &self (library omegaclaw lib_resonance))',
    '',
    ';; Extended libs (beyond original spec)',
    '!(import! &self (library omegaclaw lib_analogy))',
    '!(import! &self (library omegaclaw lib_ethical_grounding))',
    '!(import! &self (library omegaclaw lib_observer_relativity))',
    '!(import! &self (library omegaclaw lib_gap_dashboard))',
    '!(import! &self (library omegaclaw lib_temporal_continuity))',
    '!(import! &self (library omegaclaw lib_integration))',
]
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_clarity_reasoning.metta', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('entry point rewritten with', len([l for l in lines if l.startswith('!')]), 'imports')
