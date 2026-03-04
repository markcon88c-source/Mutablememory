class SentenceRetryMemoryOrgan:
    def __init__(self, creature):
        # The creature reference is required so the organ can
        # read/write shared state if needed.
        self.creature = creature

        # Local retry memory store
        self.entries = []

    def record_retry(self, words, forces, stability):
        """
        Store a snapshot of a retry attempt.
        """
        self.entries.append((words[:], forces.copy(), stability))

        # Prevent unbounded growth
        if len(self.entries) > 50:
            self.entries.pop(0)

    def get_recent(self, n=5):
        """
        Return the most recent n retry entries.
        """
        return self.entries[-n:]
