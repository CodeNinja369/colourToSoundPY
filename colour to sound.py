import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
import pyaudio
import numpy as np
import pygame

def generate_tone(frequency, duration, sample_rate=44100):
    # Calculate the number of frames
    num_frames = int(duration * sample_rate)

    # Generate the time values
    t = np.linspace(0, duration, num_frames, endpoint=False)

    # Generate the waveform for the given frequency
    waveform = np.sin(2 * np.pi * frequency * t)

    # Convert the waveform to the appropriate format for PyAudio
    waveform = (waveform * 32767).astype(np.int16)

    return waveform

def play_multiple_tones(frequencies, duration, sample_rate=44100):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Generate and sum up the waveforms for each frequency
    waveforms = [generate_tone(frequency, duration, sample_rate) for frequency in frequencies]
    mixed_waveform = np.sum(waveforms, axis=0)

    # Play the mixed waveform
    stream.write(mixed_waveform)

    # Close the stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def red(x):
    return (1550 / 255 * x) + 50

def green(x):
    return (1535 / 1700 * (x - 1600)) + 50

def blue(x):
    return (1698 / 1700 * (x - 3300)) + 50


def rgbToFrequency(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    return [red(r), green(g), blue(b)]

    
duration = 3

pygame.init()
width = 500
height = 500
disp = pygame.display.set_mode((width, width), pygame.RESIZABLE)
pygame.display.set_caption("Colour to Sound")

rslider = Slider(disp, 100, 100, 800, 40, min=0, max=255, step=1)
gslider = Slider(disp, 200, 200, 800, 40, min=0, max=255, step=1)
bslider = Slider(disp, 300, 300, 800, 40, min=0, max=255, step=1)

colour = (0,0,0)

def playsound():
    
    frequencies = rgbToFrequency(colour)
    play_multiple_tones(frequencies, duration)

button = Button(
    # Mandatory Parameters
    disp,  # Surface to place button on
    500,  # X-coordinate of top left corner
    500,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    text="play",
    onClick=lambda: playsound()
)



running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    r = rslider.getValue()
    g = gslider.getValue()
    b = bslider.getValue()

    colour = (r,g,b)
    

    disp.fill(colour)
    pygame_widgets.update(events)
    pygame.display.update()
    
pygame.quit()
