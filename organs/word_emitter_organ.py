# organs/word_emitter_organ.py

from organs.base_packet_source import BasePacketSource

class WordEmitterOrgan(BasePacketSource):
    """
    Cathedral-era WordEmitterOrgan
    Wraps VocabularyOrgan and emits packet-based words
    for UniversalBusOrgan → SentenceBuilderOrgan.
    """

    def __init__(self, creature):
        super().__init__()  # REQUIRED for PacketBus/Bus auto-registration
        self.creature = creature
        self.vocab = creature.vocabulary

    # --------------------------------------------------------
    # BUS SINK INTERFACE (NO-OP)
    # --------------------------------------------------------
    def handle_bus_packet(self, packet):
        """
        WordEmitter is a source, not a global sink.
        We ignore incoming bus packets.
        """
        pass

    # --------------------------------------------------------
    # PACKET SOURCE INTERFACE
    # --------------------------------------------------------
    def get_packets(self):
        """
        Emit ONE word packet per heartbeat.
        Creature.heartbeat() will push this into UniversalBusOrgan.
        """
        word = self.vocab.get_word()
        return [{
            "type": "word",
            "value": word
        }]
