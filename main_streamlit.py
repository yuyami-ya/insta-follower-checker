import json
import streamlit as st
import io  # メモリ上にファイルを作成するためのモジュール

def load_json(uploaded_file):
    try:
        return json.load(uploaded_file)
    except json.JSONDecodeError:
        st.error("Failed to load JSON. Please check the format of the file")
        return None
    except Exception as e:
        st.error(f"Unexpected Error. upload correct file. : {str(e)}")
        return None

def compare_json(a_data, b_data):
    try:
        a_values = {item['string_list_data'][0]['value'] for item in a_data}
        b_values = {item['string_list_data'][0]['value'] for item in b_data['relationships_following']}
        
        only_in_a = a_values - b_values
        only_in_b = b_values - a_values
        in_both = a_values & b_values

        return only_in_a, only_in_b, in_both

    except KeyError as e:
        st.error(f"JSON format error. upload correct file. : {str(e)} couldnt find Key.")
        return None, None, None
    except Exception as e:
        st.error(f"Unexpected Error. upload correct file. : {str(e)}")
        return None, None, None

# CSS style to stick subheader when scrolling
st.markdown(
    """
    <style>
    .sticky-header {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 100;
        padding: 10px 0;
        text-align: center;
    }
    .scrollable {
        overflow-x: auto;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Instagram Follow Follower Checker")

# Upload File
followers_file = st.file_uploader("Upload followers_1.json", type="json")
following_file = st.file_uploader("Upload following.json", type="json")

if followers_file and following_file:
    followers_data = load_json(followers_file)
    following_data = load_json(following_file)

    if followers_data and following_data:
        only_in_followers, only_in_following, in_both = compare_json(followers_data, following_data)

        # output 3 row
        if only_in_followers is not None and only_in_following is not None and in_both is not None:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="sticky-header">only followers_1.json</div>', unsafe_allow_html=True)
                st.markdown('<div class="scrollable">' + '<br>'.join(only_in_followers) + '</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="sticky-header">only following.json</div>', unsafe_allow_html=True)
                st.markdown('<div class="scrollable">' + '<br>'.join(only_in_following) + '</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="sticky-header">both</div>', unsafe_allow_html=True)
                st.markdown('<div class="scrollable">' + '<br>'.join(in_both) + '</div>', unsafe_allow_html=True)

            # 1. only followers_1.json
            followers_buffer = io.StringIO()
            for value in only_in_followers:
                followers_buffer.write(f"{value}\n")
            st.download_button(
                label="Download the values ​​only in followers_1.json",
                data=followers_buffer.getvalue(),
                file_name="only_in_followers.txt",
                mime="text/plain"
            )

            # 2. only following.json
            following_buffer = io.StringIO()
            for value in only_in_following:
                following_buffer.write(f"{value}\n")
            st.download_button(
                label="Download the values ​​only in following.json",
                data=following_buffer.getvalue(),
                file_name="only_in_following.txt",
                mime="text/plain"
            )

            # 3. in both
            both_buffer = io.StringIO()
            for value in in_both:
                both_buffer.write(f"{value}\n")
            st.download_button(
                label="Download in Both",
                data=both_buffer.getvalue(),
                file_name="in_both.txt",
                mime="text/plain"
            )
else:
    st.warning("Please upload two files.")
