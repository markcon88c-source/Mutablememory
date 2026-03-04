# 📝 Vocabulary Force Rolls (Emoji Edition)

def show_vocabulary(state):
    """
    Simple debug viewer for vocabulary pulls.
    This file is only kept for backward compatibility.
    It is NOT used by the SentenceViewer or metabolic viewer.
    """

    vocab = state.get("vocab", [])
    if vocab:
        print("\n📚 Vocabulary Pulls:")
        for item in vocab[-10:]:  # show last 10 pulls
            if isinstance(item, dict):
                word = item.get("word", "?")
                spark = item.get("spark", 0)
                drift_f = item.get("drift", 0)
                echo = item.get("echo", 0)
                chaos = item.get("chaos", 0)
                clarity = item.get("clarity", 0)
                memory_f = item.get("memory", 0)
                pressure_f = item.get("pressure", 0)
                wp = item.get("word_pressure", 0)

                print(
                    f"  {word:<15} | "
                    f"⚡{spark:,}  "
                    f"🌬{drift_f:,}  "
                    f"🔊{echo:,}  "
                    f"🌩{chaos:,}  "
                    f"🔍{clarity:,}  "
                    f"🧠{memory_f:,}  "
                    f"🔥{pressure_f:,}  "
                    f"💠{wp:,}"
                )
            else:
                print(f"  {item}")
    else:
        print("\n📚 No vocabulary data available.")
