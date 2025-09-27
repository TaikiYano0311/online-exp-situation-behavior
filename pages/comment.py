import streamlit as st

st.title("コメント")
st.warning(
    "ページを更新したりタブを閉じたりしないでください。入力済みのデータが失われます。"
)

comment = st.text_area(
    label="コメント", placeholder="コメントがあれば入力してください"
)

st.header("Crowd Works ユーザーへ")
st.subheader("提出前にご確認ください！")
st.caption("Crowd Works以外のユーザーは無視してください。")
st.text(
    "Crowd Worksの画面上で、合言葉を入れる欄に次のひらがな4文字を入力してください。\n\n"
    "「うけつけ」"
)

if st.button(label="提出"):
    st.session_state["comment"] = comment
    st.switch_page("pages/outro.py")
