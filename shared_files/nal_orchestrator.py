#!/usr/bin/env python3
"""NAL Orchestrator - composes multi-hop inference via sequential |- calls.
MeTTa handles reasoning. Python handles call sequencing. Clean separation."""

def build_deduction(rule_stv, obs_stv):
    return f'(|- ({rule_stv}) ({obs_stv}))'

def two_hop_chain(tone, tone_conf, tone_rule, need_key, need_rule):
    step1 = build_deduction(tone_rule, f'(--> observed-tone {tone}) (stv 1.0 {tone_conf})')
    step2_template = lambda need_conf: build_deduction(need_rule, f'(--> user-need {need_key}) (stv 1.0 {need_conf})')
    return step1, step2_template

print('NAL Orchestrator ready')
