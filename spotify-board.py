#!/usr/bin/python

sys.path.insert(1, 'rpi-rgb-led-matrix/bindings/python')

from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

NAMED_PIPE = "/var/run/spotify-board"
SPOTIFY_CACHE = "/var/cache/raspotify/.access_token"

def spotify_track_info(track_id):
    cache_file_handler = CacheFileHandler(cache_path=SPOTIFY_CACHE)
    client_credentials_manager = SpotifyClientCredentials(cache_handler=cache_file_handler)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    track = sp.track(track_id)
    return track['name'] + " • " + track['artists'][0]['name']

while True:
    with open(NAMED_PIPE) as pipe:
        input = pipe.readline().rstrip().split()

        if(len(input) == 2 and input[0] == 'playing' and input[1] is not None):
            # Configuration for the matrix
            options = RGBMatrixOptions()
            options.rows = 32
            options.cols = 64
            options.brightness = 50
            options.chain_length = 1
            options.parallel = 1
            options.hardware_mapping = 'adafruit-hat-pwm'

            matrix = RGBMatrix(options = options)

            # Make image fit our screen.
            offscreen_canvas = matrix.CreateFrameCanvas()
            font = graphics.Font()
            font.LoadFont("comic-sans-20.bdf")
            textColor = graphics.Color(255, 255, 255)
            pos = offscreen_canvas.width

            while True:
                offscreen_canvas.Clear()
                len = graphics.DrawText(offscreen_canvas, font, pos, 25, textColor, spotify_track_info(input[1]))
                pos -= 1
                if (pos + len < 0):
                    pos = offscreen_canvas.width

                time.sleep(0.02)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
