import json

output_prefix = "./sample/output"
input_prefix = "./sample"

# followers_1.jsonとfollowing.jsonを読み込む
with open(f'{input_prefix}/followers_1.json', 'r') as a_file:
    followers_1_data = json.load(a_file)

with open(f'{input_prefix}/following.json', 'r') as b_file:
    following_data = json.load(b_file)

# followers_1.jsonとfollowing.jsonの値をリストに格納
followers_1_values = {item['string_list_data'][0]['value'] for item in followers_1_data}
following_values = {item['string_list_data'][0]['value'] for item in following_data['relationships_following']}

# 各比較結果を取得
only_in_followers_1: list = followers_1_values - following_values  # followers_1.jsonだけにある値
only_in_following: list = following_values - followers_1_values  # following.jsonだけにある値
in_both: list = followers_1_values & following_values    # 両方のJSONにある値

only_in_followers_1_sorted = sorted(only_in_followers_1)
only_in_following_sorted = sorted(only_in_following)
in_both_sorted = sorted(in_both)


# 結果をファイルに出力
with open(f'{output_prefix}/only_in_followers.txt', 'w') as followers_1_output:
    for value in only_in_followers_1_sorted:
        followers_1_output.write(f"{value}\n")

with open(f'{output_prefix}/no_follow_back.txt', 'w') as following_output:
    for value in only_in_following_sorted:
        following_output.write(f"{value}\n")

with open(f'{output_prefix}/in_both.txt', 'w') as both_output:
    for value in in_both_sorted:
        both_output.write(f"{value}\n")

print("結果がそれぞれのファイルに出力されました。")
