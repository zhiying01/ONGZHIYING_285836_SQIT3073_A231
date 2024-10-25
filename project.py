# this is a group project, the leader of the group project is https://github.com/Vincentbeh00/Group-Project

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as date
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error
from plotly import graph_objs as go

st.title("Stock Prediction App")
# Example suggestions for stock tickers
suggestions = ['1155.KL', '5296.KL', '5306.KL', '4707.KL']

# User input with combo box
user_input = st.selectbox('Select Stock Ticker or Enter a Custom One', [''] + suggestions + ['Other'])

if user_input == 'Other':
    user_input = st.text_input('Enter Custom Stock Ticker', '')
if user_input:

    # Fetch historical stock data
    company = user_input

    # Get additional information about the company
    company_info = yf.Ticker(company).info

    # Define a start date and End Date
    start = date.datetime(2018, 1, 1)
    end = date.datetime(2023, 1, 1)

    data_load_state = st.text("Loading Data")
    # Read Stock Price Data 
    data = yf.download(company, start, end)
    data_load_state.text("Loading Done! :)")

    st.subheader('Company Information')
    st.text(f"Company Name: {company_info.get('shortName', 'N/A')} // {company_info.get('longName', 'N/A')}")
    st.text(f"Industry: {company_info.get('industry', 'N/A')}")
    st.text(f"Sector: {company_info.get('sector', 'N/A')}")
    st.text(f"Country: {company_info.get('country', 'N/A')}")
    st.text(f"Market Capitalization: {company_info.get('marketCap', 'N/A')}")
    st.text(f"Dividend Yield: {company_info.get('trailingAnnualDividendYield', 'N/A')}")
    st.text(f"Trailing P/E: {company_info.get('trailingPE', 'N/A')}")
    st.text(f"Forward P/E: {company_info.get('forwardPE', 'N/A')}")
    st.text(f"Mean Analyst Recommendation: {company_info.get('recommendationMean', 'N/A')}")
    st.text(f"52-Week Change: {company_info.get('52WeekChange', 'N/A')}")


    data['Target'] = data['Close'].shift(-1)  # Predicting the next day's Close price

    # Drop rows with NaN values
    data.dropna(inplace=True)

    # Features and target variable
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # You can include more features if needed
    y = data['Target']

    # Normalizing the data
    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X)
    y_normalized = scaler.fit_transform(np.array(y).reshape(-1, 1))

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_normalized, test_size=0.2, random_state=42)

    # Create and train the MLP Regressor
    model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    predictions = model.predict(X_test)

    # Reverse normalization for predictions
    predictions = scaler.inverse_transform(predictions.reshape(-1, 1))
    y_test_orig = scaler.inverse_transform(y_test)

    # Evaluate the model
    r2 = r2_score(y_test_orig, predictions)
    mse = mean_squared_error(y_test_orig, predictions)

    st.subheader('Data Tables')
    st.write(data.describe().round(3))
    st.write(data.tail().round(3))

    st.subheader('Stock Price Over Time')

    def plot_candlestick_chart():

        try:
            # Check if required columns are present
            required_columns = ['Open', 'High', 'Low', 'Close']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Missing columns: {missing_columns}")

            # Create the candlestick chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'],
                            increasing_line_color='green',  # Change color for increasing candles
                            decreasing_line_color='red',    # Change color for decreasing candles
                            line_width=2,  # Adjust line width
                            name='Candlestick Chart'))
            fig.update_layout(xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error: {e}")


    #Call the function
    plot_candlestick_chart()

    RS = f"R-squared Score: {r2}"
    MSE = f"Mean Squared Error: {mse}"


    st.subheader('Scatter Plot')
    # Plotting actual vs predicted values (scatter plot)
    fig = go.Figure()

    # Scatter plot for actual vs predicted values
    fig.add_trace(go.Scatter(x=y_test_orig.flatten(), y=predictions.flatten(),
                            mode='markers',
                            marker=dict(color='blue', opacity=0.5),
                            text=data.index[-len(y_test_orig):].strftime('%Y-%m-%d'),
                            name='Actual vs Predicted'))

    fig.update_layout(title='Actual vs Predicted Stock Prices',
                    xaxis_title='Actual Prices',
                    yaxis_title='Predicted Prices',
                    plot_bgcolor='white',
                    height = 600,
                    width = 800,
                    margin=dict(l=50, r=50, t=50, b=50),
                    title_x=0.38)
    
    fig.update_xaxes(
    showgrid = True,
    gridwidth = 0.5,
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
    )

    fig.update_yaxes(
        showgrid = True,
        gridwidth = 0.5,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    st.plotly_chart(fig)


        
    
    correlation_coefficient = np.corrcoef(y_test_orig.flatten(), predictions.flatten())[0, 1]
    st.subheader('Correlation between Actual and Predicted Prices')
    st.text(f"Correlation Coefficient: {correlation_coefficient}")
    st.text(RS)
    st.text(MSE)

    st.subheader('Prediction')

    start = date.datetime.today()-date.timedelta(days=30)
    end = date.datetime.today()
    # Read Stock Price Data 
    new_data = yf.download(company, start, end)

    # Feature Engineering
    new_data['Target'] = new_data['Close'].shift(-1)  # Predicting the next day's Close price

    # Handle NaN values
    new_data.fillna(method='ffill', inplace=True)
    # Features and target variable
    X_new = new_data[['Open', 'High', 'Low', 'Close', 'Volume']]  # You can include more features if needed
    y_new = new_data[['Target']][:-1]

    # Normalizing the new data
    scaler = MinMaxScaler()
    X_new_normalized = scaler.fit_transform(X_new)
    y_new_normalized = scaler.fit_transform(np.array(y_new).reshape(-1, 1))

    # Predict using the trained model
    predictions_new = model.predict(X_new_normalized)

    # Reverse normalization for predictions
    predictions_new = scaler.inverse_transform(predictions_new.reshape(-1, 1))
    y_new_orig = scaler.inverse_transform(y_new_normalized)

    r2_new = r2_score(y_new_orig, predictions_new[:-1])
    mse_new = mean_squared_error(y_new_orig, predictions_new[:-1])

    new_RS = f"R-squared Score for new data: {r2_new}"
    new_MSE = f"Mean Squared Error for new data: {mse_new}"

    lastdate=new_data.index[-1]
    newdate=lastdate+pd.DateOffset(days=1)
    newrow=pd.DataFrame(index=[newdate],columns=new_data.columns)
    new_data=pd.concat([new_data,newrow])

    # Plotting actual vs predicted values (scatter plot)
    fig = go.Figure()

    # Scatter plot for actual vs predicted values
    fig.add_trace(go.Scatter(x=y_new_orig.flatten(), y=predictions_new[:-1].flatten(),
                            mode='markers',
                            marker=dict(color='blue', opacity=0.5),
                            text=data.index[-len(y_test_orig):].strftime('%Y-%m-%d'),
                            name='Actual vs Predicted'))

    fig.update_layout(title='Actual vs Predicted Stock Prices',
                    xaxis_title='Actual Prices',
                    yaxis_title='Predicted Prices',
                    plot_bgcolor='white',
                    height = 600,
                    width = 800,
                    margin=dict(l=50, r=50, t=50, b=50),
                    title_x=0.4 )
    
    fig.update_xaxes(
    showgrid = True,
    gridwidth = 0.5,
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
    )

    fig.update_yaxes(
        showgrid = True,
        gridwidth = 0.5,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    st.plotly_chart(fig)

    # Plotting predicted values for the new data
    fig = plt.figure(figsize=(12, 6))
    plt.plot(new_data.iloc[1:-1].index, new_data[['Close']][1:-1], label='Actual Prices', color='green')
    plt.plot(new_data.iloc[1:-1].index, predictions_new[:-1], label='Predicted Prices', color='red')
    plt.plot(new_data.tail(2).index, predictions_new[-2:], label='Future Prices', color='blue')
    plt.title('Actual vs Predicted Stock Prices for New Data')
    plt.xlabel('Date')
    plt.ylabel('Stock Prices')
    plt.legend()
    st.pyplot(fig)

    correlation_coefficient_new = np.corrcoef(y_new_orig.flatten(), predictions_new[:-1].flatten())[0, 1]

    st.subheader('Correlation between Actual and Predicted Prices for New Data')
    st.text(f"Correlation Coefficient: {correlation_coefficient_new}")

    st.text(new_RS)
    st.text(new_MSE)
    predicted_price_tomorrow=predictions_new[-1]
    today_closing_price = new_data['Close'][-2]
    


    percentage_change = ((predicted_price_tomorrow - today_closing_price) / today_closing_price) * 100
    
    st.subheader('Buy/Sell Recommendation and Profit/Loss Prediction')
    st.write(f"Today's Stock Price({end.strftime('%d/%m/%Y')}): RM {today_closing_price:.2f}")
    st.write(f"Predicted Price Tomorrow({newdate.strftime('%d/%m/%Y')}): RM {' '.join(map(str, np.around(predictions_new[-1],3)))}")
    

    if percentage_change.item() > 0:
        
        st.success(f"Suggestion: Buy! Predicted profit percentage: {percentage_change.item():.2f}%")
    else:
        st.error(f"Suggestion: Do not buy! Predicted loss percentage: {abs(percentage_change.item()):.2f}%")


else:
    st.warning("Please enter a stock ticker.")
