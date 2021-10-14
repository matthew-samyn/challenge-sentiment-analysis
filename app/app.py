from PIL import Image
from utils.streamlit_functions import *
import streamlit as st

st.set_page_config(layout="wide")

header = st.container()
plots = st.container()
scrape_section = st.container()

# Handles the sidebar option
st.sidebar.title("Sentiment analysis")
brooklyn_99_button = st.sidebar.selectbox("What show would you like to analyze?",
                                          options=["Brooklyn 99","Analyze your own favorite show"])

# Handles the first option from the sidebar.
# Loads a csv, prescraped from Twitter.
# Shows a piechart with useful info on sentiment analysis.
if brooklyn_99_button == "Brooklyn 99":
    with header:
        st.title(" My favourite show ")
        image = Image.open('visuals/Brooklyn-Nine-Nine.jpg')
        st.image(image)
        st.write('---')

    with plots:
        df = pd.read_csv("files/brooklyn99.csv")
        with st.spinner(f"""
        Processing {len(df)} tweets
        """):
            st.success(f"Processed {len(df)} tweets")

        fig = show_sentiment_distribution(df["sentiment"], plot_title="Brooklyn99 sentiment analysis")
        st.plotly_chart(fig, use_container_width=True)

# Handles the second option from the sidebar.
# Scrapes a searchterm given by the user.
# Shows a piechart with useful info on sentiment analysis.

elif brooklyn_99_button == "Analyze your own favorite show":
    with header:
        image = Image.open('visuals/your_turn.jpg')
        st.image(image)
        st.write('---')

    with plots:
        inputted_text = st.text_input("Enter the hashtag you want to search for on Twitter:", value="#")
        if inputted_text not in ["","#"]:
            with st.spinner(f"Searching Twitter for {inputted_text}"):
                df = scrape_twitter([inputted_text])
                st.success(f"Found {len(df)} relevant tweets")

            # Safety if no tweets were found.
            if len(df) == 0:
                st.write("Please try a different search message.")

            else:
                with st.spinner(f"""
                Processing all tweets
                """):
                    df["sentiment"], df["cleaned_tweet"] = \
                        return_sentiments(df["text"])
                    st.success(f"Processed {len(df)} tweets")

                fig = show_sentiment_distribution(df["sentiment"], plot_title=f"{inputted_text} sentiment analysis")
                st.plotly_chart(fig, use_container_width=True)

