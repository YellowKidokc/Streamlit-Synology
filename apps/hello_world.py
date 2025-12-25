import datetime as dt

import streamlit as st


def main():
    st.title("Hello from Synology Streamlit Hub!")
    st.write(
        "Drop more apps into the `apps/` folder (or your mounted volume) and they will appear in the dropdown above."
    )
    st.metric("Server time", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.success("You're ready to build more dashboards.")


if __name__ == "__main__":
    main()
