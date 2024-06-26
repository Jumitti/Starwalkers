import base64
import random

import streamlit as st


def connexion_page():
    audio_files = ['sounds/space-adventure-29296.mp3', 'sounds/ambient-space-noise-55472.mp3',
                   'sounds/oscillating-space-waves-31400.mp3', 'sounds/space-ambience-56265.mp3',
                   'sounds/space-rumble-29970.mp3']
    output_audio(audio_files)


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
    st.markdown(f"""
                    <audio id="audio" autoplay loop>
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
