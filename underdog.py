import streamlit as st
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def make_text(elt):
    p_text = [p.text.strip() for p in elt.find_all("p")]
    return " - ".join([p_text[0], f"{p_text[1]} {p_text[2]}", p_text[3]])

st.title("Convert Underdog draft to csv")

st.write("In Chrome, go to the full draft view and click this icon:")
st.image("images/arrow.png", width=30)

st.write('''Next (still in Chrome) go to View->Developer->JavaScript Console (or hit command+option+j on Mac) and then run `copy(document.querySelector('html').outerHTML)` which will copy the html to your clipboard.
''')

st.write("Paste the html below (the text should contain all the data and should be very long).  Hit command+return on Mac when you're done.")

html = st.text_area('Paste the html here')

soup = BeautifulSoup(html, "html.parser")

div_list = soup.find_all("div")

user_list = [elt for elt in div_list if elt.has_attr("class") and "userHeader" in elt["class"][0]]

users = [elt.text for elt in user_list]

pick_list = [elt for elt in div_list if elt.has_attr("class") and "draftBoardCell" in elt["class"][0]]

str_list = [make_text(elt) for elt in pick_list]

try:
    df = pd.DataFrame(np.array(str_list).reshape((12, 18), order='A').T, columns=users)

    csv = df.to_csv(index=False, header=True).encode('utf-8')
    st.download_button(
            "Press to Download",
            csv,
            "draft.csv",
            "text/csv"
            )
except ValueError:
    pass
