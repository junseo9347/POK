import streamlit as st
import csv
import random
from konlpy.tag import Kkma
import matplotlib.pyplot as plt
from matplotlib import rc


def speech():
    for group in csv.reader(open("speech.csv")):
        for sentence in group:
            yield sentence + "."


k = Kkma()
sequences = {}
morphs = {}
for sentence in speech():
    l = k.morphs(sentence)
    for morph in l:
        morphs[morph] = morphs.get(morph, 0) + 1
    for i in range(len(l)-1):
        if l[i] not in sequences:
            sequences[l[i]] = dict()
        sequences[l[i]][l[i+1]] = sequences[l[i]].get(l[i+1], 0) + 1

graph = {k: (list(v.keys()), list(v.values())) for k, v in sequences.items()}

rc("font", **{"family": "sans-serif", "sans-serif": ["NanumGothic"]})
sm = sorted(((k, v) for k, v in morphs.items()), key=(lambda k: k[1]), reverse=True)[:16]
plt.bar([v[0] for v in sm], [v[1] for v in sm])
st.pyplot(plt.gcf())


txt = ["한국"]
for i in range(1000):
    try:
        prev = graph[txt[-1]]
    except KeyError:
        txt.pop()
        continue
    txt.append(random.choices(prev[0], weights=prev[1])[0])
st.write(" ".join(txt))

"""
st.session_state.setdefault("i", 0)
msg = st.chat_message("human")
with msg:
    t = ""
    for _, t in zip(range(st.session_state.i), speech()):
        st.write(t)
    os.system(f"echo {t} | espeak-ng -p 100 -s 200 --stdout > /tmp/tts.wav")
st.audio("/tmp/tts.wav", autoplay=True)


def callback():
    st.balloons()
    st.session_state.i += 1


st.button(r"$\displaystyle\frac{d}{dx}\int{f\left(x\right)} = f(x)$", on_click=callback)
st.button(r"$\frac00$", on_click=lambda: st.session_state.pop("i"))
"""
