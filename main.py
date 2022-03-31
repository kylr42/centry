import os

from centry import Centrifuge


def main():
    centri = Centrifuge("127.0.0.1", "8000")
    centri.connect(os.getenv("CENTRI_TOKEN"))
    centri.subscribe("channel1")
    centri.loop()


if __name__ == '__main__':
    main()
