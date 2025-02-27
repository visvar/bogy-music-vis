import sys, os
import json
import librosa.display
import librosa.feature
import numpy as np
import pandas as pd


# Fallback WAV file (set your default file path here)
FALLBACK_WAV_FILE = os.path.join("audio", "pixlaxdax.wav")

def process_audio(file_path):
    """Load a WAV file and extract spectral features at 60 FPS."""

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Load audio file
    Fs = 22050  # Sampling rate
    x, Fs = librosa.load(file_path, sr=Fs)

    # Compute hop length for 60 FPS
    target_fps = 60
    H = int(Fs / target_fps)  # Hop length to achieve 60 values per second
    N = 1024  # FFT window size


    # Spectral centroid
    spec = librosa.feature.spectral_centroid(y=x, sr=Fs, n_fft=N, hop_length=H)[0]

    # RMS energy
    rms = librosa.feature.rms(y=x, hop_length=H)[0]

    num_frames = len(rms)  # Number of frames
    time_steps = np.arange(num_frames) / target_fps  # Time in seconds
    frames = np.arange(num_frames)


    # Extract features
    data = {
        "time": time_steps.tolist(),  # Column for time/frame number
        "frame": frames.tolist(),
        "energy":rms.tolist(),
        "brightness": spec.tolist(),
    }

    print(f"Processing file: 1/3")

     # 1️⃣ Extract Frequencies (Pitch Tracking)
    fmin = librosa.note_to_hz('C1')  # Lower bound (~32 Hz)
    fmax = librosa.note_to_hz('C8')  # Upper bound (~4186 Hz)
    frequencies = librosa.yin(x, fmin=fmin, fmax=fmax, sr=Fs, hop_length=H)

    # Add fundamental frequencies to data
    data["fundamental_frequencies"] = frequencies.tolist()

    # 2️⃣ Beat Tracking
    tempo, beat_frames = librosa.beat.beat_track(y=x, sr=Fs, hop_length=H)
    beat_times = librosa.frames_to_time(beat_frames, sr=Fs, hop_length=H)

    # Compute "time since last beat" and "time until next beat"
    time_since_last_beat = np.zeros(num_frames)
    time_until_next_beat = np.zeros(num_frames)

    print(time_since_last_beat, num_frames)

    for i in range(num_frames):

        past_beats = beat_frames[beat_frames <= i]
        future_beats = beat_frames[beat_frames > i]

        # Time since last beat
        if len(past_beats) > 0:
            time_since_last_beat[i] = i - past_beats[-1]
        else:
            time_since_last_beat[i] = 0 # No past beat yet

        # Time until next beat
        if len(future_beats) > 0:
            time_until_next_beat[i] = future_beats[0] - i
        else:
            time_until_next_beat[i] = 0  # No future beat left

    # Add beat features to data
    data["frames_since_last_beat"] = time_since_last_beat.tolist()
    data["frames_until_next_beat"] = time_until_next_beat.tolist()

    print(f"Processing file: 2/3")

    # Chroma Features (Captures harmonic structure)
    chroma = librosa.feature.chroma_stft(y=x, sr=Fs, n_fft=N, hop_length=H)
    chroma_labels = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    for i, label in enumerate(chroma_labels):
        data[f"chroma_{label}"] = chroma[i].tolist()

    # MFCCs (Captures timbre)
    mfcc = librosa.feature.mfcc(y=x, sr=Fs, n_mfcc=13, hop_length=H)
    for i in range(13):
        data[f"mfcc_{i}"] = mfcc[i].tolist()

    print(f"Processing file: 3/3")

    return data

def save_to_csv(data, output_file):
    """Save extracted audio features to a CSV file."""

    df = pd.DataFrame(data)
    try:
        df.to_csv(output_file, index=False)
        print(f"CSV output saved to: {output_file}")

    except Exception as e:
        print(f"Error writing CSV: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Get input WAV file or use fallback
    if len(sys.argv) > 1:
        wav_file = os.path.join("audio", sys.argv[1])  # Ensure file is in "audio" folder
    else:
        wav_file = FALLBACK_WAV_FILE  # Use fallback if no argument is given

    print(f"Processing file: {wav_file}")

    # Process audio and extract features
    data = process_audio(wav_file)

    # Output CSV file in the same "audio" directory
    output_file = wav_file.replace('.wav', '.csv')
    print(f"Write file: {output_file}")
    save_to_csv(data, output_file)

if __name__ == '__main__':
    main()
