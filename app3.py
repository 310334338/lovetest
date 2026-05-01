from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


# ⭐ PythonAnywhere 需要的關鍵（很重要）
application = app

# ===============================
# 使用者設定名字
# ===============================
name_all = input("她的全名，如果想用預設請輸入9: ")
if name_all == "9":
    name_all = "劉知珉"
    name = "Karina"
else:
    name = input("她的暱稱(你平常怎麼叫她): ")

print(f"\n好的，現在已經設定完成，接下來準備開始測驗。\n")

# ===============================
# 題庫
# ===============================
QUESTIONS = {
    # 選擇題
    "Q1_choice": {
        "text": f"{name}突然問你：「前女友漂亮，還是我漂亮？」",
        "options": {
            "A": "當然是你好看啦～你眼睛比她大，腿比她好看100倍",
            "B": "前女友？她哪位？我不記得了",
            "C": "你比她可愛",
            "D": "傻瓜，你是我的第一任女友啊"
        },
        "answer": "D",
        "type": "choice"
    },
    "Q2_choice": {
        "text": f"某天你們吵架了，{name}一氣之下叫你走，你會怎麼做？",
        "options": {
            "A": "先離開，等到她冷靜一點再聯絡她",
            "B": "和她好好溝通，搞清楚到底是哪裡出錯了",
            "C": "立刻抱住她，說我錯了，我愛你～",
            "D": "帥氣又瀟灑的，頭也不回，走人！"
        },
        "answer": "C",
        "type": "choice"
    },

    # 簡答題
    "Q1_1": {
        "text": f"1-1\n走在街上的時候，你突然鬆開{name}的手，低頭滑起手機。\n{name}停下腳步，有些不高興地問：「你在幹嘛？」\n你抬頭回：「我在查一下我們等下要去的餐廳在哪裡啊！」\n{name}沉默了幾秒，語氣有點冷：「喔。」\n她真正感到不快的原因是?",
        "ideal_answer": "因為我放開了牽著她的手",
        "required_concepts": [["牽", "手"], ["放", "鬆","開"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q2_1": {
        "text": f"2-1\n你買了兩個造型髮箍，一個戴在自己頭上，另一個直接往{name}頭上一戴，開心地說：「嘿嘿~我們一組的～\n{name}卻皺起眉、轉過頭不理你。\n她生氣的真正原因是?",
        "ideal_answer": "因為我直接把髮箍帶到她頭上弄亂精心設計的髮型",
        "required_concepts": [["髮箍"], ["弄亂", "頭","頭髮"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q2_2": {
        "text": f"2-2\n你說要幫{name}買食物，轉身就去買了，留下{name}一個人繼續排隊。{name}見狀皺起眉，心情明顯不好。\n她真正生氣的原因是?",
        "ideal_answer": "因為我直接走掉所以她覺得孤獨",
        "required_concepts": [["走掉","丟下"], ["孤獨"], ["一個人","她"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q2_3": {
        "text": f"2-3\n{name}拿了自己的飲料，笑著遞給你：「你想喝一口嗎？」\n你接過後，用手擦了擦吸管，然後喝了一口:「還不錯!」\n{name}愣了一下，表情微微變化。\n她真正感到不悅的原因是?",
        "ideal_answer": "因為我擦吸管代表嫌棄她的口水",
        "required_concepts": [["吸管"], ["口水"], ["嫌", "棄"],["擦"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q3_1": {
        "text": f"3-1\n你一看到前方的女生，立刻揮手喊道：\n「{name_all}！嗨～～在這裡！」\n{name}愣了一下，尷尬地笑笑：「啊…嗨。」\n接著，她的表情有些不太自然。\n她感到不自在的真正原因是?",
        "ideal_answer": "因為我叫她全名",
        "required_concepts": [["全名"], ["叫"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q3_2": {
        "text": f"3-2\n你吃完最後一口，笑著問{name}：「欸，你吃完了嗎？」\n{name}還在慢慢嚼著食物，抬頭看你，眉頭微微皺起：「還沒呢…」\n她真正不開心的原因是?",
        "ideal_answer": "因為我沒有耐心等她吃飯",
        "required_concepts": [["等"], ["吃飯"], ["耐心"],["催"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q4_1": {
        "text": f"4-1\n走在回家的路上，{name}輕聲說：「天色晚了，有點冷耶…」\n你緊握她的手，催促道：「快點回家吧，別站太久！」\n{name}微微停下腳步，嘆了口氣，臉上帶著一絲不高興。\n她真正生氣的原因是?",
        "ideal_answer": "因為我沒有挽留",
        "required_concepts": [["直接","沒有留戀","毅然決然","依依不捨"],["挽留"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q4_2": {
        "text": f"4-2\n{name}看著你，認真地問：「你愛我嗎？」\n你愣了一下，然後回答：「我…真的非常非常喜歡你。」\n{name}臉色微微變了，沉默了幾秒，語氣有些生氣。\n她真正生氣的原因是?",
        "ideal_answer": "因為我沒有說愛她",
        "required_concepts": [["愛"], ["沒有說"],["喜歡"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q4_3": {
        "text": f"4-3\n你說：「你先走啦。」\n{name}笑著回：「不，你先走啦！」\n你正氣凜然地轉頭就走，{name}站在原地，眉頭微皺，神情有些不悅。\n她真正生氣的原因是?",
        "ideal_answer": "因為我沒有轉頭留戀直接走掉",
        "required_concepts": [["轉頭","轉身"], ["走掉"], ["留戀","毅然決然"]],
        "neg_sensitive": False,
        "type": "short_answer"
    },
    "Q_bonus": {
        "text": f"魔王題:(為加分題，不適用於先前句型，請自由發揮)\n{name}有天問你「你是因為漂亮才喜歡我，還是因為喜歡我才覺得我漂亮?」，你應該如何回答?\n",
        "ideal_answer": "喜歡跟漂亮本來是不同的事，但遇見你那一刻，他們就同時出現在我的心裡了",
        "required_concepts": [["喜歡"], ["漂亮"]],
        "neg_sensitive": False,
        "type": "short_answer"
    }
}

# ===============================
# 評語字典
# ===============================
FEEDBACK_DICT = {
    "90": [
        {"short": "哇，你幾乎抓到她所有的小心思，生氣的原因你幾乎猜得出來！",
         "long": "你就像她的小心情雷達，能感受到細微波動。偶爾她還是會調皮考驗你，但這只會讓你們的互動更甜蜜。記得偶爾給她小驚喜，讓她知道你不只懂她，也願意用心維護你們的關係。"},
        {"short": "你簡直是她的小情緒偵探，連隱藏的原因都能察覺！",
         "long": "你總能捕捉到她的微妙情緒，讓她覺得被理解。偶爾出現的小錯誤也沒關係，因為真誠比完美重要。保持這份敏感和幽默，你們之間的默契會越來越深。"},
        {"short": "幾乎每次你都猜對，她會覺得你真是心有靈犀！",
         "long": "這種準確度讓她心裡甜滋滋，但也提醒你，偶爾放鬆一點，讓互動更自然。愛情不只是解碼，還要享受過程中的小驚喜和小笑料，這會讓你們的關係更輕鬆愉快。"}
    ],
    "80": [
        {"short": "你大部分時間能猜到她的心思，偶爾小迷糊也無妨。",
         "long": "你對她的情緒敏感，能理解她的感受，但偶爾還會出現小錯誤。沒關係，這讓你們的互動更真實，也有趣味。多留心觀察，你會越來越得心應手。"},
        {"short": "你的直覺大多準確，只是偶爾需要一點再確認。",
         "long": "你已經能捕捉她的暗示和表情，但有時候還是會猜錯。這正是互動的樂趣——即使偶爾錯誤，也能讓她看到你用心的努力。慢慢來，你會更自信地理解她。"},
        {"short": "她的小情緒你幾乎能讀懂，偶爾錯一點也不影響甜蜜。",
         "long": "你已經在愛情中表現得很細心，能察覺她的需求。偶爾的錯誤反而讓你們的互動更生動。保持耐心和幽默，你會發現猜測她的心情其實也可以是一種樂趣。"}
    ],
    "60": [
        {"short": "你有時能猜到她的心思，但也常讓她覺得你心不在焉。",
         "long": "愛情就像解謎，你抓到部分線索，另一半還需要慢慢探索。多花時間觀察她的表情和語氣，你會發現自己其實能理解她更多。別急，關係慢慢磨合也是樂趣之一。"},
        {"short": "偶爾對，她也會偶爾覺得你迷糊。",
         "long": "你的努力是顯而易見的，只是有時候還不夠精準。沒關係，這是互動的一部分，也讓你們之間有點小火花。多聽多觀察，你會越來越懂她。"},
        {"short": "抓到一半正確答案，另一半可能還在摸索。",
         "long": "你對她的情緒已經開始敏感，但還需要一些經驗和觀察。小錯誤不影響你們的關係，重要的是你願意花心思理解她。慢慢累積，你會發現這些小嘗試讓你更靠近她的心。"}
    ],
    "40": [
        {"short": "嗯……她生氣的原因你大概只抓到一半吧？",
         "long": "別緊張，猜錯很正常。重要的是你有心去理解她，並願意改進。每一次錯誤都是學習的機會，也讓你慢慢建立起對她的敏感度。耐心一點，愛情需要時間，也需要你慢慢摸索。"},
        {"short": "你可能還需要多觀察，她的小脾氣不是那麼容易猜。",
         "long": "有時候她的情緒比表面更複雜，你可能會抓不全。但這正好給你機會練習細心和耐心。多聽、多問，慢慢你會發現她的小秘密，其實比你想像更有趣。"},
        {"short": "猜錯次數有點多，但至少你願意嘗試。",
         "long": "有心嘗試本身就值得肯定。雖然你還不完全懂她的心思，但每一次互動都能讓你累積經驗。放輕鬆，不要急，慢慢你會發現愛情的過程比結果更精彩。"}
    ],
    "0": [
        {"short": "欸……你猜錯的次數可能比正確的還多耶。",
         "long": "沒關係，這正是互動的樂趣。重點不是猜對多少次，而是你願意關心她的情緒。先從觀察和傾聽開始，慢慢你會學到更多，也會更自然地理解她的感受。"},
        {"short": "這次可能全錯，但至少你還願意嘗試。",
         "long": "愛情不是考試，猜對與否不重要。重要的是你在過程中投入心思，願意了解她的想法。慢慢來，累積小成功，你會發現自己逐漸變得更敏感，也更懂她的心。"},
        {"short": "完全猜錯也沒關係，畢竟你還在學習中。",
         "long": "每一次錯誤都是學習的契機，不必灰心。觀察她的表情、語氣、動作，慢慢你會抓到更多線索。耐心和好奇心才是你最好的工具，愛情會在你準備好時悄悄降臨。"}
    ]
}

# ===============================
# 計算評語
# ===============================
def get_feedback(score):
    if score >= 90:
        choices = FEEDBACK_DICT["90"]
    elif score >= 80:
        choices = FEEDBACK_DICT["80"]
    elif score >= 60:
        choices = FEEDBACK_DICT["60"]
    elif score >= 40:
        choices = FEEDBACK_DICT["40"]
    else:
        choices = FEEDBACK_DICT["0"]
    return random.choice(choices)

# ===============================
# 首頁
# ===============================
@app.route("/")
def home():
    return render_template("index.html")

# ===============================
# 簡答題評分（偽AI）
# ===============================
def score_short_answer(user_answer, qdata):
    if not user_answer:
        return 0, "未作答"

    score = 0
    total = len(qdata["required_concepts"])

    for group in qdata["required_concepts"]:
        if any(word in user_answer for word in group):
            score += 1

    final_score = (score / total) * 10

    return final_score, f"命中 {score}/{total} 個關鍵概念"

# ===============================
# 題目頁
# ===============================
@app.route("/question", methods=["GET", "POST"])
def question():
    feedback = None
    score = None

    if request.method == "POST":
        # 這裡放計分程式
        score_total = 0
        for qid, qdata in QUESTIONS.items():
            user_answer = request.form.get(qid)
            if qdata["type"] == "choice":
                if user_answer == qdata["answer"]:
                    score_total += 5
            elif qdata["type"] == "short_answer":
                score, msg = score_short_answer(user_answer, qdata)
                score_total += round(score)
        feedback = get_feedback(score_total)

        return redirect(url_for("result", score=score_total, short=feedback["short"], long=feedback["long"]))

    return render_template("question.html", questions=QUESTIONS)

# ===============================
# 結果頁
# ===============================
@app.route("/result")
def result():
    score = request.args.get("score")
    short = request.args.get("short")
    long = request.args.get("long")

    return render_template("result.html", score=score, short=short, long=long)

if __name__ == "__main__":
    app.run(debug=True)