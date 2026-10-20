from flask import Flask, redirect, render_template, request, url_for
import sqlite3
app = Flask(__name__)
DB_NAME = "database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS urls"
            " (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT NOT NULL)"
        )
    conn.commit()

def encode_base62(num):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if num == 0:
        return chars[0]
    encoded = []
    while num > 0:
        encoded.append(chars[num % 62])
        num //= 62
    return "".join(reversed(encoded))

def decode_base62(chars_str):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    num = 0
    for char in chars_str:
      num = num * 62 + chars.index(char)
    return num

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        long_url = request.form["long_url"]
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (long_url) VALUES (?)", (long_url,))
            url_id = cursor.lastrowid
            conn.commit()
        short_key = encode_base62(url_id)
        short_url = request.host_url + short_key
    return render_template("index.html", short_url=short_url)

@app.route("/<short_key>")
def redirect_to_url(short_key):
  try:
    url_id = decode_base62(short_key)
    with sqlite3.connect(DB_NAME) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT long_url FROM urls WHERE id = ?", (url_id,))
      row = cursor.fetchone()

      if row:
        # HTTP 302 Temporary Redirect for analytics tracking
        return redirect(row[0], code=302)
  except Exception:
    pass

  return "URL not found", 404

if __name__ == "__main__":
  init_db()
  app.run(debug=True)