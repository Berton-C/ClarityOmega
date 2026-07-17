# Live Integration Spec: Backbone -> Response Shaping

## Pipeline Flow
1. User message arrives
2. Call get_response_directives(user_text, speaker_id) from backbone_bridge.py
3. Returns guidance string like: BACKBONE GUIDANCE: [mode] instructions. VAD=v/a/d MODES=list
4. Prepend guidance string to system context as internal-only block
5. Generate response informed by backbone guidance
6. Send response to user (guidance block stripped - user never sees it)

## Key Files
- phrase_boost.py: 44 phrase patterns with VAD adjustments
- backbone_workspace_v4.py: V6 routing logic, ChromaDB VAD lookups
- respond_with_backbone.py: MODE_GUIDANCE dict, shape_response()
- backbone_bridge.py: get_response_directives() returns formatted guidance
- prompt_composer.py: compose_prompt() builds full prompt with context_block
- conversation_handler.py: generate_context_block() for LLM prepend

## Routing Modes (V6 confirmed 15/15)
- empathic-attunement: V<-2.0 (any arousal) OR V<-1.3 with A>-0.85
- gentle-activation: V<-0.5 OR low-arousal A<-1.5 with V>-1.3
- momentum-amplification: V>0.5
- witnessing-celebration: V>0.0 with phrase boosts present
- collaborative-exploration: D>-0.3 and V>-0.5
- recalibration: shift>0.5 after turn 1
- neutral-presence: fallback when no other mode triggers

## Integration Point
The backbone_bridge.get_response_directives() output is the single call needed.
It returns a human-readable guidance string ready for context injection.
