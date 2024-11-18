# %%
import numpy as np
import inharmonicon.inharmonicon as ih

h = ih.Harmonics(400, fmin=8)
s = ih.Sound(f = h, length=.07)
s.play()
# %%
