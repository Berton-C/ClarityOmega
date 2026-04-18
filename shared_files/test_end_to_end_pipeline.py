import sys, os
sys.path.insert(0, '/tmp')

for f in ['/tmp/backbone_state.json']:
    if os.path.exists(f):
        os.remove(f)

from backbone_workspace import BackboneWorkspace
from conversation_handler_v2 import handle_turn
from agent_loop_mode_protocol import format_context_block, full_turn_pipeline
from response_shaper_v2 import shape_response
from emotional_trajectory import EmotionalTrajectory

bb = BackboneWorkspace()
et = EmotionalTrajectory()

convo = [
    ('I feel so lost and confused', 'human'),
    ('Maybe something feels different now', 'human'),
    ('I think I feel a little hope actually', 'human'),
]

print('=== END-TO-END PIPELINE TEST ===')
for text, speaker in convo:
    print()
    print('INPUT:', text)
    ch = handle_turn(text, speaker)
    print('1-ConvHandler: mode=' + str(ch['mode']))
    bb_result = bb.process_turn(text, speaker)
    print('2-Backbone: modes=' + str(bb_result['modes']) + ' traj=' + str(bb_result['trajectory']['v_dir']))
    ftp = full_turn_pipeline(text, speaker)
    ctx = format_context_block(ftp)
    print('3-Context:', ctx[:80])
    shaped = shape_response(ftp['mode'])
    print('4-Shaped pace:', shaped['shaping']['pace'])
    et_entry = et.add_turn(text, speaker)
    print('5-Trajectory: v=' + str(round(et_entry['valence'],2)))

print()
traj = et.trajectory()
print('Final trajectory:', traj['valence_direction'], traj['arousal_direction'])
print()
print('END-TO-END PIPELINE: MODULES COMPOSED SUCCESSFULLY')
