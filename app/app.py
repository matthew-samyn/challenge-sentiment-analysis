from PIL import Image
from utils.streamlit_functions import *

header = st.container()
plots = st.container()
scrape_section = st.container()
st.sidebar.title("Sentiment analysis")
brooklyn_99_button = st.sidebar.selectbox("What show would you like to analyze?",
                                          options=["Brooklyn 99","Analyze your own favorite show"])

if brooklyn_99_button == "Brooklyn 99":
    with header:
        # st.header("_ Header  _")
        st.title(" My favourite show ")
        image = Image.open('visuals/Brooklyn-Nine-Nine.jpg')
        st.image(image)
        st.write('---')

    with plots:
        df = pd.read_csv("files/brooklyn99.csv")
        with st.spinner(f"""
        Processing {len(df)} tweets
        """):
        #     df["sentiment"], df["cleaned_tweet"] = \
        #         return_sentiments(df["text"])
            st.success(f"Processed {len(df)} tweets")
        # df.to_csv("files/brooklyn99.csv", index=False)

        fig = show_sentiment_distribution(df["sentiment"], title="Brooklyn99 sentiment analysis")
        st.plotly_chart(fig, use_container_width=True)

elif brooklyn_99_button == "Analyze your own favorite show":
    with header:
        # st.header("_ Header  _")
        image = Image.open('visuals/your_turn.jpg')
        st.image(image)
        st.write('---')

    with plots:
        inputted_text = st.text_input("Enter the hashtag you want to search for on Twitter:", value="#")
        if inputted_text not in ["","#"]:
            with st.spinner(f"Searching Twitter for {inputted_text}"):
                df = scrape_twitter([inputted_text])
                st.success(f"Found {len(df)} relevant tweets")

            with st.spinner(f"""
            Processing all tweets
            """):
                df["sentiment"], df["cleaned_tweet"] = \
                    return_sentiments(df["text"])
                st.success(f"Processed {len(df)} tweets")

            fig = show_sentiment_distribution(df["sentiment"], title=f"{inputted_text} sentiment analysis")
            st.plotly_chart(fig, use_container_width=True)

