"""
Sound effects for DSA Visualizer using pygame
"""
import pygame
import numpy as np


def create_pop_sound():
    """
    Create a pop sound effect using pygame mixer
    
    Returns:
        pygame.mixer.Sound object
    """
    pygame.mixer.init()
    freq = 600
    duration = 0.1
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.02)
    wave = (wave * 32767).astype(np.int16)
    return pygame.mixer.Sound(buffer=wave.tobytes())
