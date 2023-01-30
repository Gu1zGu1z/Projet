import pyxel

class Score:
    def __init__(self):
        self.time = 0
        self.running = False

    def start(self):
        self.time = 0
        self.running = True

    def switch(self):
        self.running = not self.running
        
    def stop(self):
        self.running = False

    def update(self):
        if pyxel.btnr(pyxel.KEY_A):
            self.switch()
        if self.running:
            self.time += 1

    def draw(self):
        seconds = self.time//60
        pyxel.text(135, 5,f"{seconds:05}", 7)

class Jeu():
    def __init__(self):
# Initialise Pyxel
        pyxel.init(160, 120)

# Create an instance of the chronometer
        self.score = Score()

# Start the chronometer
        self.score.start()
        pyxel.run(self.update, self.draw)


# Update function for Pyxel
    def update(self):
        self.score.update()
        

# Draw function for Pyxel
    def draw(self):
        pyxel.cls(0)
        self.score.draw()

# Run Pyxel
Jeu()
