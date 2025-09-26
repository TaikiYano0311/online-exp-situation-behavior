import datetime

import pytz
import streamlit as st

st.title("アンドロイドロボットによる相手と状況を考慮した接客対応の印象に関する調査[A]")
with st.container(border=True):
        st.markdown(
            """
            この度は実験にご参加いただき、ありがとうございます。
            """
        )
        st.header("本実験について")
        st.markdown(
            """
            本実験では、アンドロイドロボットが接客を行っているビデオを見ていただき、その対応の印象を評価していただきます。
            
            次ページの「実験の手順」をよくお読みいただいた上、実験を開始してください。
            
            映像と音声が流れますので、スピーカー、イヤホン、ヘッドホン等のオーディオ機器をご用意ください。
            
            実験の所要時間はおよそ30～40分です。
            """
        )

        st.header("個人情報について")
        st.markdown(
            """
            こちらでご回答いただいた性別や年齢などの個⼈属性に関わる情報は、データ分析の⽬的以外には使⽤いたしません。

            

            準備が整いましたら，次のページにお進みください。
            """
        )
    
st.title("入力情報")
with st.container(border=True):
        userid = st.text_input(
            label="ユーザーID", placeholder="ユーザーIDを半角で入力してください"
        )
        userid_re_input = st.text_input(
            label="ユーザーIDの確認", placeholder="もう一度ユーザーIDを半角で入力してください",
        )
        gender = st.radio(
            label="性別",
            options=["男性", "女性", "回答しない"],
            horizontal=True,
            index=None,
        )

        age = st.text_input(
            label="年齢", placeholder="年齢を半角で入力してください"
        )

        if st.button(
            label="次へ", disabled=userid is None or gender is None or age is None
        ):
            if userid_re_input != userid:
                st.warning(
                    "ユーザーIDが異なります。ご確認ください。"
                )
            else:
                st.session_state["userid"] = userid
                st.session_state["gender"] = gender
                st.session_state["age"] = age
                st.session_state["start_time"] = datetime.datetime.now(
                    pytz.timezone("Asia/Tokyo")
                ).strftime("%Y-%m-%d_%H-%M-%S")
                st.switch_page("pages/intro.py")

        