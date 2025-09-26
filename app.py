import datetime

import pytz
import streamlit as st

if "agree" not in st.session_state:
    st.session_state["agree"] = False

if not st.session_state["agree"]:
    st.title("はじめに")
    with st.container(border=True):
        st.header("実験概要")
        st.markdown(
            """
            本実験は、ロボットの表情の自然さを調査することを目的としています。

            ロボットの表情を見たあと、自然さに関する質問にご回答いただきます。所要時間は10分程度です。
            """
        )

        st.header("同意書")
        st.markdown(
            """
            本実験では、年齢や性別の個人情報を収集いたします。これらはデータ解析の目的のみに使用し、それ以外の目的には一切使用いたしません。

            「同意する」ボタンをクリックされた時点で、上記の内容をご理解のうえ、同意いただいたものとみなします。内容にご同意いただけない場合は、実験への参加をお控えいただき、画面を閉じてください。
            """
        )
        if st.button(label="同意する"):
            st.session_state["agree"] = True
            st.rerun()
else:
    st.title("個人情報")
    with st.container(border=True):
        userid = st.text_input(
            label="ユーザーID", placeholder="ユーザーIDを半角で入力してください"
        )
        userid_re_input = st.text_input(
            label="ユーザーIDの確認",
            placeholder="もう一度ユーザーIDを半角で入力してください",
        )
        gender = st.radio(
            label="性別",
            options=["男性", "女性", "その他"],
            horizontal=True,
            index=None,
        )
        age = st.radio(
            label="年齢",
            options=["20代以下", "20代", "30代", "40代", "50代", "60代", "70代以上"],
            horizontal=True,
            index=None,
        )

        if st.button(
            label="提出", disabled=userid is None or gender is None or age is None
        ):
            if userid_re_input != userid:
                st.warning(
                    "2回入力されたユーザーIDが一致していません。ユーザーIDを再度ご確認ください。"
                )
            else:
                st.session_state["userid"] = userid
                st.session_state["gender"] = gender
                st.session_state["age"] = age
                st.session_state["start_time"] = datetime.datetime.now(
                    pytz.timezone("Asia/Tokyo")
                ).strftime("%Y-%m-%d_%H-%M-%S")
                st.switch_page("pages/intro.py")
