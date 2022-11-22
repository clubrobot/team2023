from robots.demo.demo_wheeledbase import *
from robots.R128.setup_128 import *

controller_keys.update({
    K_x: {KEYDOWN: lambda: None,    KEYUP: lambda: None},
})

X_jb = 2
controller_joybuttons.update({
    X_jb: {JOYBUTTONDOWN: lambda: None,    JOYBUTTONUP: lambda: None},
})


text = """
Demo 128
"""
update_text(text)
controlEvent()
stop()
pygame.quit()
