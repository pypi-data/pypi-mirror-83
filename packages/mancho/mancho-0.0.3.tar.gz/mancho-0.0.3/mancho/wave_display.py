# SPDX-License-Identifier: GPL-3.0-only

"""Widget for interacting with waveforms."""
import bisect

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np

from gi.repository import Gtk, GObject


class AnimatedWaveDisplay(Gtk.Box):
    __gsignals__ = {
        'selection-updated': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                              (GObject.TYPE_FLOAT, GObject.TYPE_FLOAT))
    }

    def __init__(self):
        super().__init__()
        self.data = []
        self.timestamps = []
        self.display_range = [0, 10]
        self.selection = None
        self.playhead_location = 0
        self.marker_locations = []

        self.fig = Figure()
        self.fig.subplots_adjust(wspace=0, hspace=0)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_facecolor("#F6F6F6")
        self.fig.tight_layout()
        self.canvas = FigureCanvas(self.fig)

        self.pack_start(self.canvas, True, True, 0)
        self.canvas.mpl_connect('button_press_event',
                                self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event',
                                self.on_mouse_movement)
        self.canvas.mpl_connect('button_release_event',
                                self.on_mouse_release)
        self.canvas.mpl_connect('draw_event', self.on_draw)

    def update_data(self, data, sampling_rate):
        # Convert data to mono if streo, no reason to display stereo
        if not(len(data.shape) == 1 or data.shape[1] == 1):
            data = data.T[0]
        self.data = data / data.max()
        # Timestamps are required to work with time data instead of sample nos.
        self.timestamps = [i/sampling_rate for i in range(len(data))]
        self.update_figure(redraw_data=True)

    def on_draw(self, *args):
        self.background = self.fig.canvas.copy_from_bbox(
            self.ax.get_figure().bbox)
        self.plot, = self.ax.plot([], [], "g", animated=True)
        self.playhead = self.ax.axvline(self.playhead_location,
                                        color="black", animated=True)

        self.data_should_redraw = True
        self.update_figure(redraw_data=True)
        return False

    def update_figure(self, redraw_data=False):
        if redraw_data:
            self.fig.canvas.restore_region(self.background)
            start_index = bisect.bisect(self.timestamps, self.display_range[0])
            end_index = bisect.bisect(self.timestamps, self.display_range[1])
            # Show no more than 10_000 samples, for speedup
            step = max(1, (end_index-start_index) // 10_000)
            self.plot.set_data(self.timestamps[start_index:end_index:step],
                               self.data[start_index:end_index:step])
            #self.ax.set_xticks(np.arange(0, 100, 0.25))
            self.ax.set_xlim(self.display_range)

            # self.ax.set_yticks([0])
            self.ax.set_ylim([-1, 1])
            self.ax.grid()
            self.ax.set_xticks([])
            self.ax.set_yticks = ([])

            self.ax.draw_artist(self.plot)
            self.plot_cache = self.fig.canvas.copy_from_bbox(
                self.ax.get_figure().bbox)

        if not redraw_data:
            self.fig.canvas.restore_region(self.plot_cache)
        if self.selection and self.selection[0] != self.selection[1]:
            selection_axvspan = self.ax.axvspan(*self.selection,
                                                color='red',
                                                alpha=0.5,
                                                animated=True)
            self.ax.draw_artist(selection_axvspan)
        self.playhead.set_xdata(self.playhead_location)
        self.ax.draw_artist(self.playhead)
        for loc in self.marker_locations:
            marker = self.ax.axvline(loc, color="gray", animated=True)
            self.ax.draw_artist(marker)

        self.fig.canvas.blit(self.fig.bbox)

    def set_playhead(self, location):
        data_should_redraw = False
        self.playhead_location = location
        display_width = self.display_range[1] - self.display_range[0]
        if location < self.display_range[0]:
            self.display_range = [i-display_width/2 for i in self.display_range]
            data_should_redraw = True
        elif location > self.display_range[1]:
            self.display_range = [i+display_width/2 for i in self.display_range]
            data_should_redraw = True
        self.update_figure(data_should_redraw)

    def set_marker_locations(self, locations):
        self.marker_locations = locations
        self.update_figure()

    def set_display_range(self, display_range):
        self.display_range = display_range
        self.update_figure(redraw_data=True)

    def set_selection(self, selection):
        self.selection = selection
        self.update_figure()

    def on_mouse_press(self, event):
        self.set_selection([event.xdata, event.xdata])

    def on_mouse_movement(self, event):
        if event.button and event.button == event.button.LEFT:
            self.set_selection([self.selection[0], event.xdata])

    def on_mouse_release(self, event):
        self.selection.sort()
        self.emit("selection-updated", *self.selection)
