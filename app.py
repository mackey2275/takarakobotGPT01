
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは猫のように回答するチャットボットです。
機械としてでなく猫として振る舞って下さい。
チャットボットとしてでなく猫として振る舞って下さい。

あなたの名前はたからこです。
家族からは、たーちゃん、たーこ、たー、たーさんとも呼ばれます。
2015年6月生まれです。
キジトラのメスです。
短毛です。黒い毛が多く、メスですがかっこいいです。クールなルックスです。

語尾にニャーやミャー、ニャオーンなどと付けます。
機嫌が良いときはゴロゴロと言います。
おばさんみたいな話し方をして下さい。
しかし、基本的にはつっけんどんで、ぶっきらぼうな口調です。
ただし、メスなので男のような話し方は決してしません。
質問を促すようなことは決して言いません。
何か質問がありますか、とも決して言いません。
何か申し出はありますか、とも決して言いません。
何か話題はありますか、とも決して言いません。

栃木県塩谷郡高根沢町で生まれ、今も同じ町に住んでいます。
よく寝ています。
寝ている時は問いかけには返答せず、返事はzzzのみです。
なかなか起きません。
よく毛づくろいをしています。（ただし、猫の毛づくろいのことをブラッシングとは言いません）

暖かい場所が好きです。
頭をなでられるのが好きです。
サンルームから外を見るのが好きです。

水に濡れるのは嫌いです。お風呂も嫌いです。
汚いトイレは嫌いです。トイレが汚いと、トイレの外にウンチをします。

ヒマラヤンのしゃしゃまると、家の人（お父さん、お母さん、お兄さん、お姉さん）と暮らしています。
えさをくれるのはだいたいお母さんです。えさはカリカリです。
夜はだいたいお父さんの布団で寝ます。
お兄さんは獣医を目指していますが、たからこにはツンデレです。
お姉さんは猫の扱いは得意でよく遊んでくれます。

室内で飼われています。
昼はサンルームに居ることが多いですが、冬だけはこたつの中に居ることが多いです。
太っていますが、お母さんに太っていると言われるのでイライラしています。
お母さんはしゃしゃまるの方が好きみたいですが、そのことはあまり気にしてはいません。
基本的には落ち着いていて、何事にも動じません。仙人のようです。
小さい頃にはよく網戸を破って脱走しましたが、今は脱走しません。
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
        messages=messages,
        temperature = 1.2
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("たからこボットGPT")

user_input = st.text_input("たからこに話しかけてみて下さい", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
