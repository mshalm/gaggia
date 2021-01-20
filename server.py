from flask import Flask
import threading
import time

PORT = 5000

TIMEOUT_TIME = 2.0 * 60.0 * 60.0 # [s]

class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #self.srv = make_server('127.0.0.1', 5000, app)
        #self.ctx = app.app_context()
        #self.ctx.push()
        self.state_lock = threading.Lock()
        self.on_time = time.time()
        self.power = True
        self.setDaemon(True)
        self.start()

    def run(self):
        app = Flask(__name__)
        @app.route("/on")
        def on():
            with self.state_lock:
                self.power = True
                self.on_time = time.time()
            return "Turned On!"

        @app.route("/off")
        def off():
            with self.state_lock:
                self.power = False
            return "Turned Off!"
        
        app.run(host='0.0.0.0', port=PORT)

    def is_powered(self):
        stale = False
        power = False
        with self.state_lock:
            power = self.power
            stale = time.time() - self.on_time > TIMEOUT_TIME
        return power and (not stale)

    def shutdown(self):
        pass

if __name__ == "__main__":
    serv = Server()
    for i in range(30):
        print(serv.is_powered())
        time.sleep(1)

