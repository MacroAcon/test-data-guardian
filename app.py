import streamlit as st
import pandas as pd
import datetime
import random
import plotly.express as px

# Set page config
st.set_page_config(page_title="Data Guardian MVP", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Marketplace", "Transaction Log", "Settings"])

# Dummy user data function
def fetch_user_data():
    data = {
        "Data Type": ["Health", "Financial", "Media"],
        "Shared": [True, False, True],
        "Earnings": [round(random.uniform(0.5, 5.0), 2) for _ in range(3)]
    }
    return pd.DataFrame(data)

# Dummy transaction log
def fetch_transaction_log():
    transactions = []
    for i in range(1, 6):
        transactions.append({
            "Timestamp": (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
            "Transaction ID": f"TXN{i}{random.randint(100,999)}",
            "Data Shared": random.choice(["Health", "Financial", "Media"]),
            "Amount Earned": round(random.uniform(0.5, 5.0), 2)
        })
    return pd.DataFrame(transactions)

# Dashboard Page
if page == "Dashboard":
    st.title("📊 Data Guardian Dashboard")
    st.write("Monitor your data sharing status and earnings.")
    
    user_data = fetch_user_data()
    total_earnings = user_data["Earnings"].sum()
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Earnings", f"${total_earnings:.2f}", "+5% this week")
    col2.metric("Active Shares", user_data["Shared"].sum(), "+1 New")
    col3.metric("Total Transactions", len(fetch_transaction_log()), "+2 Today")
    
    # Pie chart for data sharing
    st.subheader("Your Data Sharing Preferences")
    fig = px.pie(user_data, names="Data Type", values="Earnings", title="Earnings by Data Type")
    st.plotly_chart(fig, use_container_width=True)

# Marketplace Page
elif page == "Marketplace":
    st.title("🛒 Data Monetization Marketplace")
    st.write("Enable or disable data sharing options.")
    user_data = fetch_user_data()
    
    for index, row in user_data.iterrows():
        col1, col2 = st.columns(2)
        col1.write(f"**{row['Data Type']} Data**")
        col2.toggle("Share Data", value=row['Shared'], key=row['Data Type'])
    
    # Bar Chart Visualization
    st.subheader("Estimated Earnings by Data Type")
    fig = px.bar(user_data, x="Data Type", y="Earnings", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# Transaction Log Page
elif page == "Transaction Log":
    st.title("🔗 Blockchain Transaction Log")
    txn_log = fetch_transaction_log()
    st.dataframe(txn_log)
    
    # Line chart for earnings over time
    st.subheader("Earnings Over Time")
    fig = px.line(txn_log, x="Timestamp", y="Amount Earned", title="Earnings Trend")
    st.plotly_chart(fig, use_container_width=True)

# Settings Page
elif page == "Settings":
    st.title("⚙️ User Settings")
    st.write("Manage your data sharing preferences.")
    for data_type in ["Health", "Financial", "Media"]:
        st.checkbox(f"Share {data_type} Data", value=True)
    if st.button("Save Settings"):
        st.success("Settings saved!")
