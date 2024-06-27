import base64
import random
import os
import uuid

import streamlit as st


def main_game():
    audio_files = ['sounds/ambient-space-noise-55472.mp3', 'sounds/oscillating-space-waves-31400.mp3',
                   'sounds/space-ambience-56265.mp3', 'sounds/space-rumble-29970.mp3']
    output_audio(audio_files)


def battle():
    audio_files = ['sounds/space-attack-45505.mp3', 'sounds/space-danger-32677.mp3']
    st.markdown(f"""
                        <audio id="audio" autoplay>
                            <source src="data:audio/mp3;base64,{base64.b64encode(open(random.choice(audio_files), 'rb').read()).decode()}" type="audio/mp3">
                        </audio>
                        <script>
                            var audio = document.getElementById('audio');
                            audio.volume = 1.0;
                            document.addEventListener('DOMContentLoaded', function() {{
                                audio.play().catch(function(error) {{
                                    console.log('Playback prevented: ' + error);
                                }});
                            }});
                        </script>
                        """, unsafe_allow_html=True)


def output_audio(audio_files):
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
            </audio>
            <script>
                var audio = document.getElementById('audio');
                audio.volume = 1.0;
                document.addEventListener('DOMContentLoaded', function() {{
                    audio.play().catch(function(error) {{
                        console.log('Playback prevented: ' + error);
                    }});
                }});
            </script>
        """, unsafe_allow_html=True)
