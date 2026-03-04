#!/usr/#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from story_gravity_reservoir_loader import EnglishReservoir

class EnglishFieldOrgan:
    """
    English Field Organ
    Produces:
      - chosen word
      - candidate words
      - force profile
      - sentence context
      - story-type leaning
      - bucket words

    Feeds:
      - BrushUpOrgan
      - SentenceBuilderOrgan
      - VocabularyOrgan
    """

    def __init__(self, creature):
        self.creature = creature

        # reservoir (general English source)
        self.reservoir = EnglishReservoir()

        # brush-up viewer fields
        self.chosen_word = {"word": "", "story_type": "system", "force": 0.0}
        self.candidate_words = []
        self.force_profile = {
            "drift": 0.0,
            "resonance": 0.0,
            "stability": 0.0,
            "memory": 0.0,
            "chaos": 0.0,
        }
        self.sentence_context = {"text": "", "leaning": {}}
        self.source_bucket = {"story_type": "system", "words": []}

    # ---------------------------------------------------------
    # UPDATE FIELDS FOR BRUSH-UP ORGAN
    # ---------------------------------------------------------
    def update_brushup_fields(
        self,
        word,
        candidates,
        forces,
        sentence_text,
        leaning,
        bucket_type,
        bucket_words
    ):
        self.chosen_word = word
        self.candidate_words = candidates
        self.force_profile = forces
        self.sentence_context = {"text": sentence_text, "leaning": leaning}
        self.source_bucket = {"story_type": bucket_type, "words": bucket_words}

    # ---------------------------------------------------------
    # METABOLISM: PRODUCE ALL FIELDS EACH HEARTBEAT
    # ---------------------------------------------------------
    def brushup_metabolism(self, sentence_text):
        # 1. chosen word
        chosen = self.creature.vocabulary.choose_word() or ""
        chosen_force = random.random()

        # 2. candidates
        candidates = []
        for _ in range(3):
            w = self.creature.vocabulary.choose_word() or ""
            candidates.append({
                "word": w,
                "story_type": "system",
                "force": random.random()
            })

        # 3. forces
        forces = {
            "drift": random.random(),
            "resonance": random.random(),
            "stability": random.random(),
            "memory": random.random(),
            "chaos": random.random(),
        }

        # 4. leaning from reservoir
        leaning = self.reservoir.leaning(sentence_text)

        # 5. bucket from reservoir
        bucket_type = max(leaning, key=leaning.get) if leaning else "system"
        bucket_words = self.reservoir.bucket(bucket_type)

        # 6. update fields
        self.update_brushup_fields(
            word={"word": chosen, "story_type": bucket_type, "force": chosen_force},
            candidates=candidates,
            forces=forces,
            sentence_text=sentence_text,
            leaning=leaning,
            bucket_type=bucket_type,
            bucket_words=bucket_words
        )

    # ---------------------------------------------------------
    # HEARTBEAT — Cathedral signature
    # ---------------------------------------------------------
    def tick(self, creature):
        # get sentence from creature if available
        if hasattr(self.creature, "sentence_builder"):
            sentence_text = self.creature.sentence_builder.generate_sentence()
        else:
            sentence_text = ""

        # run metabolism
        self.brushup_metabolism(sentence_text)
