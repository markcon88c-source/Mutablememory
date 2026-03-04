from organs.reason_organ import ReasonOrgan
from organs.reason_viewer_organ import ReasonViewerOrgan

if __name__ == "__main__":
    reason_organ = ReasonOrgan()
    reason_organ.load_atlas("reason_atlas.txt")

    viewer = ReasonViewerOrgan(reason_organ)
    viewer.run()
