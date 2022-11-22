from robots.demo.demo_wheeledbase import *
from robots.bornibus.setup_bornibus import *

controller_keys.update({
    K_x: {KEYDOWN: lambda: None,    KEYUP: lambda: None},
    K_a: {KEYDOWN: lambda: None,    KEYUP: lambda: None},
    K_b: {KEYDOWN: lambda: None,    KEYUP: lambda: None},
})

X_jb = 2
A_jb = 0
B_jb = 1
controller_joybuttons.update({
    X_jb: {JOYBUTTONDOWN: lambda: None,    JOYBUTTONUP: lambda: None},
    A_jb: {JOYBUTTONDOWN: lambda: None,    JOYBUTTONUP: lambda: None},
    B_jb: {JOYBUTTONDOWN: lambda: None,    JOYBUTTONUP: lambda: None},
})


text = """
Demo Bornibus

"""
update_text(text)
controlEvent()
stop()
pygame.quit()
