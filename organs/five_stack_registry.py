import importlib

class FiveStackOrganRegistry:
    """
    Loads ONLY the organs required for the five-stack viewer.
    This avoids loading hundreds of Cathedral organs that do not
    produce packet fields.
    """

    REQUIRED_ORGANS = [
        "router_organ.RouterOrgan",
        "english_field_organ.EnglishFieldOrgan",
        "language_organ.LanguageOrgan",
        "story_organ.StoryOrgan",
        "story_type_organ.StoryTypeOrgan",   # <-- ADDED
        "brush_up_organ.BrushUpOrgan",
        "idea_engine_organ.IdeaEngineOrgan",
        "gravity_organ.GravityOrgan",
        "emergence_gate_cathedral.EmergenceGateCathedral",
    ]

    def load_all(self, creature):
        organs = []

        for path in self.REQUIRED_ORGANS:
            module_name, class_name = path.split(".")
            module_path = f"organs.{module_name}"

            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)

                try:
                    organ = cls(creature)
                except TypeError:
                    organ = cls()

                organs.append(organ)

            except Exception as e:
                print(f"[FiveStackOrganRegistry] Failed to load {path}: {e}")

        return organs
