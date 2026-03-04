#!/usr/bin/env python3
# rememger2.py — main command router for Rememger 2.0

import sys

# ------------------------------------------------------------
# ORGAN IMPORTS
# ------------------------------------------------------------
# Code retriever organ (pulls code for any organ in the registry)
from organs.code_retriever.code_retriever import cli as code_cli


# ------------------------------------------------------------
# MAIN ROUTER
# ------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: memo2 <command> [args]")
        return

    command = sys.argv[1]

    # -------------------------
    # CODE RETRIEVER
    # -------------------------
    if command == "code":
        # Usage: memo2 code <organ-name>
        # Example: memo2 code scanner
        code_cli()
        return

    # -------------------------
    # PIPELINE (placeholder)
    # -------------------------
    elif command == "pipeline":
        # This will eventually assemble the creature and update the registry.
        print("Pipeline subsystem not yet installed.")
        return

    # -------------------------
    # HELP
    # -------------------------
    elif command in ("help", "-h", "--help"):
        print("Rememger 2.0 — available commands:")
        print("  code <organ>     Show source code for an organ from the pipeline registry")
        print("  pipeline         (placeholder) Run the creature assembly pipeline")
        print("  help             Show this help message")
        return

    # -------------------------
    # UNKNOWN COMMAND
    # -------------------------
    else:
        print(f"Unknown command: {command}")
        print("Use: memo2 help")
        return


# ------------------------------------------------------------
# ENTRYPOINT
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
