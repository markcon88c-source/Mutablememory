# organs/glyph_mapper.py

class GlyphMapper:
    """
    Light-wiring language organ.
    Converts force values (0.0–1.0) into letters A–Z + Ø.
    Produces uppercase for structural forces and lowercase for textures.
    """

    # 27-letter alphabet + null
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZØ"
    LOWER = "abcdefghijklmnopqrstuvwxyzØ"

    @staticmethod
    def force_to_letter(value, lowercase=False):
        """
        Maps a force value (0.0–1.0) to one of 27 letters.
        """
        if value is None:
            return "Ø"

        # clamp
        v = max(0.0, min(1.0, float(value)))

        index = int(v * 26)  # 0–26
        if lowercase:
            return GlyphMapper.LOWER[index]
        return GlyphMapper.ALPHABET[index]

    @staticmethod
    def forces_to_glyph(forces):
        """
        Converts a full force dict into a glyph string.
        Example output: 'VDRBXL'
        """
        if not forces:
            return "Ø"

        return "".join([
            GlyphMapper.force_to_letter(forces.get("spark")),
            GlyphMapper.force_to_letter(forces.get("drift")),
            GlyphMapper.force_to_letter(forces.get("echo")),
            GlyphMapper.force_to_letter(forces.get("chaos")),
            GlyphMapper.force_to_letter(forces.get("clarity")),
            GlyphMapper.force_to_letter(forces.get("memory")),
            GlyphMapper.force_to_letter(forces.get("pressure")),
        ])
