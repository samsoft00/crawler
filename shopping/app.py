from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor
from arachne import Arachne

app = Arachne(__name__)

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(8888, site)


@app.route('/')
def index():
	return 'Hey'


if __name__ == '__main__':
	reactor.run()