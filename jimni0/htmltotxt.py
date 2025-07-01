import os
from bs4 import BeautifulSoup

html_dir = "wevity_html"
txt_dir = "wevity_txt"
os.makedirs(txt_dir, exist_ok=True)

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        html_path = os.path.join(html_dir, filename)
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text(separator="\n")

        txt_filename = filename.replace(".html", ".txt")
        txt_path = os.path.join(txt_dir, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)