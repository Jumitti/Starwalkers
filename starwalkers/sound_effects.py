import base64
import random
import os
import streamlit as st


def shuttles():
    audio_files = [os.path.join('./sounds/effect/shuttles/', f) for f in os.listdir('./sounds/effect/shuttles/') if
                   f.endswith('.mp3')]
    effect(audio_files)


def battle():
    audio_files = [os.path.join('./sounds/effect/battle/', f) for f in os.listdir('./sounds/effect/battle/') if f.endswith('.mp3')]
    effect(audio_files)


def effect(audio_files):
    st.markdown(f"""
                <audio id="audio" autoplay>
                    <source src="data:audio/mp3;base64,{base64.b64encode(open(random.choice(audio_files), 'rb').read()).decode()}" type="audio/mp3">
                </audio>""", unsafe_allow_html=True)


def ambient():
    audio_files = [os.path.join('./sounds/ambient/', f) for f in os.listdir('./sounds/ambient/') if f.endswith('.mp3')]

    concatenated_audio = b""
    for file_path in audio_files:
        with open(file_path, 'rb') as f:
            concatenated_audio += f.read()

    # Encoder le fichier audio en base64
    audio_data = base64.b64encode(concatenated_audio).decode()

    # Inclure le fichier audio dans st.markdown()
    st.markdown(f"""
                <audio id="audio" autoplay loop>
                    <source src="data:audio/mp3;base64,{audio_data}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>""", unsafe_allow_html=True)
