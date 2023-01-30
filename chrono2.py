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
        minutes, seconds = self.time//60, self.time%60
        pyxel.text(135, 5, f"{minutes:02}{seconds:02}", 7)

class Jeu():
    def __init__(self):
# Initialise Pyxel
    pyxel.init(160, 120)

# Create an instance of the chronometer
    self.chronometer = Chronometer()

# Start the chronometer
    self.chronometer.start()
    pyxel.run(self.update, self.draw)


# Update function for Pyxel
    def update(self):
        chronometer.update()

# Draw function for Pyxel
    def draw(self):
        pyxel.cls(0)
        self.chronometer.draw()

# Run Pyxel
Jeu()
