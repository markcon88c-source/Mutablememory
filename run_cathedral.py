# run_cathedral.py
# Full Cathedral runtime — heartbeat loop + metabolic chain

import time
from creature_cathedral import CathedralCreature

print("Cathedral Creature starting...")

# Instantiate creature
creature = CathedralCreature()

# Emit initial seed packet
creature.bus.emit({
    "type": "seed",
    "text": "hello cathedral"
})

# Main metabolic loop
try:
    while True:
        creature.tick()
        time.sleep(0.10)   # 10 ticks per second
except KeyboardInterrupt:
    print("Cathedral Creature shutting down.")
