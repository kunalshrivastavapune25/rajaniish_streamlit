import streamlit as st

import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

if st.session_state["authentication_status"]:



# Generate sample dataset
    np.random.seed(0)
    X = np.random.rand(100, 1) * 10
    y = 3 * X.squeeze() + np.random.randn(100) * 3
    
    # Streamlit UI
    st.title('Simple Linear Regression Demo')
    
    # Plot sample data
    st.subheader('Sample Data:')
    fig, ax = plt.subplots()
    ax.scatter(X, y)
    ax.set_xlabel('X')
    ax.set_ylabel('y')
    st.pyplot(fig)
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Display regression line
    st.subheader('Regression Line:')
    x_values = np.linspace(0, 10, 100)
    y_values = model.predict(x_values.reshape(-1, 1))
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, color='red')
    ax.scatter(X, y)
    ax.set_xlabel('X')
    ax.set_ylabel('y')
    st.pyplot(fig)
    
    # Display coefficients
    st.subheader('Coefficients:')
    st.write(f'Intercept: {model.intercept_}')
    st.write(f'Slope: {model.coef_[0]}')




elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
