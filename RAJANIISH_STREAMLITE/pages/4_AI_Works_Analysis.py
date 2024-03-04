
import streamlit as st

from transformers import pipeline
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

if st.session_state["authentication_status"]:


# Load sentiment analysis pipeline
    sentiment_classifier = pipeline("sentiment-analysis")
    
    # Streamlit UI
    st.title('Sentiment Analysis Demo')
    
    # Text input for user to enter text
    user_text = st.text_area("Enter text for sentiment analysis:")
    
    # Perform sentiment analysis when button is clicked
    if st.button("Analyze Sentiment"):
        if user_text:
            # Perform sentiment analysis on user input
            sentiment_result = sentiment_classifier(user_text)
            # Display sentiment analysis result
            st.write(f"Sentiment: {sentiment_result[0]['label']}")
            st.write(f"Confidence: {sentiment_result[0]['score']:.2f}")
        else:
            st.warning("Please enter some text for analysis.")

    

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
