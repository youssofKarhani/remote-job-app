from datetime import datetime

import altair as alt  # Added import for Altair
import pandas as pd
import streamlit as st  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

from jobs import fetch_jobs

GERMAN_CITIES = {
    "berlin": (52.5200, 13.4050),
    "hamburg": (53.5500, 10.0000),
    "munich": (48.1375, 11.5750),
    "münchen": (48.1375, 11.5750),
    "cologne": (50.9364, 6.9528),
    "köln": (50.9364, 6.9528),
    "frankfurt": (50.1106, 8.6822),
    "frankfurt am main": (50.1106, 8.6822),
    "stuttgart": (48.7775, 9.1800),
    "düsseldorf": (51.2333, 6.7833),
    "leipzig": (51.3400, 12.3750),
    "dortmund": (51.5139, 7.4653),
    "essen": (51.4508, 7.0131),
    "bremen": (53.0758, 8.8072),
    "dresden": (51.0500, 13.7400),
    "hannover": (52.3744, 9.7386),
    "nuremberg": (49.4528, 11.0778),
    "nürnberg": (49.4528, 11.0778),
    "duisburg": (51.4333, 6.7667),
    "bochum": (51.4819, 7.2169),
    "wuppertal": (51.2500, 7.1833),
    "bielefeld": (52.0167, 8.5333),
    "bonn": (50.7333, 7.1000),
    "münster": (51.9625, 7.6253),
    "karlsruhe": (49.0097, 8.4047),
    "mannheim": (49.4875, 8.4661),
    "augsburg": (48.3717, 10.8983),
    "wiesbaden": (50.0833, 8.2500),
    "gelsenkirchen": (51.5167, 7.1000),
    "mönchengladbach": (51.1967, 6.4417),
    "braunschweig": (52.2667, 10.5167),
    "chemnitz": (50.8333, 12.9167),
    "kiel": (54.3233, 10.1394),
    "aachen": (50.7756, 6.0836),
    "halle": (51.4833, 11.9667),
    "magdeburg": (52.1333, 11.6167),
    "freiburg": (47.9961, 7.8494),
    "krefeld": (51.3333, 6.5667),
    "mainz": (50.0000, 8.2667),
    "lübeck": (53.8667, 10.6833),
    "oberhausen": (51.4667, 6.8667),
    "rostock": (54.0833, 12.1333),
    "kassel": (51.3167, 9.5000),
    "hagen": (51.3500, 7.4667),
    "hamm": (51.6833, 7.8167),
    "saarbrücken": (49.2333, 7.0000),
    "potsdam": (52.4000, 13.0667),
    "ludwigshafen": (49.4833, 8.4333),
    "oldenburg": (53.1333, 8.2167),
    "leverkusen": (51.0333, 6.9833),
    "osnabrück": (52.2667, 8.0500),
    "solingen": (51.1667, 7.0833),
    "heidelberg": (49.4122, 8.7094),
    "darmstadt": (49.8728, 8.6511),
}

st.set_page_config(page_title="Remote Jobs", page_icon="💼", layout="wide")


@st.cache_data(ttl=3600)  # Cache data for 1 hour
def cached_fetch_jobs(page=1):
    """Fetch and cache jobs data for a specific page."""
    return fetch_jobs(page=page)


def get_time_difference(past_time):
    """Get a human-readable time difference with custom intervals."""
    delta = datetime.now() - past_time
    minutes = delta.total_seconds() / 60

    if minutes < 1:
        return f"{int(delta.total_seconds())} seconds ago"

    if minutes <= 5:
        return f"{int(minutes)} minutes ago"

    # After 5 minutes, snap to the nearest 10-minute interval starting from 5.
    # e.g., 5, 15, 25, etc.
    display_minutes = 10 * int((minutes - 5) // 10) + 5
    return f"{display_minutes} minutes ago"


def show_placeholder_cards(num=3):
    """Displays a number of placeholder job cards."""
    st.markdown("### ⏳ Fetching latest jobs, please wait...")
    st.divider()
    for _ in range(num):
        with st.container(border=True):
            st.markdown("### &nbsp;")
            st.markdown("<small>&nbsp;</small>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        st.write("")


def find_german_city_in_location(location_str, german_cities_dict):
    """Find a German city in a location string."""
    if pd.isna(location_str):
        return None

    location_lower = location_str.lower()

    # Sort keys by length (longest first) to prioritize more specific matches
    # e.g., "frankfurt am main" before "frankfurt"
    sorted_keys = sorted(german_cities_dict.keys(), key=len, reverse=True)

    for city_key in sorted_keys:
        if city_key in location_lower:
            # Standardize "frankfurt am main" to "frankfurt"
            if "frankfurt" in city_key:
                return "frankfurt"
            return city_key

    return None


def main():
    """Streamlit application for displaying remote jobs."""
    st.title("🚀 Latest Jobs from Arbeitnow")

    # --- Callbacks ---
    def reset_pagination():
        st.session_state.page = 1

    def clear_filters_func():
        st.session_state.remote_only = False
        st.session_state.country = ""
        st.session_state.keywords = ""
        st.session_state.selected_job_types = []
        st.session_state.sort_by = "Newest"
        st.session_state.page = 1

    # --- Sidebar ---
    st.sidebar.header("Controls")
    if st.sidebar.button("Refresh Jobs"):
        st.cache_data.clear()
        st.session_state.page = 1
        st.session_state.last_updated = datetime.now()
        st.success("Cache cleared! Fetching latest jobs...")
        st.rerun()

    st.sidebar.button("Clear Filters", type="secondary", on_click=clear_filters_func)

    st.sidebar.divider()

    # Initialize session state for page number and filters
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "country" not in st.session_state:
        st.session_state.country = ""
    if "keywords" not in st.session_state:
        st.session_state.keywords = ""
    if "selected_job_types" not in st.session_state:
        st.session_state.selected_job_types = []
    if "remote_only" not in st.session_state:
        st.session_state.remote_only = False
    if "sort_by" not in st.session_state:
        st.session_state.sort_by = "Newest"
    if "last_updated" not in st.session_state:
        st.session_state.last_updated = datetime.now()

    # --- Main Page Global Controls ---
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("🌎 Remote Only", key="remote_only", on_change=reset_pagination)
    with col2:
        st.selectbox(
            "Sort by",
            options=["Newest", "Oldest", "Company Name"],
            key="sort_by",
            on_change=reset_pagination,
        )

    # --- Sidebar Filters ---
    st.sidebar.subheader("Filter")
    st.sidebar.text_input("📍 Location", key="country", on_change=reset_pagination)
    st.sidebar.text_input(
        "🔑 Keywords (comma-separated)", key="keywords", on_change=reset_pagination
    )

    # --- Main Content Area ---
    placeholder = st.empty()
    with placeholder.container():
        show_placeholder_cards()

    try:
        # Fetch data
        first_page_jobs = cached_fetch_jobs(page=1)
        all_job_types = []
        if first_page_jobs:
            first_page_df = pd.DataFrame(first_page_jobs)
            all_job_types = first_page_df["job_types"].explode().str.strip().unique()
            all_job_types = [job_type for job_type in all_job_types if job_type]

        st.sidebar.multiselect(
            "📁 Job Type",
            options=all_job_types,
            key="selected_job_types",
            on_change=reset_pagination,
        )

        jobs = cached_fetch_jobs(page=st.session_state.page)

        # Now that data is fetched, clear the placeholder
        placeholder.empty()

        if jobs:
            df = pd.DataFrame(jobs)

            # Apply filters from session state
            if st.session_state.remote_only:
                df = df[df["remote"]]
            if st.session_state.country:
                df = df[
                    df["location"].str.contains(
                        st.session_state.country, case=False, na=False
                    )
                ]

            if st.session_state.keywords:
                keyword_list = [
                    k.strip().lower() for k in st.session_state.keywords.split(",")
                ]
                df = df[
                    df.apply(
                        lambda row: any(
                            k in row["title"].lower() or k in row["description"].lower()
                            for k in keyword_list
                        ),
                        axis=1,
                    )
                ]

            if st.session_state.selected_job_types:
                df = df[
                    df["job_types"].apply(
                        lambda x: any(
                            item in st.session_state.selected_job_types for item in x
                        )
                    )
                ]

            # Apply sorting
            if st.session_state.sort_by == "Newest" and "created_at" in df.columns:
                df = df.sort_values(by="created_at", ascending=False)
            elif st.session_state.sort_by == "Oldest" and "created_at" in df.columns:
                df = df.sort_values(by="created_at", ascending=True)
            elif (
                st.session_state.sort_by == "Company Name"
                and "company_name" in df.columns
            ):
                df = df.sort_values(by="company_name", ascending=True)

            # --- Status Line ---
            update_time_str = get_time_difference(st.session_state.last_updated)
            st.markdown(f"**{len(df)} jobs** • Page {st.session_state.page}")
            st.markdown(f"Updated {update_time_str}")
            st.divider()

            # --- Insights Section ---
            if not df.empty:
                st.write(f"Total jobs fetched: {len(df)}") # Debug print



                with st.expander("Insights", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        with st.container(border=True):
                            st.markdown("##### Top 5 Job Categories")
                            job_types_series = df["job_types"].explode().str.strip()
                            job_types_series = job_types_series[job_types_series != ""]

                            if not job_types_series.empty:
                                top_categories = (
                                    job_types_series.value_counts().nlargest(5)
                                )

                                chart_data = top_categories.reset_index()
                                chart_data.columns = ["Category", "Count"]  # type: ignore

                                chart = (
                                    alt.Chart(chart_data)
                                    .mark_bar()
                                    .encode(
                                        x="Count",
                                        y=alt.Y(
                                            "Category",
                                            sort="-x",
                                            axis=alt.Axis(labelAngle=0, labelLimit=300),
                                        ),
                                        tooltip=["Category", "Count"],
                                    )
                                )
                                st.altair_chart(chart, use_container_width=True)
                            else:
                                st.markdown("No category data to display.")

                    with col2:
                        with st.container(border=True):
                            st.markdown("##### Top 5 Job Locations")
                            locations_series = df["location"].dropna()
                            locations_series = locations_series[locations_series != ""]

                            if not locations_series.empty:
                                top_locations = (
                                    locations_series.value_counts().nlargest(5)
                                )

                                loc_chart_data = top_locations.reset_index()
                                loc_chart_data.columns = ["Location", "Count"]

                                loc_chart = (
                                    alt.Chart(loc_chart_data)
                                    .mark_bar()
                                    .encode(
                                        x="Count",
                                        y=alt.Y(
                                            "Location",
                                            sort="-x",
                                            axis=alt.Axis(labelAngle=0, labelLimit=300),
                                        ),
                                        tooltip=["Location", "Count"],
                                    )
                                )
                                st.altair_chart(loc_chart, use_container_width=True)
                            else:
                                st.markdown("No location data to display.")

                    # --- Germany Map ---
                    df["matched_city"] = df["location"].apply(
                        lambda x: find_german_city_in_location(x, GERMAN_CITIES)
                    )
                    df_germany = df[df["matched_city"].notna()].copy()

                    if not df_germany.empty:
                        st.divider()
                        st.markdown("##### Jobs Map - Germany")

                        job_counts = (
                            df_germany["matched_city"].value_counts().to_dict()
                        )

                        locations_to_plot = []
                        for city, count in job_counts.items():
                            if count > 0 and city in GERMAN_CITIES:
                                coords = GERMAN_CITIES[city]
                                locations_to_plot.append(
                                    {
                                        "lat": coords[0],
                                        "lon": coords[1],
                                        "size": count,
                                    }
                                )

                        if locations_to_plot:
                            map_df = pd.DataFrame(locations_to_plot)
                            st.map(map_df, zoom=5)
                        else:
                            st.markdown(
                                "No plottable German cities in the current results."
                            )

                st.divider()

            if df.empty:
                st.warning("🤔 No jobs match your current filters.")
                st.info(
                    "Try changing your keywords or clearing some filters "
                    "to see more results."
                )
                st.button("Clear All Filters", on_click=clear_filters_func)
            else:
                for index, row in df.iterrows():
                    with st.container(border=True):
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"### **{row['title']}**")
                        with col2:
                            st.link_button("🔗 View Job", row["url"], type="secondary")

                        st.markdown(
                            (
                                f"<small>at *{row['company_name']}* | "
                                f"📍 {row['location']}</small>"
                            ),
                            unsafe_allow_html=True,
                        )

                        # --- Tags ---
                        tags = []
                        if row.get("remote"):
                            tags.append("🌎 Remote")
                        if row.get("job_types"):
                            tags.extend(
                                t for t in row["job_types"] if t
                            )  # Ensure no empty tags

                        if tags:
                            tag_style = (
                                "background-color: #262626; color: #ffffff; "
                                "padding: 2px 8px; border-radius: 12px; "
                                "margin-right: 4px; font-size: 0.9em;"
                            )
                            tag_html = "".join(
                                f'<span style="{tag_style}">{tag}</span>'
                                for tag in tags
                            )
                            st.markdown(tag_html, unsafe_allow_html=True)

                        soup = BeautifulSoup(row["description"], "lxml")
                        description_text = soup.get_text()
                        preview_text = description_text[:200].strip()

                        show_more_key = f"show_more_{index}"
                        if show_more_key not in st.session_state:
                            st.session_state[show_more_key] = False

                        if st.session_state[show_more_key]:
                            # Show full description and other details
                            if "created_at" in row and pd.notna(row["created_at"]):
                                posted_date = pd.to_datetime(
                                    row["created_at"], unit="s"
                                ).strftime("%Y-%m-%d")
                                st.subheader(f"📅 Posted on: {posted_date}")
                                st.divider()
                            st.markdown(description_text, unsafe_allow_html=False)
                            st.link_button("🔗 View Job", row["url"], type="primary")

                            def create_show_less_callback(key):
                                def callback():
                                    st.session_state[key] = False

                                return callback

                            st.button(
                                "Show less",
                                key=f"show_less_btn_{index}",
                                on_click=create_show_less_callback(show_more_key),
                            )
                        else:
                            # Show preview and "Show more" button
                            st.markdown(
                                f"<div style='margin-top: 10px;'>{preview_text}...</div>",
                                unsafe_allow_html=True,
                            )

                            def create_show_more_callback(key):
                                def callback():
                                    st.session_state[key] = True

                                return callback

                            st.button(
                                "Show more",
                                key=f"show_more_btn_{index}",
                                on_click=create_show_more_callback(show_more_key),
                            )
                    st.write("")  # Add a vertical gap between cards

                # Pagination controls
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.session_state.page > 1:
                        if st.button("⬅️ Previous"):
                            st.session_state.page -= 1
                            st.rerun()
                with col3:
                    # Disable 'Next' if the current page has less than 100 jobs
                    # (assuming 100 is a full page)
                    if len(jobs) == 100:
                        if st.button("Next ➡️"):
                            st.session_state.page += 1
                            st.rerun()
                with col2:
                    st.write(f"Page {st.session_state.page}")

        else:
            st.warning("No more jobs found.")
            if st.button("⬅️ Go Back"):
                st.session_state.page -= 1
                st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
