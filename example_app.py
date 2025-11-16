from pathlib import Path

import streamlit as st
import music21

from streamlit_music_score import music_score, music_score_file, music_score_stream


st.set_page_config(page_title="Music Score Demo", layout="wide")
st.title("Streamlit Music Score")
st.write(
    "Render MusicXML strings in Streamlit using the "
    "[OpenSheetMusicDisplay](https://opensheetmusicdisplay.org/) library."
)
st.markdown("OSMD play functionality is only available for sponsors at the moment. As soon as it is released to the public this demo will be updated also to include play controls.")

score_file = Path("examples/twinkle.musicxml")

st.subheader("Example Score: Twinkle Twinkle Little Star")
st.markdown("Reading the MusicXML from a file and rendering it. The file needs to be a valid MusicXML format.")
score_xml = score_file.read_text(encoding="utf-8")
with st.expander("Sample source (MusicXML)", expanded=False):
    st.code(score_xml, language="xml")
music_score(score_xml, height=520, key="sample")

st.subheader("Try your own file")
uploaded = st.file_uploader("Upload a MusicXML (.xml/.musicxml) file", type=["xml", "musicxml"])
if uploaded:
    uploaded_xml = uploaded.read().decode("utf-8")
    music_score(uploaded_xml, height=520, key="uploaded")

st.subheader("Loading files directly")
st.write(
    "You can also load score files directly using the `music_score_file` function. Music21 loads the file and converts to xml directly"
)
abc_file = Path("examples/scale.abc")
score = music21.converter.parse(abc_file)
with st.expander("Sample source (ABC notation)", expanded=False):
    st.code(abc_file.read_text(encoding="utf-8"), language="abc")
st.markdown("Rendering the ABC notation file using music21:")
music_score_stream(score, height=520, key="abc_example", hide_part_name=True)    

st.subheader("Using music21 to load files")
st.write(
    "In this final example you can pass the music21 stream object directly and transpose it to any major key."
)
abc_file = Path("examples/scale.abc")
base_score = music21.converter.parse(abc_file)
with st.expander("Sample source (ABC notation)", expanded=False):
    st.code(abc_file.read_text(encoding="utf-8"), language="abc")

major_keys = ["C", "C#", "D-", "D", "E-", "E", "F", "F#", "G", "A-", "A", "B-", "B"]
target_key = st.selectbox("Transpose to key (major)", major_keys, index=major_keys.index("C"))
if target_key != "C":
    interval_to_target = music21.interval.Interval(music21.key.Key("C").tonic, music21.key.Key(target_key).tonic)
    score_for_render = base_score.transpose(interval_to_target)
else:
    score_for_render = base_score

if score_for_render.metadata is None:
    score_for_render.insert(0, music21.metadata.Metadata())
score_for_render.metadata.title = f"Scale in {target_key} Major"

st.markdown(f"Rendering the ABC notation file transposed to {target_key} major:")
music_score_stream(score_for_render, height=520, key="abc_transposed", hide_part_name=True)
