

import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch

def classify_text(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    # Perform classification
    outputs = model(**inputs)
    logits = outputs.logits
    # Get predicted label
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

if st.session_state["authentication_status"]:


    
    # Function to perform text classification

    
    # Streamlit UI
    st.title('Text Classification with BERT')
    st.write('Enter some text for classification:')
    
    # Text input for user to enter text
    user_text = st.text_area('Text input')
    
    # Perform classification when button is clicked
    if st.button('Classify'):
        if user_text:
            # Perform text classification
            predicted_class = classify_text(user_text)
            # Display predicted class
            st.write(f'Predicted class: {predicted_class}')
        else:
            st.warning('Please enter some text for classification.')
    


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
