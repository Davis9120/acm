import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# OpenAI APIキーを設定
openai.api_key = 'your-api-key-here'

# 会話データ
conversation_data = [
    "ハロ：「ハローアムロ。ハローアムロ」",
    "アムロ：「ハロ、今日も元気だね」",
    "ハロ：「サンキュー、アムロ」",
    "フラウ：「何を着ていくつもり？アムロ？アムロ！？」",
    "アムロ：「このコンピューター組んだら食べるよ」",
    "フラウ：「避難命令聞いてなかったの？」",
    "アムロ：「避難命令？あのサイレンそうなの？」",
    "フラウ：「あきれたー、軍の放送聴かなかったの？軍艦が入港するから避難するんだってさ！」",
    "アムロ：「なんでー？」",
    "フラウ：「知らないわよ！」",
    "「アムロー！時間が無いのよ！」",
    "アムロ：「わかったよー・・・」",
    "避難を呼びかける人「退避急げー！」",
    "フラウ：「外で待ってるから。ハロ、いらっしゃい」",
    "アムロ：「うるさいなぁー」",
]

# データ分割
validation_data = conversation_data[:8]
test_data = conversation_data[8:]

# 性格パラメータ生成用モデル (ACM)
def generate_personality_parameters(conversation):
    questions = [
        "a. 活発で、外向的だと思う。",
        "b. 他人に不満をもち、もめ事を起こしやすいと思う。",
        "c. しっかりしていて、自分に厳しいと思う。",
        "d. 心配性で、うろたえやすいと思う。",
        "e. 新しいことが好きで、変わった考えを持つと思う。",
        "f. ひかえめで，おとなしいと思う。",
        "g. 人に気をつかう，やさしい人間だと思う。",
        "h. だらしなく，うっかりしていると思う。",
        "i. 冷静で，気分が安定していると思う。",
        "j. 発想力に欠けた，平凡な人間だと思う。",
    ]

    # API呼び出し
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a psychologist who assesses personality based on dialogue."},
            {"role": "user", "content": conversation},
        ] + [{"role": "user", "content": question} for question in questions]
    )
    
    answers = response['choices'][0]['message']['content'].split('\n')
    
    # TIPI-Jのスコア計算
    scores = {
        '外向性': (int(answers[0][-1]) + (8 - int(answers[5][-1]))) / 2,
        '協調性': ((8 - int(answers[1][-1])) + int(answers[6][-1])) / 2,
        '勤勉性': (int(answers[2][-1]) + (8 - int(answers[7][-1]))) / 2,
        '神経症傾向': (int(answers[3][-1]) + (8 - int(answers[8][-1]))) / 2,
        '開放性': (int(answers[4][-1]) + (8 - int(answers[9][-1]))) / 2,
    }
    
    return scores

# 対話モデル (CCM)
def generate_dialogue(personality_params, prompt):
    # 性格パラメータに基づくプロンプトを作成
    personality_prompt = f"""
    キャラクター：アムロ・レイ
    年齢：16歳
    外向性：{personality_params['外向性']}
    協調性：{personality_params['協調性']}
    勤勉性：{personality_params['勤勉性']}
    神経症傾向：{personality_params['神経症傾向']}
    開放性：{personality_params['開放性']}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that emulates the character Amuro Ray."},
            {"role": "user", "content": personality_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    dialogue = response['choices'][0]['message']['content']
    return dialogue

# 評価
def evaluate_similarity(test_data, generated_data):
    # ベクトル化
    test_vectors = [openai.Embedding.create(input=sentence, model="text-embedding-ada-002")['data'][0]['embedding'] for sentence in test_data]
    generated_vectors = [openai.Embedding.create(input=sentence, model="text-embedding-ada-002")['data'][0]['embedding'] for sentence in generated_data]
    
    # コサイン類似度
    similarities = [cosine_similarity([test_vector], [generated_vector])[0][0] for test_vector, generated_vector in zip(test_vectors, generated_vectors)]
    average_similarity = np.mean(similarities)
    
    return average_similarity

# 実行例
personality_params = generate_personality_parameters('\n'.join(validation_data))
generated_dialogue = [generate_dialogue(personality_params, prompt) for prompt in test_data]

similarity_score = evaluate_similarity(test_data, generated_dialogue)
print(f"Similarity Score: {similarity_score}")


