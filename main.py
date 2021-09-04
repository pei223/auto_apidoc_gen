# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from app.parser.parser import parse
from app.writer.api_entpoint import gen_api_endpoint

if __name__ == "__main__":
    text_ls = [
        "店舗情報を取得する",
        "店舗情報の一覧を取得する",
        "店舗情報一覧を取得する",
        "お気に入り登録する",
        "予約状態を更新する",
        "予約状態を確定する",
        "店舗情報を検索する",
        "お気に入り削除する"
    ]

    for text in text_ls:
        entity, api_type = parse(text)
        endpoint = gen_api_endpoint(entity, api_type, True)
        print(text, end="           ->         ")
        print(endpoint, api_type.method_type().value)

    # nltk.download('punkt')
    # nltk.download('wordnet')
    # print(nltk.word_tokenize("reserve confirmation"))
    # print(WordNetLemmatizer().lemmatize("reserve"))
