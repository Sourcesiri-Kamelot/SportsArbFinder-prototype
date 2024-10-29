import subprocess
import sys
import time
import signal
import streamlit as st

def run_arbitrage_finder(region, market, cutoff, interactive, offline_file):
    command = [sys.executable, "main.py", "-r", region, "-c", str(cutoff), "-s", "response_data.json", "--market", market]
    if interactive:
        command.append("-i")
    if offline_file:
        command.extend(["-o", offline_file])
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        st.error("An error occurred while running the arbitrage finder.")
    except KeyboardInterrupt:
        st.warning("Arbitrage finder interrupted. Exiting.")

def main():
    st.title("Sports Betting Arbitrage Finder Easy Run")

    st.sidebar.header("Configuration")
    region = st.sidebar.selectbox("Choose a region", ["us", "eu", "uk", "au"], index=0)
    market = st.sidebar.selectbox("Choose a betting market", ["h2h", "spreads", "totals", "outrights", "h2h_lay", "outrights_lay"], index=0)
    cutoff = st.sidebar.number_input("Enter minimum profit margin percentage", min_value=0.0, value=0.0, step=0.1)
    interactive = st.sidebar.checkbox("Enable interactive betting calculator", value=False)
    offline = st.sidebar.checkbox("Use offline data", value=False)
    offline_file = st.sidebar.text_input("Enter the name of the offline data file", value="response_data.json") if offline else None

    if st.sidebar.button("Run Arbitrage Finder"):
        st.write("Running the arbitrage finder...")
        run_arbitrage_finder(region, market, cutoff, interactive, offline_file)
        st.write("Arbitrage finder completed.")

    if st.sidebar.button("Launch Viewer"):
        st.write("Launching the arbitrage opportunities viewer...")
        try:
            subprocess.run([sys.executable, "viewer.py"], check=True)
        except subprocess.CalledProcessError:
            st.error("An error occurred while running the viewer.")
        except KeyboardInterrupt:
            st.warning("Viewer interrupted. Exiting.")

if __name__ == "__main__":
    main()
