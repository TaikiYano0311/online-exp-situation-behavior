import random
import time
from functools import reduce

def add(a, b):
    return a + b

import streamlit as st

# random.seed(1234)

folder = "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/20250926-carlos-yano-situation-behavior/"

indices = ["1-1", "1-2", "1-3", "2-1", "2-2", "2-3", "2-4", "3-1", "3-2", "3-3"]


video_ids = [
    f"{idx}{t}"
    for t in ["cc", "cd", "dc", "dd"]
    for idx in indices
]
VID2URL = {
    video_id: f"{folder}{video_id}.mp4"
    for video_id in video_ids
}

# st.write(video_ids)
# st.write(VID2URL)
# assert 0
N_SCENARIOS = 2
N_VIDEOS = 4

if "scenarios" not in st.session_state:
    # Initialize
    scenarios_A = [
        {"idx": "1", "videos": [["1-1dd", "1-1dc"], ["1-1cc", "1-1cd"]]},
        {"idx": "2", "videos": [["1-3dd", "1-3dc"], ["1-3cc", "1-3cd"]]},
        # {"idx": "3", "videos": [["2-1dd", "2-1dc"], ["2-1cc", "2-1cd"]]},
        # {"idx": "4", "videos": [["2-3dd", "2-3dc"], ["2-3cc", "2-3cd"]]},
        # {"idx": "5", "videos": [["3-2dd", "3-2dc"], ["3-2cc", "3-2cd"]]},
        # {"idx": "6", "videos": [["3-3dd", "3-3dc"], ["3-3cc", "3-3cd"]]},
    ]
    scenarios_B = [
        {"idx": "1", "videos": [["1-1dd", "1-1dc"], ["1-1cc", "1-1cd"]]},
        {"idx": "2", "videos": [["1-2dd", "1-2dc"], ["1-2cc", "1-2cd"]]},
        {"idx": "3", "videos": [["2-2dd", "2-2dc"], ["2-2cc", "2-2cd"]]},
        {"idx": "4", "videos": [["2-4dd", "2-4dc"], ["2-4cc", "2-4cd"]]},
        {"idx": "5", "videos": [["3-1dd", "3-1dc"], ["3-1cc", "3-1cd"]]},
        {"idx": "6", "videos": [["3-3dd", "3-3dc"], ["3-3cc", "3-3cd"]]},
    ]
    scenarios = scenarios_A
    # scenarios = scenarios_B
    for i in range(len(scenarios)):
        for j in range(len(scenarios[i]["videos"])):
            random.shuffle(scenarios[i]["videos"][j])
        random.shuffle(scenarios[i]["videos"])
        scenarios[i]["videos"] = reduce(add, scenarios[i]["videos"])
    random.shuffle(scenarios)
    # st.write(scenarios)
    st.session_state["scenarios"] = scenarios
    st.session_state["scenario_idx"] = 0
    st.session_state["log"] = []


def choice_to_value(choice: str) -> int:
    # value = 0
    # match choice:
    #     case "非常にそう思う":
    #         value = 2
    #     case "そう思う":
    #         value = 1
    #     case "そう思わない":
    #         value = -1
    #     case "B":
    #         value = -2
    return int(choice)


def on_form_submitted():
    # Record choice
    scenario = st.session_state["scenarios"][st.session_state["scenario_idx"]]
    vids = scenario["videos"]

    data = {"idx": scenario["idx"], "videos": {}}
    for idx in range(N_VIDEOS):
        q1_value = choice_to_value(
            st.session_state[f'q1_choice_{st.session_state["scenario_idx"]}_{idx}']
        )
        q2_value = choice_to_value(
            st.session_state[f'q2_choice_{st.session_state["scenario_idx"]}_{idx}']
        )
        q3_value = choice_to_value(
            st.session_state[f'q3_choice_{st.session_state["scenario_idx"]}_{idx}']
        )
        q4_value = choice_to_value(
            st.session_state[f'q4_choice_{st.session_state["scenario_idx"]}_{idx}']
        )
        data["videos"][vids[idx]] = [q1_value, q2_value, q3_value, q4_value]
    data["ranking"] = st.session_state[f'ranking_{st.session_state["scenario_idx"]}']
    data["commend"] = st.session_state[f'comment_{st.session_state["scenario_idx"]}']
    st.session_state["log"].append(data)

    # Move to next
    st.session_state["scenario_idx"] += 1
    global VID2URL
    VID2URL = {k: v + f"?t={time.time()}" for k, v in VID2URL.items()}


# Interface
st.title("実験")
st.warning(
    "注意：ページを更新したり、タブを閉じたり、戻るボタンを押したりしないでください。入力済みのデータが失われます。"
)
st.warning(
    """
    ・ビデオのタイトル画面に表示される「状況設定」と「客の種類」をご確認ください。

    ・ご自身が設定の客の立場で、ロボットから接客を受けていると想像しながらご覧ください。

    ・各ビデオを見た後に、質問にお答えください。
    """
)
pbar = st.progress(0, text=f"進捗: {0}/{N_SCENARIOS}")


@st.fragment
def exp_fragment():
    # Check if all completed
    if st.session_state["scenario_idx"] == N_SCENARIOS:
        # Move to next page
        st.switch_page("pages/comment.py")

    # Get sample info
    vids = st.session_state["scenarios"][st.session_state["scenario_idx"]]["videos"]
    urls = [VID2URL[vid] for vid in vids]

    # Place interface
    with st.container(border=True):
        for idx, url in enumerate(urls):
            with st.container(border=True):
                st.subheader(f"ビデオ{idx+1}")
                st.video(url)
                q1_choice = st.radio(
                    "Q1: ロボットの動作や表情などを見て、人間らしいと感じましたか、それとも機械的だと感じましたか？\n\n1: 非常に機械的; . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7: 非常に人間らしい",
                    options=[str(i) for i in range(1, 8)],
                    index=None,
                    key=f'q1_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q2_choice = st.radio(
                    "Q2: ロボットの話し方や態度は客の種類や状況に合っていると感じましたか？\n\n1: 全く合っていない; . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7: 非常に合っている",
                    options=[str(i) for i in range(1, 8)],
                    index=None,
                    key=f'q2_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q3_choice = st.radio(
                    "Q3: このロボットは心のこもった接客をしていると感じましたか？\n\n1: 全く心がこもっていない; . . . . . . . . . . . . . . . . . . . . . . . . 7: 非常に心がこもっている",
                    options=[str(i) for i in range(1, 8)],
                    index=None,
                    key=f'q3_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q4_choice = st.radio(
                    "Q4: ロボットの接客対応についてどのくらい満足しましたか？\n\n1: 非常に不満; . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7: 非常に満足",
                    options=[str(i) for i in range(1, 8)],
                    index=None,
                    key=f'q4_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
        with st.container(border=True):
            st.subheader("４つのビデオの比較")
            st.pills(
                "以上の４つのビデオについて、対応が良いと感じられた順に選択してください。",
                options=[f"ビデオ{idx+1}" for idx in range(4)],
                key=f'ranking_{st.session_state["scenario_idx"]}',
                selection_mode="multi"
            )
            ranking = st.session_state[f'ranking_{st.session_state["scenario_idx"]}']
            st.write(f"あなたが選んだ順位: {ranking}")
            def reset_ranking():
                st.session_state[f'ranking_{st.session_state["scenario_idx"]}'] = []
            st.button("順位をリセット", on_click=reset_ranking)

        with st.container(border=True):
            st.markdown(
            """
            4つのビデオについて、良かった点、悪かった点などのご意見・ご感想等ありましたらご自由にお書きください。
            """
            )
            st.text_area(
                label="コメント", #placeholder="コメントがあれば入力してください"
                key=f'comment_{st.session_state["scenario_idx"]}',
            )

        choice_has_not_been_made = (
            q1_choice is None
            or q2_choice is None
            or q3_choice is None
            or q4_choice is None
            or len(st.session_state[f'ranking_{st.session_state["scenario_idx"]}']) < 4
        )
        st.button(
            "次へ",
            on_click=on_form_submitted,
            disabled=choice_has_not_been_made,
            help="質問にお答えください。" if choice_has_not_been_made else "",
        )

    pbar.progress(
        st.session_state["scenario_idx"] / N_SCENARIOS,
        f"進捗: {st.session_state['scenario_idx']}/{N_SCENARIOS}",
    )


exp_fragment()
