import random
import time
from functools import reduce

def add(a, b):
    return a + b

import streamlit as st
from streamlit_scroll_to_top import scroll_to_here

# random.seed(1234)

#url_turorial = "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/20250926-carlos-yano-situation-behavior/1-1dd.mp4"

folder = "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/20250926-carlos-yano-situation-behavior/"

indices = ["1-1"]


video_ids = [
    f"{idx}{t}"
    for t in ["dd"]
    for idx in indices
]
VID2URL = {
    video_id: f"{folder}{video_id}.mp4"
    for video_id in video_ids
}


# st.write(video_ids)
# st.write(VID2URL)
# assert 0
N_SCENARIOS = 1
N_VIDEOS = 1



if "scenarios" not in st.session_state:
    # Initialize
    scenarios_tutorial = [
        {"idx": "1-1", "videos": ["1-1dd"],},
    ]
    scenarios = scenarios_tutorial
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
    #data["ranking"] = [f"{name}_{vids[idx]}" for idx, name in enumerate(st.session_state[f'ranking_{st.session_state["scenario_idx"]}'])]
    #data["comment"] = st.session_state[f'comment_{st.session_state["scenario_idx"]}']
    st.session_state["log"].append(data)

    # Move to next
    st.session_state["scenario_idx"] += 1
    global VID2URL
    VID2URL = {k: v + f"?t={time.time()}" for k, v in VID2URL.items()}
    scroll_to_here(0, "top")


# Interface
st.title("練習")
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
        st.switch_page("pages/exp.py")

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
                    "Q1: ロボットの話し方、表情、動きなどを見て、人間らしいと感じましたか、それとも機械的だと感じましたか？\n\n1: 非常に機械的; . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7: 非常に人間らしい",
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

        #with st.container(border=True):
        #    st.markdown(
        #    """4つのビデオについて、良かった点、悪かった点などのご意見・ご感想等ありましたらご自由にお書きください。
        #    """
        #    )
        #    st.text_area(
        #        label="コメント", #placeholder="コメントがあれば入力してください"
        #        key=f'comment_{st.session_state["scenario_idx"]}',
        #    ) """

        choice_has_not_been_made = (
            q1_choice is None
            or q2_choice is None
            or q3_choice is None
            or q4_choice is None
            #or len(st.session_state[f'ranking_{st.session_state["scenario_idx"]}']) < 4
        )
        st.markdown(
            """
            では、これより本実験を始めます。次のページにお進みください。
            """
        )
        st.button(
            "実験へ",
            on_click=on_form_submitted,
            disabled=choice_has_not_been_made,
            help="質問にお答えください。" if choice_has_not_been_made else "",
        )

    pbar.progress(
        st.session_state["scenario_idx"] / N_SCENARIOS,
        f"進捗: {st.session_state['scenario_idx']}/{N_SCENARIOS}",
    )


exp_fragment()

