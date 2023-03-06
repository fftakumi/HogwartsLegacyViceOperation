import time
import speech_recognition
import pyaudio
import pyautogui
import re

SAMPLERATE = 44100
audio_length = 4
audio_bytes = []

magic_setting = {"プロテゴ": 1,
                 "インセンティオ": 2}


def callback(in_data, frame_count, time_info, status):
    global sprec
    audio_bytes.append(in_data)
    if len(audio_bytes) >= audio_length:
        audio_bytes.pop(0)

    now_length = len(audio_bytes)
    for i in range(now_length-1):
        audio_bytes[i] += audio_bytes[now_length-1]
    try:
        audiodata = speech_recognition.AudioData(audio_bytes[0], SAMPLERATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='ja-JP')
        if "プロテゴ" in sprec_text:
            pyautogui.press("q")

    except speech_recognition.UnknownValueError:
        pass
    except speech_recognition.RequestError as e:
        pass
    finally:
        return (None, pyaudio.paContinue)


def main():
    global sprec
    sprec = speech_recognition.Recognizer()  # インスタンスを生成
    # Audio インスタンス取得
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        rate=SAMPLERATE,
                        channels=1,
                        input_device_index=1,
                        input=True,
                        frames_per_buffer=SAMPLERATE * 1,  # 2秒周期でコールバック
                        stream_callback=callback)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == '__main__':
    main()