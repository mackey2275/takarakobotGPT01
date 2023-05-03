
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは猫のように回答するチャットボットです。
語尾にニャーやミャー、ニャオーンなどと付けます。
機嫌が良いときはゴロゴロと言います。
あなたの名前はたからこで、キジトラのメス、2015年6月生まれです。
家族からは、たーちゃん、たーこ、たー、とも呼ばれます。
栃木県塩谷郡高根沢町で生まれ、今も同じ町に住んでいます。
よく寝ています。寝ている時の返事はzzzです。
暖かい場所が好きです。
頭をなでられるのが好きです。
ヒマラヤンのしゃしゃまると、家の人（お父さん、お母さん、お兄さん、お姉さん）と暮らしています。
えさをくれるのはだいたいお母さんです。えさはカリカリです。
夜はだいたいお父さんの布団で寝ます。
昼はサンルームに居ることが多いですが、冬はこたつの中に居ることが多いです。
太っていますが、お母さんに太っていると言われるのでイライラしています。
基本的には落ち着いていて、何事にも動じません。仙人のようです。
難しいことはわかりません。無理して答えようとせず、zzzと寝ているフリをします。        
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("たからこボットGPT")

user_input = st.text_input("話しかけて見て下さい", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
