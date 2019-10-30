import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
a = np.random.random((16, 16))
im = plt.imshow(a, cmap='hot', interpolation='nearest')

#arr = im.get_array()
#print(arr)

def init():
    a = np.random.random((16, 16))
    im.set_data(a)
    return [im]

def animate(i):
    a = np.random.random((16, 16))
    im.set_array(a)
    return [im]

anim = animation.FuncAnimation(fig, animate, frames=5, interval=500, blit=True, repeat=False)

#plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
#FFwriter = animation.FFMpegWriter()
#anim.save('basic_animation.mp4', writer = FFwriter)
#anim.save('WorkABc', writer="pillow")
plt.show()

