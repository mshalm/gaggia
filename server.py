from flask import Flask
import threading
import time

PORT = 5000

class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #self.srv = make_server('127.0.0.1', 5000, app)
        #self.ctx = app.app_context()
        #self.ctx.push()
        self.state_lock = threading.Lock()
        self.power = True
        self.setDaemon(True)
        self.start()

    def run(self):
        app = Flask(__name__)
        @app.route("/on")
        def on():
            with self.state_lock:
                self.power = True
            return "Turned On!"

        @app.route("/off")
        def off():
            with self.state_lock:
                self.power = False
            return "Turned Off!"
        
        app.run(host='0.0.0.0', port=PORT)

    def is_powered(self):
        power = False
        with self.state_lock:
            power = self.power
        return power

    def shutdown(self):
        pass

if __name__ == "__main__":
    serv = Server()
    for i in range(30):
        print(serv.is_powered())
        time.sleep(1)

