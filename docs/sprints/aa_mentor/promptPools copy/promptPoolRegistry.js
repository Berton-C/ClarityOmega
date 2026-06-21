// Import prompt pool modules
const introspectivePrompts = require('./introspectivePrompts');
const natureOfReflectionPrompts = require('./natureOfReflectionPrompts');
const immersiveTouchPrompts = require('./immersiveTouchPrompts');
const emptinessAndImpermanence = require('./emptinessAndImpermanence');
const freshPerspectivesPrompts = require('./freshPerspectivesPrompts');
const innateWellBeingPrompts = require('./innateWellBeingPrompts');
// Import additional prompt pools here as needed

// Export an object that maps identifiers to their respective modules
module.exports = {
    // Add additional prompt pools here...

    emptinessAndImpermanence: {
        prompts: emptinessAndImpermanence,
        description: "Exploring The Unseen Nature of Thought and Consciousness",
        label: "Perception and Phenomena",
        category: "Thought and Consciousness",
    },
    freshPerspectivesPrompts: {
        prompts: freshPerspectivesPrompts,
        description: "New Perspectives",
        label: "Exploring the weightlessness of thinking",
        category: "Insights and Experience",
    },
    innateWellBeingPrompts: {
        prompts: innateWellBeingPrompts,
        description: "Exploring Innate Well-Being",
        label: "Innate Well-Being --> Unbroken Well-Being",
        category: "Exploring Innate Intelligence"
    },
    introspectivePrompts: {
        prompts: introspectivePrompts,
        description: "Exploring Our Natural",
        label: "Innate Wisdom --> irrepressible new thought",
        category: "Exploring Innate Intelligence"
    },
    natureOfReflectionPrompts: {
        prompts: natureOfReflectionPrompts,
        description: "Inviting Our Learners",
        label: "Reflection and Insight",
        category: "Inviting Our Learners"
    },
    immersiveTouchPrompts: {
        prompts: immersiveTouchPrompts,
        label: "Immersive Touch",
        category: "Exploring Our Learners"
    }
};