from axiom import store
from merlyn import exercise
from twisted.application import service
from twisted import plugin
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.internet.ssl import PrivateCertificate
from twisted.protocols.amp import AMP
from twisted.python import usage
from zope import interface


class AMP(AMP, exercise.Locator):
    """
    The merlyn AMP protocol.
    """
    @property
    def store(self):
        return self.factory.store



class Options(usage.Options):
    """
    The options for starting a service.
    """
    optParameters = [
        ["store", "s", None, "Path to root store (mandatory)", store.Store]
    ]

    def postOptions(self):
        """Verify that a store was passed.

        """
        if self["store"] is None:
            raise usage.UsageError("Passing a root store is mandatory.")



class Service(service.Service):
    def __init__(self, store):
        self.store = store


    def startService(self):
        with open("cert.pem") as certFile, open("key.pem") as keyFile:
            pemData = keyFile.read() + certFile.read()
        cert = PrivateCertificate.loadPEM(pemData)
        factory = ServerFactory.forProtocol(AMP)
        factory.store = self.store
        reactor.listenSSL(4430, factory, cert.options())



@interface.implementer(plugin.IPlugin, service.IServiceMaker)
class ServiceMaker(object):
    """
    Makes a merlyn service from the command line.
    """
    tapname = "merlyn"
    description = "Exercise server"
    options = Options

    def makeService(self, options):
        return Service(options["store"])