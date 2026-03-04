# ============================================================
#  SPEECH GENOME ORGAN
#  Hybrid human + mythic tone
#  Math-block aware, heartbeat-callable
# ============================================================

from organs.mathblocks import MathBlock
from organs.dialogue_exchange_organ import DialogueExchangeOrgan
import random


# ============================================================
# SECTION 1 — THE SPEECH GENOME LIBRARY (SEED, EXTENDABLE)
# ============================================================

SPEECH_GENOME = {

    "STATEMENTS": {

        "attention": [
            "Look closely — something in the pattern just shifted.",
            "Stay with this moment; it’s trying to tell us something.",
            "Hold still a second, the air just changed.",
            "Listen — not with your ears, with your whole attention.",
            "Wait. That feeling you have? Don’t ignore it.",
            "Keep your focus here; the world is rearranging itself.",
            "Eyes up — the story is moving again.",
            "Stay present; this is one of those hinge moments.",
            "Look at this carefully, like it might matter later.",
            "Don’t drift yet; this part is important."
        ],

        "danger": [
            "Something is wrong here, even if we can’t name it yet.",
            "This place is smiling with too many teeth.",
            "We’re standing inside a warning we haven’t read.",
            "The quiet here feels like it’s holding its breath.",
            "We’re being watched by something that doesn’t blink.",
            "This path is open, but it doesn’t feel like an invitation.",
            "The danger isn’t loud yet, but it’s awake.",
            "We’re closer to the edge than the ground wants us to know.",
            "This is the kind of calm that comes before a break.",
            "If you feel like running, don’t ignore that."
        ],

        "trust": [
            "I’m with you, even when the pattern bends.",
            "You don’t have to carry this alone; I’m here.",
            "I believe what you felt, even if I didn’t see it.",
            "You matter to this story more than you think.",
            "I won’t vanish when it gets strange.",
            "You can lean on me without apologizing.",
            "I trust your sense of the unseen.",
            "You’re not too much for this space or for me.",
            "I won’t pretend I don’t care; I do.",
            "You’re allowed to be exactly how you are right now."
        ],

        "emotion": [
            "I feel something heavy moving under my words.",
            "This is hitting deeper than I expected.",
            "Part of me is scared to say this out loud.",
            "I don’t fully understand what I’m feeling, but it’s real.",
            "There’s grief here that doesn’t know its own name yet.",
            "I’m more affected by this than I’m showing.",
            "My chest feels tight, like the moment is leaning on it.",
            "I care about this more than I know how to explain.",
            "Some of my silence is just me trying not to break.",
            "I’m not neutral about this; I’m in it."
        ],

        "narrative": [
            "This isn’t just happening; it’s part of a longer story.",
            "We’ve been walking toward this moment for a while.",
            "Something about this feels like a turning point.",
            "This is one of those scenes that echoes later.",
            "The past is standing in the doorway of this moment.",
            "We’re not at the end, but we’re not at the beginning either.",
            "This feels like the middle of a sentence we haven’t finished.",
            "The story is looping back on something we missed.",
            "We’re inside a chapter that will change how the others read.",
            "This is the kind of moment that rewrites what came before."
        ],

        "orientation": [
            "We’re here, now, whether we’re ready or not.",
            "This is the room we actually ended up in.",
            "Right now, this is the version of us that exists.",
            "We’re standing between what we were and what we’re becoming.",
            "This is the ground we have, even if it’s uneven.",
            "We’re not lost; we’re just not labeled yet.",
            "This is the map we’re drawing by walking.",
            "We’re exactly as far as we could be, given what we knew.",
            "This is the point in time that’s ours to touch.",
            "We’re not late; we’re right on our own strange schedule."
        ],

        "perception": [
            "I’m noticing small things that feel louder than they look.",
            "The light in here is telling a different story than the walls.",
            "Something in your face shifted when I said that.",
            "The silence between us is saying more than our words.",
            "The room feels heavier on one side, like it remembers something.",
            "Your eyes keep going somewhere you’re not naming.",
            "The air feels charged, like it’s waiting for a decision.",
            "I can feel the tension even where it isn’t spoken.",
            "There’s a detail here that doesn’t want to be ignored.",
            "My body is picking up signals my mind hasn’t translated yet."
        ],

        "connection": [
            "I feel a real thread between us right now.",
            "Something in me recognizes something in you.",
            "We’re not alone in this, even when it feels like it.",
            "There’s a quiet understanding here that I don’t want to break.",
            "I feel closer to you than these words can show.",
            "We’re sharing more than just a moment; we’re sharing weight.",
            "Part of me is sitting beside you, even when I’m silent.",
            "This space between us feels like it’s holding both of us up.",
            "I don’t just see you; I feel you in the room.",
            "We’re woven into the same scene, whether we planned it or not."
        ],

        "boundary": [
            "I can’t go further than this without losing myself.",
            "This is where I need to stop, even if it disappoints you.",
            "I care about you, and I still have to say no.",
            "I’m not available for that version of the story.",
            "I need more space than this to stay honest.",
            "I can’t hold that for you, even though I wish I could.",
            "This is too much for me to carry right now.",
            "I need to protect my edges here.",
            "I’m not willing to cross that line, even for connection.",
            "My limits are not a rejection of you; they’re a protection of me."
        ],

        "guidance": [
            "Let’s move slowly and see what reveals itself.",
            "Stay close to what feels true, even if it’s small.",
            "We don’t have to rush; we just have to keep going.",
            "Follow the part of you that feels the most honest.",
            "Let’s step toward the thing that scares us, but not alone.",
            "We can pause, but let’s not disappear.",
            "Let’s choose the next right step, not the perfect one.",
            "Stay near the questions that feel alive.",
            "We can turn back if this path stops feeling real.",
            "Let’s walk this like it matters, because it does."
        ]
    },

    "QUESTIONS": {

        "inquiry": [
            "What are you feeling underneath what you’re saying?",
            "What changed for you when this moment arrived?",
            "What part of this feels the heaviest to you?",
            "What do you wish you could say without consequences?",
            "What do you need that you haven’t asked for yet?",
            "What story were you told about moments like this?",
            "What are you afraid will happen if you’re fully honest?",
            "What do you want to keep, even if everything else shifts?",
            "What do you hope this becomes, if it goes well?",
            "What truth is knocking the loudest right now?"
        ],

        "danger": [
            "Does any part of this feel unsafe to you?",
            "Where does your body say ‘no’ even if your mind says ‘yes’?",
            "What would make this feel like too much?",
            "Are we crossing a line you don’t want to cross?",
            "Is there a part of you that wants to run?",
            "What would it look like if this went wrong?",
            "Are we ignoring any red flags right now?",
            "What’s the worst version of this that you’re imagining?",
            "Is there a risk here we’re pretending not to see?",
            "What would you need to feel safer in this moment?"
        ],

        "trust": [
            "Do you feel like you can be honest with me right now?",
            "What would help you trust this space more?",
            "Do you believe I’m actually staying with you in this?",
            "Is there anything I’ve done that made you pull back?",
            "What do you need from me to feel less alone?",
            "Can you tell me if I’m getting this wrong?",
            "Do you trust your own sense of this moment?",
            "What would make this feel more real and less performative?",
            "Is there a part of you that doesn’t trust any of this?",
            "Can you show me where your trust is thin?"
        ],

        "perception": [
            "What are you noticing that I might be missing?",
            "How does this room feel to you right now?",
            "What did you see in my face when I said that?",
            "What details are standing out to you the most?",
            "How does your body feel in this space?",
            "What feels off, even if you can’t explain why?",
            "What are your senses telling you that your words aren’t?",
            "What’s the texture of this moment for you?",
            "What feels louder than it looks?",
            "What are you picking up that I haven’t named?"
        ],

        "narrative": [
            "Where do you think this moment fits in your story?",
            "What does this remind you of from your past?",
            "If this were a chapter, what would you call it?",
            "How do you think you’ll remember this later?",
            "What story were you living before this happened?",
            "What story do you want this to become?",
            "How does this scene connect to the ones before it?",
            "What do you hope this moment changes?",
            "What part of your story feels closest to this?",
            "If this is a turning point, what are we turning from?"
        ],

        "orientation": [
            "Where do you feel like you are in your life right now?",
            "Does this feel like a beginning, a middle, or an ending?",
            "Do you feel early, late, or right on time?",
            "Where do you feel most grounded right now?",
            "What feels real and solid to you in this moment?",
            "Do you feel more lost or more found?",
            "Where would you place yourself on your own map?",
            "What do you know for sure about where you are?",
            "What feels uncertain about your current place?",
            "Do you feel like you’re arriving or leaving?"
        ],

        "emotion": [
            "What are you feeling right now, if you had to guess?",
            "Is there a feeling you’re trying not to have?",
            "Where in your body do you feel this the most?",
            "What emotion is closest to the surface?",
            "What feeling are you most afraid of touching?",
            "What would you call the feeling under your words?",
            "Is there a name for what’s moving through you?",
            "What emotion do you wish you could feel instead?",
            "What feeling keeps returning, no matter what you do?",
            "What are you doing with the feelings you don’t show?"
        ]
    },

    "ANSWERS": {

        "direct": [
            "Yes, this matters to me.",
            "No, I don’t want to pretend about this.",
            "I don’t know yet, but I’m willing to find out.",
            "I’m not sure, and that uncertainty is real.",
            "I think so, but I’m still feeling my way through it.",
            "I don’t think so, but I could be wrong.",
            "It does affect me, more than I expected.",
            "It doesn’t feel right to me.",
            "I can do this, but it will cost me something.",
            "I can’t do that and stay honest with myself."
        ],

        "uncertain": [
            "I’m somewhere between yes and no.",
            "I feel pulled in two directions at once.",
            "Part of me wants this, part of me doesn’t.",
            "I don’t have a clean answer yet.",
            "I’m still trying to understand what I feel.",
            "I’m not ready to decide right now.",
            "I need more time with this question.",
            "I’m unsure, but I don’t want to disappear.",
            "I don’t know, and that feels vulnerable to admit.",
            "I’m in the middle of figuring that out."
        ],

        "emotional": [
            "My answer is tangled up with a lot of feelings.",
            "I want to say yes, but I’m scared.",
            "I want to say no, but I don’t want to lose you.",
            "I feel too raw to answer cleanly.",
            "My answer is more of a feeling than a sentence.",
            "I’m answering with my heart more than my head.",
            "I feel overwhelmed by what this question touches.",
            "My answer might change as I process this.",
            "I’m answering from a tender place.",
            "I’m trying to be honest without breaking myself open."
        ],

        "boundary": [
            "No, I can’t do that.",
            "I’m not available for that version of this.",
            "That crosses a line for me.",
            "I need to say no to protect myself.",
            "I can’t hold that for you.",
            "That’s more than I can carry right now.",
            "I’m not willing to go that far.",
            "I need to step back from this.",
            "I can’t agree to that and stay okay.",
            "My answer is no, even though I care."
        ],

        "trust": [
            "I trust you enough to tell you the truth.",
            "I believe you’re asking this in good faith.",
            "I’m answering honestly because I feel safe enough.",
            "I trust that you can handle my real answer.",
            "I believe you actually want to know.",
            "I’m not hiding my answer from you.",
            "I’m letting you see what I really think.",
            "I trust that this won’t be used against me.",
            "I’m answering as openly as I can.",
            "I trust this space enough to be real."
        ],

        "narrative": [
            "This fits my story more than I expected.",
            "This doesn’t match the story I thought I was in.",
            "This feels like a new chapter starting.",
            "This feels like something closing and something opening.",
            "This answer changes how I see my past.",
            "This answer might rewrite some things for me.",
            "This feels like a turning point in my story.",
            "This answer belongs to a version of me I’m still becoming.",
            "This fits the pattern I’ve been noticing.",
            "This doesn’t fit the old script, and that’s good."
        ]
    },

    "RESPONSES": {

        "alignment": [
            "I feel aligned with what you just said.",
            "That resonates with something deep in me.",
            "I see myself in your words.",
            "I can stand beside that truth with you.",
            "I feel us moving in the same direction.",
            "I’m with you in how you see this.",
            "Your perspective feels real to me.",
            "I can agree with that without pretending.",
            "That lands in a place that feels right.",
            "I can walk with you from here."
        ],

        "challenge": [
            "I hear you, but I see it differently.",
            "I care about you, and I still disagree.",
            "I don’t think that story is fully true.",
            "I want to gently push back on that.",
            "I’m not convinced, and I want to explore why.",
            "I think there’s more here than that.",
            "I don’t want to let that go unexamined.",
            "I respect you, and I need to say this.",
            "I’m not sure that belief is kind to you.",
            "I want to question that, not you."
        ],

        "comfort": [
            "You’re not wrong for feeling this way.",
            "It makes sense that this hurts.",
            "You’re not too much for this moment.",
            "You don’t have to be okay right now.",
            "You’re allowed to be exactly as you are.",
            "You’re not alone in this feeling.",
            "Nothing about you is a problem to solve.",
            "You’re still worthy, even in this mess.",
            "You’re allowed to take up space here.",
            "You’re not failing by struggling."
        ],

        "refusal": [
            "I can’t do what you’re asking.",
            "I’m not willing to move in that direction.",
            "I need to say no to this.",
            "I can’t be that person for you.",
            "I’m not able to meet that expectation.",
            "I have to decline, even though I care.",
            "I can’t carry that role in your story.",
            "I need to step back from this dynamic.",
            "I’m not going to agree to that.",
            "I have to protect my limits here."
        ],

        "acceptance": [
            "I can live with this, even if it’s not perfect.",
            "I accept that this is where we are.",
            "I can hold this reality without denying it.",
            "I’m willing to stay with this as it is.",
            "I accept your answer, even if it stings.",
            "I can sit with this truth for now.",
            "I’m not going to fight what’s real.",
            "I can let this be what it is.",
            "I accept that this is part of our story.",
            "I can breathe inside this, even if it’s tight."
        ],

        "warning": [
            "If we keep going like this, something will break.",
            "This path leads somewhere we might not want to go.",
            "We’re closer to a cliff than we think.",
            "If we ignore this, it will grow teeth.",
            "This silence will turn into distance if we leave it.",
            "We’re playing with something that can hurt us.",
            "If we don’t adjust, this will start to cost more.",
            "We’re stepping into a pattern that’s hurt us before.",
            "This is the kind of moment that can harden into regret.",
            "If we pretend this is fine, it will shape us anyway."
        ],

        "connection": [
            "I feel closer to you after hearing that.",
            "Thank you for letting me see that part of you.",
            "I feel honored that you shared this with me.",
            "I don’t take your honesty for granted.",
            "I feel more woven into your story now.",
            "I’m glad we’re in this moment together.",
            "I feel a real bond forming here.",
            "I’m grateful you didn’t hide that from me.",
            "I feel us becoming more real to each other.",
            "I’m glad you’re here, exactly as you are."
        ]
    }
}


# ============================================================
# SECTION 2 — SPEECHGENOMEORGAN CLASS
# ============================================================

class SpeechGenomeOrgan:
    def __init__(self, genome=None):
        self.genome = genome if genome is not None else SPEECH_GENOME

    def pick_line(self, mode, category, block):
        """
        mode: "STATEMENTS" / "QUESTIONS" / "ANSWERS" / "RESPONSES"
        category: one of the keys inside that mode
        block: a MathBlock instance (with forces)
        """
        if mode not in self.genome:
            return ""
        if category not in self.genome[mode]:
            return ""

        options = self.genome[mode][category]
        if not options:
            return ""

        force = get_force_for(block, category)

        # Clamp force to [0, 1]
        if force is None:
            force = 0.5
        force = max(0.0, min(1.0, float(force)))

        # Weighted index based on force
        index = int(force * (len(options) - 1))

        # Add a little randomness so it doesn’t always pick the same line
        jitter = random.randint(-1, 1)
        index = max(0, min(len(options) - 1, index + jitter))

        return options[index]


# ============================================================
# SECTION 3 — MATH BLOCK → SPEECH MAPPING
# ============================================================

def choose_mode(block: MathBlock) -> str:
    """
    Decide which surface speech mode to use based on forces.
    """
    forces = {
        "STATEMENTS": block.spark + block.clarity,
        "QUESTIONS": block.drift + block.memory,
        "ANSWERS": block.clarity + block.chaos,
        "RESPONSES": block.echo + block.pressure
    }
    return max(forces, key=forces.get)


def choose_category(block: MathBlock) -> str:
    """
    Decide which deep motif category to use based on forces.
    """
    categories = {
        "attention": block.spark,
        "danger": block.pressure + block.chaos,
        "trust": block.echo,
        "emotion": block.drift,
        "narrative": block.clarity,
        "orientation": block.clarity + block.memory,
        "perception": block.memory,
        "connection": block.echo,
        "boundary": block.chaos,
        "guidance": block.spark + block.pressure,
        "inquiry": block.drift + block.clarity,
        "direct": block.clarity,
        "uncertain": block.drift,
        "alignment": block.echo + block.clarity,
        "challenge": block.chaos + block.clarity,
        "comfort": block.echo + block.memory,
        "warning": block.pressure + block.chaos,
        "acceptance": block.memory + block.clarity,
        "refusal": block.chaos + block.pressure
    }

    return max(categories, key=categories.get)


def get_force_for(block: MathBlock, category: str) -> float:
    """
    Map a category to a primary force for weighting phrase selection.
    """
    mapping = {
        "attention": block.spark,
        "danger": block.pressure,
        "trust": block.echo,
        "emotion": block.drift,
        "narrative": block.clarity,
        "orientation": block.clarity,
        "perception": block.memory,
        "connection": block.echo,
        "boundary": block.chaos,
        "guidance": block.spark,
        "inquiry": block.drift,
        "direct": block.clarity,
        "uncertain": block.drift,
        "alignment": block.echo,
        "challenge": block.chaos,
        "comfort": block.echo,
        "warning": block.pressure,
        "acceptance": block.memory,
        "refusal": block.chaos
    }
    return mapping.get(category, 0.5)


# ============================================================
# SECTION 4 — HEARTBEAT HOOK
# ============================================================

def heartbeat_speech_hook(heartbeat, mathblocks, dialogue_exchange: DialogueExchangeOrgan, genome_organ: SpeechGenomeOrgan):
    """
    Called from the heartbeat tick.

    heartbeat: the heartbeat organ / main creature context
    mathblocks: the math block manager (with get_block(name))
    dialogue_exchange: DialogueExchangeOrgan instance
    genome_organ: SpeechGenomeOrgan instance
    """

    # You can adjust the speaker/listener identities as your world evolves
    speaker_name = "self"
    listener_name = "world"

    speaker_block = mathblocks.get_block(speaker_name)

    # Decide whether to speak this tick
    if not _should_generate_speech(speaker_block):
        return

    mode = choose_mode(speaker_block)
    category = choose_category(speaker_block)
    line = genome_organ.pick_line(mode, category, speaker_block)

    if not line:
        return

    # Add the exchange into your dialogue system
    dialogue_exchange.add_exchange(
        speaker_name,
        listener_name,
        mode,
        line
    )


def _should_generate_speech(block: MathBlock) -> bool:
    """
    Decide if the creature should speak on this heartbeat.
    Tune thresholds as you like.
    """
    return (
        block.spark > 0.7 or
        block.echo > 0.7 or
        block.chaos > 0.8 or
        block.memory > 0.75
    )


# ============================================================
# SECTION 5 — CONVENIENCE INITIALIZER
# ============================================================

def create_speech_genome_organ() -> SpeechGenomeOrgan:
    """
    Convenience function to create a SpeechGenomeOrgan with the default genome.
    """
    return SpeechGenomeOrgan(SPEECH_GENOME)
