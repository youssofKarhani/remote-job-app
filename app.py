import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from jobs import fetch_jobs

st.set_page_config(page_title="Remote Jobs", page_icon="💼", layout="wide")


@st.cache_data(ttl=3600)  # Cache data for 1 hour
def cached_fetch_jobs(page=1):
    """Fetch and cache jobs data for a specific page."""
    return fetch_jobs(page=page)


def main():
    """Streamlit application for displaying remote jobs."""
    st.title("🚀 Latest Remote Jobs")
    st.markdown(
        """
        This app fetches the latest remote job listings from the [Arbeitnow API](https://arbeitnow.com/api/job-board-api).
        Job data is cached for 1 hour to ensure fast loading times.
        """
    )

    # --- Callbacks ---
    def reset_pagination():
        st.session_state.page = 1

    # --- Sidebar ---
    st.sidebar.header("Controls")
    if st.sidebar.button("Refresh Jobs"):
        st.cache_data.clear()
        st.session_state.page = 1
        st.success("Cache cleared! Fetching latest jobs...")
        st.rerun()

    if st.sidebar.button("Clear Filters"):
        st.session_state.remote_only = False
        st.session_state.country = ""
        st.session_state.keywords = ""
        st.session_state.selected_job_types = []
        st.session_state.sort_by = "Newest"
        st.session_state.page = 1
        st.rerun()

    # Initialize session state for page number and filters
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if 'country' not in st.session_state:
        st.session_state.country = ""
    if 'keywords' not in st.session_state:
        st.session_state.keywords = ""
    if 'selected_job_types' not in st.session_state:
        st.session_state.selected_job_types = []
    if 'remote_only' not in st.session_state:
        st.session_state.remote_only = False
    if 'sort_by' not in st.session_state:
        st.session_state.sort_by = "Newest"

    try:
        # Fetch a stable list of job types from the first page
        with st.spinner("Fetching initial job types..."):
            first_page_jobs = cached_fetch_jobs(page=1)
        if first_page_jobs:
            first_page_df = pd.DataFrame(first_page_jobs)
            all_job_types = first_page_df['job_types'].explode().str.strip().unique()
            all_job_types = [job_type for job_type in all_job_types if job_type]
        else:
            all_job_types = []

        with st.spinner(f"Fetching jobs for page {st.session_state.page}..."):
            jobs = cached_fetch_jobs(page=st.session_state.page)
        if jobs:
            df = pd.DataFrame(jobs)

            # Filtering UI
            st.sidebar.header("Filter & Sort")
            st.sidebar.checkbox("🌎 Remote Only", key="remote_only", on_change=reset_pagination)
            st.sidebar.text_input("📍 Location", key="country", on_change=reset_pagination)
            st.sidebar.text_input("🔑 Keywords (comma-separated)", key="keywords", on_change=reset_pagination)
            st.sidebar.multiselect("📁 Job Type", options=all_job_types, key="selected_job_types", on_change=reset_pagination)
            st.sidebar.selectbox("Sort by", options=["Newest", "Oldest", "Company Name"], key="sort_by", on_change=reset_pagination)

            # Apply filters from session state
            if st.session_state.remote_only:
                df = df[df["remote"] == True]
            if st.session_state.country:
                df = df[df["location"].str.contains(st.session_state.country, case=False, na=False)]
            
            if st.session_state.keywords:
                keyword_list = [k.strip().lower() for k in st.session_state.keywords.split(',')]
                df = df[df.apply(lambda row: any(k in row['title'].lower() or k in row['description'].lower() for k in keyword_list), axis=1)]

            if st.session_state.selected_job_types:
                df = df[df['job_types'].apply(lambda x: any(item in st.session_state.selected_job_types for item in x))]

            # Apply sorting
            if st.session_state.sort_by == "Newest":
                df = df.sort_values(by="created_at", ascending=False)
            elif st.session_state.sort_by == "Oldest":
                df = df.sort_values(by="created_at", ascending=True)
            elif st.session_state.sort_by == "Company Name":
                df = df.sort_values(by="company_name", ascending=True)


            st.info(f"Showing {len(df)} jobs on page {st.session_state.page}.")

            for index, row in df.iterrows():
                with st.expander(f"{row['title']} at {row['company_name']} - {row['location']} ({', '.join(row['job_types'])})"):
                    st.markdown(f"**📅 Posted on:** {pd.to_datetime(row['created_at'], unit='s').strftime('%Y-%m-%d')}")
                    st.markdown(f"**🔗 [View Job]({row['url']})**")
                    with st.container():
                        soup = BeautifulSoup(row['description'], 'lxml')
                        st.markdown(soup.get_text(), unsafe_allow_html=False)
            
            # Pagination controls
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.session_state.page > 1:
                    if st.button("⬅️ Previous"):
                        st.session_state.page -= 1
                        st.rerun()
            with col3:
                # Disable 'Next' if the current page has less than 100 jobs (assuming 100 is a full page)
                if len(jobs) == 100:
                    if st.button("Next ➡️"):
                        st.session_state.page += 1
                        st.rerun()
            with col2:
                st.write(f"Page {st.session_state.page}")


        else:
            st.warning("No more jobs found.")
            if st.button("⬅️ Go Back"):
                st.session_state.page -=1
                st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
