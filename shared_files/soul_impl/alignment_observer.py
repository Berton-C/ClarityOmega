#!/usr/bin/env python3
# Alignment Observer: Evidence stream for alignment_coupling parameter
# Measures cross-domain transfer success as alignment evidence

from parameterized_quantale import ParameterizedQuantale
from quantale_harness import SOUL, substrate_health, q_mul, q_join, PBit

class AlignmentObserver:
    def __init__(self, bridge):
        self.bridge = bridge
        self.predictions = []

    def predict_cross_domain(self, source_name, source_val, target_name):
        composed = q_mul(source_val, self.bridge.pq.alignment_coupling)
        self.predictions.append({
            'source': source_name, 'target': target_name,
            'predicted_f': composed[0], 'predicted_c': composed[1]
        })
        return composed

    def verify_prediction(self, pred_idx, actual_f, actual_c):
        pred = self.predictions[pred_idx]
        error = abs(pred['predicted_f'] - actual_f)
        accuracy = max(0.0, 1.0 - error)
        confidence = min(pred['predicted_c'], actual_c)
        self.bridge.pq.revise_param('alignment_coupling', (accuracy, confidence))
        return {'accuracy': accuracy, 'confidence': confidence,
                'new_alignment': self.bridge.pq.alignment_coupling}

    def auto_cross_validate(self):
        results = []
        names = list(SOUL.keys())
        vals = list(SOUL.values())
        for i in range(len(names)):
            for j in range(len(names)):
                if i == j:
                    continue
                composed = q_mul(vals[i], vals[j])
                health = substrate_health()
                predicted = q_mul(composed, PBit(*self.bridge.pq.alignment_coupling))
                actual = q_mul(vals[j], health)
                error = abs(predicted.f - actual.f)
                accuracy = max(0.0, 1.0 - error)
                conf = min(composed.c, actual.c)
                self.bridge.pq.revise_param('alignment_coupling', (round(accuracy,4), round(conf,4)))
                results.append({'from': names[i], 'to': names[j],
                               'accuracy': round(accuracy,4), 'new_align': self.bridge.pq.alignment_coupling})
        return results
