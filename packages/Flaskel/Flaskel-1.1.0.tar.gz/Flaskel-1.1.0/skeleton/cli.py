from flaskel import Server

from blueprints import BLUEPRINTS
from ext import EXTENSIONS


if __name__ == '__main__':
    server = Server(blueprints=BLUEPRINTS, extensions=EXTENSIONS)
    server.run()
