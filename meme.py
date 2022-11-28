from flask import Flask, render_template
import requests
import json

app = Flask(__name__)


def get_meme():
    # тут можно выбрать категорию реддита
    reddit_cat = "Pikabu" #  "Pikabu", "memes", "ComedyCemetery", "MemeEconomy", "AdviceAnimals", "dankmemes"
    url = f"http://meme-api.herokuapp.com/gimme/{reddit_cat}"
    response = json.loads(requests.request("GET", url).text)
    meme_large = response["preview"][-2]
    subreddit = response["subreddit"]
    return meme_large, subreddit


@app.route("/")
def index():
    meme_pic,subreddit = get_meme()
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)


if __name__ == '__main__':
    app.run(debug=True)