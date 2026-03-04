from organs.reason_organ import ReasonOrgan
from organs.reason_autoscroll_viewer import ReasonAutoViewer

if __name__ == "__main__":
    reason_organ = ReasonOrgan()
    reason_organ.load_atlas("reason_atlas.txt")

    viewer = ReasonAutoViewer(reason_organ)
    viewer.run()
