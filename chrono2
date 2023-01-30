import pyxel

class Chronometer:
    def __init__(self):
        self.time = 0
        self.running = False

    def start(self):
        self.time = 0
        self.running = True

    def stop(self):
        self.running = False

    def update(self):
        if self.running:
            self.time += 1

    def draw(self):
        minutes, seconds = divmod(self.time, 60)
        pyxel.text(5, 5, f"{minutes:02}:{seconds:02}", 7)

# Initialise Pyxel
pyxel.init(160, 120)

# Create an instance of the chronometer
chronometer = Chronometer()

# Start the chronometer
chronometer.start()

# Update function for Pyxel
def update():
    chronometer.update()

# Draw function for Pyxel
def draw():
    pyxel.cls(0)
    chronometer.draw()

# Run Pyxel
pyxel.run(update, draw)
