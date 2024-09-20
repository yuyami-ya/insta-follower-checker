import json
import streamlit as st
import io  # メモリ上にファイルを作成するためのモジュール

def load_json(uploaded_file):
    try:
        return json.load(uploaded_file)
    except json.JSONDecodeError:
        st.error("JSONの読み込みに失敗しました。ファイルの形式を確認してください。")
        return None
    except Exception as e:
        st.error(f"予期しないエラーが発生しました: {str(e)}")
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
        st.error(f"JSONフォーマットのエラー: {str(e)} キーが見つかりませんでした。")
        return None, None, None
    except Exception as e:
        st.error(f"予期しないエラーが発生しました: {str(e)}")
        return None, None, None

# CSSでsubheaderをスクロール時に固定するスタイル
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

# StreamlitアプリのUI部分
st.title("JSONファイル比較アプリ")

# ファイルアップロード
followers_file = st.file_uploader("followers_1.jsonをアップロード", type="json")
following_file = st.file_uploader("following.jsonをアップロード", type="json")

if followers_file and following_file:
    # JSONデータを読み込む
    followers_data = load_json(followers_file)
    following_data = load_json(following_file)

    if followers_data and following_data:
        # JSONを比較
        only_in_followers, only_in_following, in_both = compare_json(followers_data, following_data)

        # 結果を3列レイアウトで表示
        if only_in_followers is not None and only_in_following is not None and in_both is not None:
            col1, col2, col3 = st.columns(3)  # 3列のレイアウトを作成

            with col1:
                st.markdown('<div class="sticky-header">followers_1.jsonだけにある値</div>', unsafe_allow_html=True)
                st.markdown('<div class="scrollable">' + '<br>'.join(only_in_followers) + '</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="sticky-header">following.jsonだけにある値</div>', unsafe_allow_html=True)
                st.markdown('<div class="scrollable">' + '<br>'.join(only_in_following) + '</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="sticky-header">両方にある値</div>', unsafe_allow_html=True)
                st.markdown('<div class="scrollable">' + '<br>'.join(in_both) + '</div>', unsafe_allow_html=True)

            # 結果をテキストファイルとしてダウンロードできるようにする
            # 1. followers_1.jsonにだけある値
            followers_buffer = io.StringIO()
            for value in only_in_followers:
                followers_buffer.write(f"{value}\n")
            st.download_button(
                label="followers_1.jsonだけにある値をダウンロード",
                data=followers_buffer.getvalue(),
                file_name="only_in_followers.txt",
                mime="text/plain"
            )

            # 2. following.jsonにだけある値
            following_buffer = io.StringIO()
            for value in only_in_following:
                following_buffer.write(f"{value}\n")
            st.download_button(
                label="following.jsonだけにある値をダウンロード",
                data=following_buffer.getvalue(),
                file_name="only_in_following.txt",
                mime="text/plain"
            )

            # 3. 両方にある値
            both_buffer = io.StringIO()
            for value in in_both:
                both_buffer.write(f"{value}\n")
            st.download_button(
                label="両方にある値をダウンロード",
                data=both_buffer.getvalue(),
                file_name="in_both.txt",
                mime="text/plain"
            )
else:
    st.warning("2つのファイルをアップロードしてください。")
