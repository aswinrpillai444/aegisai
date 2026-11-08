import wave
import math
import struct
import os

sample_rate = 44100
amp = 28000  # High volume for emergency

def apply_envelope(samples, attack_ms=10, release_ms=10):
    attack_samples = int(sample_rate * (attack_ms / 1000.0))
    release_samples = int(sample_rate * (release_ms / 1000.0))
    total_samples = len(samples)
    for i in range(min(attack_samples, total_samples)):
        samples[i] = samples[i] * (i / attack_samples)
    for i in range(min(release_samples, total_samples)):
        idx = total_samples - 1 - i
        samples[idx] = samples[idx] * (i / release_samples)
    return samples

def make_beep(freq, dur_ms):
    samples = []
    n = int(sample_rate * dur_ms / 1000.0)
    for i in range(n):
        t = i / sample_rate
        s = math.sin(2.0 * math.pi * freq * t)
        samples.append(s * amp)
    return apply_envelope(samples)

def make_siren(f_low, f_high, dur_ms):
    samples = []
    n = int(sample_rate * dur_ms / 1000.0)
    for i in range(n):
        t = i / sample_rate
        # Rising/falling LFO (2 Hz)
        lfo = (math.sin(2.0 * math.pi * 1.5 * t - math.pi/2) + 1.0) / 2.0
        freq = f_low + (f_high - f_low) * lfo
        s = math.sin(2.0 * math.pi * freq * t)
        samples.append(s * amp)
    return apply_envelope(samples, attack_ms=50, release_ms=100)

def make_silence(dur_ms):
    return [0.0] * int(sample_rate * dur_ms / 1000.0)

audio = []

# Pattern: 3 short high-pitched beeps, followed by long rising-falling siren.
# Repeat 2 times. Total duration ~ 6.3 seconds.
for _ in range(2):
    for _ in range(3):
        audio.extend(make_beep(1250, 150)) # Sharp beep
        audio.extend(make_silence(150))

    audio.extend(make_siren(600, 1300, 2000)) # Long siren
    audio.extend(make_silence(400))

os.makedirs('assets/audio', exist_ok=True)
wav_path = 'assets/audio/emergency_alert.wav'

with wave.open(wav_path, 'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sample_rate)
    for s in audio:
        w.writeframes(struct.pack('<h', int(s)))

print(f'Generated emergency alert at: {wav_path}')
