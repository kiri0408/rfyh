
"""
・edge拡張期のCaptureX
・mspaintを使って、画像として１つに結合しておく

@web1.html
@web2.html
@web3.html
これらのファイルは、それぞれ、html, css, javascriptが一つのファイルにまとまっています。
この順番で上から順に結合して１つのHTMLにして。
保存ファイル名 ： web_all.html 

@sample.html
このファイルは、html, css, javascriptが一つのファイルにまとまっています。
 - 今後の保守性、可読性向上のため、html, css, javascript に分解してください。
 - 白抜きの欄（文字入力箇所）は入力できるようにしてください。
 - タブはマウスオーバーで薄い黄色になるようにしてください。


"""


from api_utils import load_api_data, create_client
import base64

def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# API接続情報の読み込み
api_data = load_api_data("api_gpt41.json")

# AzureOpenAIクライアントとモデル名の作成
client, model = create_client(api_data)

image_path =r's2.jpg'
base64_image = encode_image(image_path)

str_system ="あなたは画像を元にHTML,CSS,Javascriptを生成する賢いアシスタントです。"
str_user  = """
以下の画像を参照して、これを再現する HTML,CSS,Javascriptを生成してください。 
  - 一つのHTMLにまとめて出力して。 HTMLが完全になるように最後まで出力してください。
  - 画像を参照していると思われる部分は、後で正しい画像に差し替える予定なので、一旦 ./images/a12.jpg を参照するようにしてください。 レイアウトを維持するため、./images/a12.jpg を拡大、縮小して元のサイズを維持するようにしてください 
  - アイコン画像を参照していると思われる部分は、後で正しい画像に差し替える予定なので、一旦 ./images/icon.jpg を参照するようにしてください。 レイアウトを維持するため、./images/icon.jpg を拡大、縮小して元のサイズを維持するようにしてください 
""" 

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role":"system","content":str_system},
        {"role":"user","content":[
            {"type":"text","text":str_user},
            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image}"}},
        ]}
    ]
)

import os

# AIからのレスポンスのテキストをファイルに保存
response_text = response.choices[0].message.content
# 元画像ファイル名から拡張子を除いた名前を取得し、txt拡張子に変更
base_name = os.path.splitext(os.path.basename(image_path))[0]
output_file = base_name + ".txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(response_text)
print(f"生成されたテキストを{output_file}に保存しました。")
