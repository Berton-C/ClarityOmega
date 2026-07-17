# VAD Migration Design: Python to MeTTa
## 2026-04-16

### Proven Foundation
Three VAD axes modeled as NAL inheritance chains:
- valence: vad-valence to positive to approach-behavior (0.68/0.520)
- arousal: vad-arousal to high to activation-behavior (0.675/0.459)
- dominance: vad-dominance to control to assertive-behavior (0.663/0.451)

### Migration Blueprint

#### Step 1: VAD Lexicon as MeTTa Atoms
Each NRC VAD word entry becomes:
(= (vad-entry word) (Vec v a d))
Where v/a/d are p-bit encoded values from the NRC lexicon.

#### Step 2: Emotional Comparison as NAL Similarity
Cosine similarity between word vectors becomes:
(|- ((<-> word1 word2) (stv similarity confidence)))
Native NAL similarity judgments replace Python cosine computation.

#### Step 3: Felt-Sense Field as Bundled Vec
9-dimensional relational exchange vectors become:
(= (felt-sense context) (bundle (vad-vec) (relational-depth-vec) (shift-vec) (domain-vec)))
Using existing VSA bundling operations from Goals 1-9.

#### Step 4: Presence Pipeline as NAL Revision
Accumulator with decay becomes temporal revision.
New evidence revises existing presence state, confidence decays naturally.

#### Step 5: Composite Emotional State
Three VAD axes bundled into single state vector:
(= (emotional-state context) (bind (bind vad-v-vec key-valence) (bind vad-a-vec key-arousal) (bind vad-d-vec key-dominance)))
Unbindable by axis key for dimension-specific queries.

### Dependencies
- MeTTa VSA foundation Goals 1-9: CONFIRMED WORKING
- Quantale algebra: CONFIRMED WORKING
- STV-PB bridge: CONFIRMED WORKING
- NRC lexicon file access: NEEDS filesystem path

### Estimated Scope
28 Python components, 5 migration steps, each testable independently.
