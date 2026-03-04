import wave
import json
import os
from vosk import Model, KaldiRecognizer

MODEL_PATH = "models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"


def transcribe_audio(audio_path):
    """
    Transcribe WAV audio file using Vosk
    """

    if not os.path.exists(MODEL_PATH):
        raise Exception("Vosk model not found. Check models folder.")

    wf = wave.open(audio_path, "rb")

    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, wf.getframerate())

    transcript = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcript.append(result.get("text", ""))

    final_result = json.loads(rec.FinalResult())
    transcript.append(final_result.get("text", ""))

    full_text = " ".join(transcript)

    return full_text


def save_transcript(audio_path, text):
    """
    Save transcript next to audio file
    """

    txt_path = audio_path.replace(".wav", ".txt")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("Transcript saved:", txt_path)


if __name__ == "__main__":

    audio_file = "data/demo/sample_call_fixed.wav"

    text = transcribe_audio(audio_file)

    print("Transcription completed.")

    save_transcript(audio_file, text)