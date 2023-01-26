from youtube_gui import QApplication, YouTubeSubscriberCounter
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = YouTubeSubscriberCounter(sys.argv)
    gui.show()
    sys.exit(app.exec_())
