import json
import streamlit as st

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

# CSSスタイルで横スクロールを有効にする
st.markdown(
    """
    <style>
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
                st.subheader("followers_1.jsonだけにある値")
                st.markdown('<div class="scrollable">' + '<br>'.join(only_in_followers) + '</div>', unsafe_allow_html=True)

            with col2:
                st.subheader("following.jsonだけにある値")
                st.markdown('<div class="scrollable">' + '<br>'.join(only_in_following) + '</div>', unsafe_allow_html=True)

            with col3:
                st.subheader("両方にある値")
                st.markdown('<div class="scrollable">' + '<br>'.join(in_both) + '</div>', unsafe_allow_html=True)

            # 結果をファイルに出力
            if st.button("結果をテキストファイルに出力"):
                with open('only_in_followers.txt', 'w') as a_output:
                    for value in only_in_followers:
                        a_output.write(f"{value}\n")

                with open('only_in_following.txt', 'w') as b_output:
                    for value in only_in_following:
                        b_output.write(f"{value}\n")

                with open('in_both.txt', 'w') as both_output:
                    for value in in_both:
                        both_output.write(f"{value}\n")

                st.success("結果がテキストファイルに出力されました。")
else:
    st.warning("2つのファイルをアップロードしてください。")
