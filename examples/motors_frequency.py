"""
This example demonstrates how to play a simple song using the Modulino motors in DC mode, 
by varying the frequency of the motor's PWM signal to produce different musical notes.
The decay mode is set to fast for more responsive frequency changes.

Initial author: Sebastian Romero (s.romero@arduino.cc)
"""

from modulino import ModulinoMotors, DecayMode
from time import sleep_ms

def play_song(motors: ModulinoMotors, song: list, tempo: int):
  """
  Plays a song using the Modulino motors by setting the frequency of the PWM signal.
  Each note in the song is represented as a tuple of (note, duration), 
  where 'note' is a string representing the note name and 'duration' is the length of the note in beats.

  Parameters:
  - motors: An instance of ModulinoMotors.
  - song: A list of tuples, where each tuple contains a note (as a string representing the note name) and its duration (in beats).
  - tempo: The duration of a single beat in milliseconds.
  """
  # Note frequencies in Hz (names based on scientific pitch notation)
  frequencies = {
      'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392,
      'G#4': 415, 'A4': 440, 'A#4': 466, 'B4': 494,
      'C5': 523, 'D5': 587, 'D#5': 622, 'E5': 659, 'F5': 698,
      'F#5': 740, 'G5': 784, 'A5': 880, 'C6': 1047,
      'REST': 0
  }

  for note, beat in song:
    duration = beat * tempo
    if note == 'REST':
      motors.speed_a = 0
      motors.speed_b = 0
      sleep_ms(duration)
    else:
      if note in frequencies:
        motors.speed_a = base_speed
        motors.speed_b = base_speed
        motors.frequency = frequencies[note]
      sleep_ms(duration)
    sleep_ms(tempo // 10) # Short pause between notes for audibility

motors = ModulinoMotors()
motors.stepper_mode_enabled = False  # DC mode
motors.set_decay(DecayMode.FAST)

# Song represented as list of (Note, Duration) tuples
song = [
    ('E5', 1),
    ('E5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('C5', 1),
    ('E5', 1),
    ('REST', 1),
    ('G5', 2),
    ('REST', 2),
    ('G4', 2),
    ('REST', 2),
    ('C5', 2),
    ('REST', 1),
    ('G4', 1),
    ('REST', 2),
    ('E4', 2),
    ('REST', 1),
    ('A4', 1),
    ('REST', 1),
    ('B4', 1),
    ('REST', 1),
    ('A#4', 1),
    ('A4', 2),
    ('G4', 1),
    ('E5', 1),
    ('G5', 1),
    ('REST', 1),
    ('A5', 2),
    ('F5', 1),
    ('G5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('C5', 1),
    ('D5', 1),
    ('B4', 1),
    ('REST', 2),
    ('C5', 2),
    ('REST', 1),
    ('G4', 1),
    ('REST', 2),
    ('E4', 2),
    ('REST', 1),
    ('A4', 1),
    ('REST', 1),
    ('B4', 1),
    ('REST', 1),
    ('A#4', 1),
    ('A4', 2),
    ('G4', 1),
    ('E5', 1),
    ('G5', 1),
    ('REST', 1),
    ('A5', 2),
    ('F5', 1),
    ('G5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('C5', 1),
    ('D5', 1),
    ('B4', 1),
    ('REST', 2),
    ('REST', 2),
    ('G5', 1),
    ('F#5', 1),
    ('F5', 1),
    ('D#5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('G#4', 1),
    ('A4', 1),
    ('C5', 1),
    ('REST', 1),
    ('A4', 1),
    ('C5', 1),
    ('D5', 1),
    ('REST', 2),
    ('G5', 1),
    ('F#5', 1),
    ('F5', 1),
    ('D#5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('C6', 1),
    ('REST', 1),
    ('C6', 1),
    ('C6', 2),
    ('REST', 2),
    ('REST', 2),
    ('G5', 1),
    ('F#5', 1),
    ('F5', 1),
    ('D#5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('G#4', 1),
    ('A4', 1),
    ('C5', 1),
    ('REST', 1),
    ('A4', 1),
    ('C5', 1),
    ('D5', 1),
    ('REST', 2),
    ('D#5', 2),
    ('REST', 1),
    ('D5', 1),
    ('REST', 2),
    ('C5', 2),
    ('REST', 6),
    ('REST', 2),
    ('G5', 1),
    ('F#5', 1),
    ('F5', 1),
    ('D#5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('G#4', 1),
    ('A4', 1),
    ('C5', 1),
    ('REST', 1),
    ('A4', 1),
    ('C5', 1),
    ('D5', 1),
    ('REST', 2),
    ('G5', 1),
    ('F#5', 1),
    ('F5', 1),
    ('D#5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('C6', 1),
    ('REST', 1),
    ('C6', 1),
    ('C6', 2),
    ('REST', 2),
    ('REST', 2),
    ('G5', 1),
    ('F#5', 1),
    ('F5', 1),
    ('D#5', 1),
    ('REST', 1),
    ('E5', 1),
    ('REST', 1),
    ('G#4', 1),
    ('A4', 1),
    ('C5', 1),
    ('REST', 1),
    ('A4', 1),
    ('C5', 1),
    ('D5', 1),
    ('REST', 2),
    ('D#5', 2),
    ('REST', 1),
    ('D5', 1),
    ('REST', 2),
    ('C5', 2),
    ('REST', 6),
]

base_speed = 30 # Motor speed (0-100) for playing notes
tempo = 135  # ms per beat
play_song(motors, song, tempo)
motors.speed_a = 0
motors.speed_b = 0