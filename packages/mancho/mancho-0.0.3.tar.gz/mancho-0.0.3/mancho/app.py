# SPDX-License-Identifier: GPL-3.0-only
import bisect
import os
import tempfile
import logging

import soundfile as sf
import audiofile as af
import pyaudio

from .audio import AudioPlayer
from .wave_display import AnimatedWaveDisplay

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject  # noqa


class App:

    def __init__(self):
        self.builder = Gtk.Builder()
        gladefile_path = os.path.join(os.path.dirname(__file__), "main.glade")
        self.builder.add_from_file(gladefile_path)
        self.builder.connect_signals(self)
        main_window = self.builder.get_object("main_window")
        main_box = self.builder.get_object("main_box")
        self.wave_display = AnimatedWaveDisplay()
        self.wave_display.connect("selection-updated",
                                  self.on_selection_updated)
        main_box.pack_start(self.wave_display, True, True, 0)
        main_window.show_all()

        self.file_dialog = self.builder.get_object("open_dialog")
        self.file_dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        self.preferences_window = self.builder.get_object("preferences_window")

        self.selected_sound_device = 0
        self.audio_player = AudioPlayer(self.selected_sound_device)
        self.selected_range = None
        self.cursor_location = 0
        self.time_markers = [0]

        GObject.timeout_add(50, self.on_update_loop)

    def on_update_loop(self, *args):
        if self.audio_player.is_playing:
            self.cursor_location = self.audio_player.playback_time
            self.wave_display.set_playhead(self.cursor_location)
        return True

    def on_quit(self, *args):
        self.audio_player.stop()
        Gtk.main_quit()

    def on_selection_updated(self, wave_display, selection0, selection1):
        if selection0 == selection1:
            self.selected_range = None
        else:
            self.selected_range = (selection0, selection1)
        self.audio_player.stop()
        return True

    def on_open(self, *args):
        response = self.file_dialog.run()
        if response == Gtk.ResponseType.OK:
            path = self.file_dialog.get_filename()
            self.load_file(path)
            self.wave_display.update_data(self.data, self.sampling_rate)
            # TODO remove magic numbers [0-10]
            self.selected_range = None
            self.wave_display.set_display_range([0, 10])
            self.wave_display.set_selection(None)
            self.time_markers = [0]
            self.audio_player.stop()
        self.file_dialog.hide()

    def on_preferences(self, *args):
        devices_combobox = self.builder.get_object("devices_combobox")
        devices_combobox.remove_all()
        pyaudio_obj = pyaudio.PyAudio()
        for i in range(pyaudio_obj.get_device_count()):
            devices_combobox.append_text(pyaudio_obj.get_device_info_by_index(i)["name"])
        devices_combobox.set_active(self.selected_sound_device)
        self.preferences_window.show()

    def on_preferences_window_delete_event(self, *args):
        self.preferences_window.hide()
        return True

    def on_preferences_ok(self, *args):
        self.selected_device = self.builder.get_object("devices_combobox").get_active()
        self.audio_player.device_id = self.selected_device
        self.preferences_window.hide()

    def on_main_window_key_press_event(self, window, event):
        def zoom(zoom_factor):
            zoom_diff = (self.wave_display.display_range[1] -
                         self.wave_display.display_range[0])*zoom_factor

            self.wave_display.set_display_range(
                [self.wave_display.display_range[0] + zoom_diff,
                 self.wave_display.display_range[1] - zoom_diff]
            )

        def set_marker():
            if self.audio_player.is_playing:
                marker_location = self.audio_player.playback_time
            else:
                marker_location = self.cursor_location
            if marker_location not in self.time_markers:
                bisect.insort(self.time_markers, marker_location)
            self.wave_display.set_marker_locations(self.time_markers)

        def remove_marker(to_right):
            if to_right:
                to_delete = bisect.bisect_left(self.time_markers,
                                               self.cursor_location)
            else:
                to_delete = bisect.bisect(self.time_markers,
                                          self.cursor_location)-1
            if (0 <= to_delete < len(self.time_markers)
                    and self.time_markers[to_delete] != 0):
                del self.time_markers[to_delete]
                self.wave_display.set_marker_locations(self.time_markers)

        def select_between_markers():
            i = bisect.bisect_left(self.time_markers, self.cursor_location)
            if i >= len(self.time_markers) or i < 1:
                return
            self.selected_range = [self.time_markers[i-1], self.time_markers[i]]
            self.wave_display.set_selection(self.selected_range)

        def modify_selection(extend=True, to_right=True):
            if self.selected_range is None:
                return
            side_to_modify = 1 if to_right else 0
            i = (bisect.bisect_left(self.time_markers,
                                    self.selected_range[side_to_modify]) +
                 (1 if extend == to_right else -1))
            if i < 0 or i >= len(self.time_markers):
                return
            self.selected_range[side_to_modify] = self.time_markers[i]
            if self.selected_range[0] == self.selected_range[1]:
                self.selected_range = None
            self.wave_display.set_selection(self.selected_range)

        print(event.keyval)
        if event.keyval == 65363:  # Right arrow
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                modify_selection(extend=True, to_right=True)
            elif event.state & Gdk.ModifierType.MOD1_MASK:
                modify_selection(extend=False, to_right=False)
            elif event.state & Gdk.ModifierType.CONTROL_MASK:
                # Move right by extending to right and shortening from left
                modify_selection(extend=True, to_right=True)
                modify_selection(extend=False, to_right=False)
            else:
                self.cursor_location += 0.1
                self.wave_display.set_playhead(self.cursor_location)
        elif event.keyval == 65361:  # Left arrow
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                modify_selection(extend=True, to_right=False)
            elif event.state & Gdk.ModifierType.MOD1_MASK:
                modify_selection(extend=False, to_right=True)
            elif event.state & Gdk.ModifierType.CONTROL_MASK:
                # Move left by extending to left and shortening from right
                modify_selection(extend=True, to_right=False)
                modify_selection(extend=False, to_right=True)
            else:
                self.cursor_location -= 0.1
                self.wave_display.set_playhead(self.cursor_location)
        elif event.keyval == 65362:  # Up arrow
            zoom(0.1)
        elif event.keyval == 65364:  # Down arrow
            zoom(-0.1)
        elif event.keyval == 97:  # a
            set_marker()
        elif event.keyval == 115:
            select_between_markers()
        elif event.keyval == 65535:  # del
            remove_marker(to_right=True)
        elif event.keyval == 65288:  # backspace
            remove_marker(to_right=False)
        elif event.keyval == 65307:  # Esc
            self.selected_range = None
            self.wave_display.set_selection(None)
        elif event.keyval == 32:  # Spacebar
            self.on_play_pause_clicked()
        else:
            return False
        return True

    def on_play_pause_clicked(self, *args):
        print("SR:", self.selected_range)
        if self.audio_player.is_playing:
            logging.debug("Stopping audio player")
            self.audio_player.stop()
            logging.debug("Audio player stopped")
        else:
            logging.debug("Stating audio player")
            speed = self.builder.get_object("speed_scale").get_value() / 100
            if self.selected_range:
                start = self.selected_range[0]
                end = self.selected_range[1]
            else:
                start = self.cursor_location
                end = len(self.data)/self.sampling_rate
            self.audio_player.play(self.data, start, end,
                                   self.sampling_rate, playback_speed=speed)

    def load_file(self, path):
        filename, extension = os.path.splitext(path)
        if extension != ".wav":
            with tempfile.TemporaryDirectory() as temp_dirpath:
                target_path = os.path.join(temp_dirpath, filename+".wav")
                af.convert_to_wav(path, target_path)
                self.data, self.sampling_rate = sf.read(target_path)
        else:
            self.data, self.sampling_rate = sf.read(path)

    def run(self):
        Gtk.main()
