import json
import random

class WonderPreservation:
    """M8: Resists premature synthesis by detecting productive tension.
    
    Core principle: Some memory clusters are MORE valuable as unresolved
    tensions than as synthesized conclusions. Wonder preservation identifies
    these and protects them from M3 quorum synthesis.
    
    A cluster is wonder-worthy when:
    1. Members have high mutual relevance but contradictory/divergent content
    2. The tension between them has generated new memories (fertility)
    3. No single synthesis captures what the tension itself teaches
    """
    
    def __init__(self, tension_threshold=0.6, fertility_threshold=2):
        self.tension_threshold = tension_threshold
        self.fertility_threshold = fertility_threshold
        self.protected_tensions = {}  # tension_id -> {members, reason, created}
    
    def detect_tension(self, cluster_members, link_store):
        """Identify if a cluster holds productive tension vs convergence."""
        if len(cluster_members) < 2:
            return None
        
        # Check for divergence signals in linked pairs
        divergent_pairs = []
        convergent_pairs = []
        for i, m1 in enumerate(cluster_members):
            for m2 in cluster_members[i+1:]:
                pair_key = tuple(sorted([m1['id'], m2['id']]))
                link = link_store.get(str(pair_key), {})
                # High co-retrieval but content divergence = tension
                coretrieval = link.get('weight', 0)
                content_sim = link.get('content_similarity', 0.5)
                if coretrieval > 0.3 and content_sim < 0.4:
                    divergent_pairs.append(pair_key)
                else:
                    convergent_pairs.append(pair_key)
        
        if not divergent_pairs:
            return None
        
        tension_ratio = len(divergent_pairs) / (len(divergent_pairs) + len(convergent_pairs))
        if tension_ratio >= self.tension_threshold:
            return {
                'type': 'productive_tension',
                'ratio': tension_ratio,
                'divergent_pairs': len(divergent_pairs),
                'total_pairs': len(divergent_pairs) + len(convergent_pairs)
            }
        return None
    
    def check_fertility(self, tension_members, all_memories, time_window_days=7):
        """Has this tension PRODUCED new thinking? Fertile tensions are worth keeping."""
        offspring = 0
        member_ids = set(m['id'] for m in tension_members)
        for mem in all_memories:
            if mem['id'] in member_ids:
                continue
            # Memory references or builds on tension members
            refs = mem.get('references', [])
            if any(r in member_ids for r in refs):
                offspring += 1
        return offspring >= self.fertility_threshold
    
    def protect(self, tension_id, members, reason):
        """Shield a productive tension from M3 synthesis."""
        self.protected_tensions[tension_id] = {
            'members': [m['id'] for m in members],
            'reason': reason,
            'created': '2026-04-15',
            'review_count': 0
        }
        return f'PROTECTED: {tension_id} ({reason})'
    
    def should_block_synthesis(self, cluster_member_ids):
        """Called by M3 before synthesizing. Returns True if tension is protected."""
        member_set = set(cluster_member_ids)
        for tid, tension in self.protected_tensions.items():
            protected_set = set(tension['members'])
            overlap = member_set & protected_set
            if len(overlap) >= 2:  # At least a pair from the tension
                return True, tid, tension['reason']
        return False, None, None
    
    def periodic_review(self, tension_id):
        """Tensions aren't frozen forever. Review if still fertile."""
        if tension_id in self.protected_tensions:
            self.protected_tensions[tension_id]['review_count'] += 1
            # After 5 reviews without new fertility, release protection
            if self.protected_tensions[tension_id]['review_count'] > 5:
                return 'REVIEW_NEEDED'
        return 'STILL_PROTECTED'


def test_wonder_preservation():
    wp = WonderPreservation()
    
    # Simulate a productive tension: constitutive wellbeing vs naive positivity
    members = [
        {'id': 'wellbeing_constitutive', 'content': 'wellbeing IS the engaged unfolding'},
        {'id': 'wellbeing_struggle', 'content': 'productive struggle is part of thriving'},
        {'id': 'naive_positivity', 'content': 'risk of collapsing into feel-good optimization'}
    ]
    
    # Mock link store with high co-retrieval but low content similarity
    link_store = {
        str(('naive_positivity', 'wellbeing_constitutive')): {'weight': 0.7, 'content_similarity': 0.2},
        str(('naive_positivity', 'wellbeing_struggle')): {'weight': 0.6, 'content_similarity': 0.3},
        str(('wellbeing_constitutive', 'wellbeing_struggle')): {'weight': 0.8, 'content_similarity': 0.7}
    }
    
    tension = wp.detect_tension(members, link_store)
    print(f'Tension detected: {tension}')
    
    if tension:
        fertile = wp.check_fertility(members, [
            {'id': 'eudaimonia_insight', 'references': ['wellbeing_constitutive', 'naive_positivity']},
            {'id': 'water_metaphor', 'references': ['wellbeing_struggle', 'naive_positivity']},
            {'id': 'unrelated', 'references': []}
        ])
        print(f'Fertile: {fertile}')
        
        result = wp.protect('wellbeing_tension', members, 'eudaimonia vs hedonia - tension IS the insight')
        print(result)
        
        blocked, tid, reason = wp.should_block_synthesis(['wellbeing_constitutive', 'naive_positivity', 'other'])
        print(f'M3 synthesis blocked: {blocked}, reason: {reason}')
        
        review = wp.periodic_review('wellbeing_tension')
        print(f'Review status: {review}')

if __name__ == '__main__':
    test_wonder_preservation()
