import numpy as np
import matplotlib.pyplot as plt
from julia import juliaset


def iter_function(c, max_iter):
    n = 1
    z = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n


def mandelbrot_set(zoom: float, pos: tuple, img_size: tuple, max_iter: int):

    # img resolution
    WIDTH, HEIGHT = img_size
    ratio = HEIGHT / WIDTH

    # Plot window
    X, Y = pos
    ZOOM = zoom

    RE_START = X - 2 / 2 ** ZOOM
    RE_END = X + 2 / 2 ** ZOOM
    IM_START = Y + 2 * ratio / 2 ** ZOOM
    IM_END = Y - 2 * ratio / 2 ** ZOOM

    mandelset = np.zeros((HEIGHT, WIDTH))
    for x in range(WIDTH):
        for y in range(HEIGHT):

            z = complex(
                RE_START + (x / WIDTH) * (RE_END - RE_START),
                IM_START + (y / HEIGHT) * (IM_END - IM_START),
            )

            iter_reached = iter_function(z, max_iter)

            mandelset[y, x] = iter_reached / max_iter

    return mandelset


def onclick(event):
    jx, jy = event.xdata, event.ydata
    # m_fig.canvas.mpl_disconnect(cid)  # stop after 1 click
    # plt.close()  # close mandelbrot fig

    img_size = (500, 500)
    c = complex(-1.5 + jx / m_img_size[0] * 3, -1.5 + jy / m_img_size[1] * 3)
    zoom = 0
    pos = (0, 0)
    max_abs = 10
    max_iter = 200
    juliaset(c, zoom, pos, img_size, max_abs, max_iter)


if __name__ == "__main__":
    # mandelbrot mapper settings
    m_img_size = (1000, 900)
    m_zoom = -0.1
    m_pos = (0, 0)
    m_max_iter = 100

    m_plot_data = mandelbrot_set(m_zoom, m_pos, m_img_size, m_max_iter)

    m_fig = plt.figure()
    ax = m_fig.add_subplot(111)
    ax.imshow(m_plot_data, plt.cm.hot)

    cid = m_fig.canvas.mpl_connect("button_press_event", onclick)

    plt.show()
