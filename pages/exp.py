import random
import time

import streamlit as st

# random.seed(1234)

VID2URL = {
    "1-1": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "1-2": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "1-3": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "1-4": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "2-1": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "2-2": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "2-3": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "2-4": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "3-1": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "3-2": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "3-3": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "3-4": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "4-1": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "4-2": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "4-3": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
    "4-4": "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2025_ral_exp/groups/group_0/cfm_1.mp4",
}
N_SCENARIOS = 2
N_VIDEOS = 4

if "scenarios" not in st.session_state:
    # Initialize
    scenarios = [
        {"idx": "1", "videos": ["1-1", "2-1", "3-1", "4-1"]},
        {"idx": "2", "videos": ["1-2", "2-2", "3-1", "4-1"]},
    ]
    for i in range(len(scenarios)):
        random.shuffle(scenarios[i]["videos"])
    random.shuffle(scenarios)
    st.session_state["scenarios"] = scenarios
    st.session_state["scenario_idx"] = 0
    st.session_state["video_idx"] = 0
    st.session_state["log"] = []


def choice_to_value(choice: str) -> int:
    value = 0
    match choice:
        case "A":
            value = 2
        case "ややA":
            value = 1
        case "ややB":
            value = -1
        case "B":
            value = -2
    return value


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
        q5_value = choice_to_value(
            st.session_state[f'q5_choice_{st.session_state["scenario_idx"]}_{idx}']
        )
        data["videos"][vids[idx]] = [q1_value, q2_value, q3_value, q4_value, q5_value]

    st.session_state["log"].append(data)

    # Move to next
    st.session_state["scenario_idx"] += 1
    st.session_state["video_idx"] = 0
    global VID2URL
    VID2URL = {k: v + f"?t={time.time()}" for k, v in VID2URL.items()}


# Interface
st.title("実験")
st.warning(
    "ページを更新したり、タブを閉じたり、戻るボタンを押したりしないでください。入力済みのデータが失われます。"
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
                st.subheader("Title")
                st.video(url)
                q1_choice = st.radio(
                    "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
                    options=[
                        "A",
                        "ややA",
                        "どちらとも言えない",
                        "ややB",
                        "B",
                    ],
                    index=None,
                    key=f'q1_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q2_choice = st.radio(
                    "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
                    options=[
                        "A",
                        "ややA",
                        "どちらとも言えない",
                        "ややB",
                        "B",
                    ],
                    index=None,
                    key=f'q2_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q3_choice = st.radio(
                    "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
                    options=[
                        "A",
                        "ややA",
                        "どちらとも言えない",
                        "ややB",
                        "B",
                    ],
                    index=None,
                    key=f'q3_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q4_choice = st.radio(
                    "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
                    options=[
                        "A",
                        "ややA",
                        "どちらとも言えない",
                        "ややB",
                        "B",
                    ],
                    index=None,
                    key=f'q4_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )
                q5_choice = st.radio(
                    "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
                    options=[
                        "A",
                        "ややA",
                        "どちらとも言えない",
                        "ややB",
                        "B",
                    ],
                    index=None,
                    key=f'q5_choice_{st.session_state["scenario_idx"]}_{idx}',
                    horizontal=True,
                )

        choice_has_not_been_made = (
            q1_choice is None
            or q2_choice is None
            or q3_choice is None
            or q4_choice is None
            or q5_choice is None
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
