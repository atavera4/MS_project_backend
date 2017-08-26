import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
import socket
import cv2
import numpy
import base64
import time
import thread

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


# capture = cv2.VideoCapture(0);
# time.sleep(0.25); # warm up camera
# ret, frame = capture.read();
# cnt = cv2.imencode('.png',frame)[1]
# b64 = base64.encodestring(cnt)
# img = b64;

class image:
    def __init__(self):
        self.img = "testing  ";
        return;
Image = image();

class SomeServerProtocol(WebSocketServerProtocol):
    # def onConnect(self, request):
    #     print("some request connected {}".format(request))

    def onOpen(self):
        self.sendMessage("ariel");

    def onMessage(self, payload, isBinary):
        #self.sendMessage("message received")
        #self.sendMessage(payload)
        #print(image.img);
        self.sendMessage(image.img);
        # img = "here"
        # print(img)


def GetVideo():
    capture = cv2.VideoCapture(0);
    time.sleep(0.25); # warm up camera
    ret, frame = capture.read();
    while True:
        time.sleep(.05);
        ret, frame = capture.read();
        # img_str = cv2.imencode('.jpg', frame).tostring()
        cnt = cv2.imencode('.png',frame)[1]
        b64 = base64.encodestring(cnt)
        image.img = b64;
        # print(img)
        #time.sleep(10);

        # html = "<html><img src='data:image/png;base64,"+b64 +"'></html"
        # send(html)


if __name__ == "__main__":
    

    thread.start_new_thread(GetVideo, ( ));

    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File(".")

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()
