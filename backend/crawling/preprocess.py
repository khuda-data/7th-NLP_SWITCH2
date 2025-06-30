

from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Remove scripts, styles, and other non-visible elements
    for tag in soup(['script', 'style', 'noscript', 'header', 'footer', 'svg', 'img', 'meta', 'link']):
        tag.decompose()

    # Get visible text
    text = soup.get_text(separator=' ', strip=True)

    # Normalize whitespace
    cleaned_text = ' '.join(text.split())

    return cleaned_text

if __name__ == '__main__':
    html_path = 'body_cleaned.html'  # Change path if needed
    text = extract_text_from_html(html_path)
    # print(text)
    with open("cleaned_text.txt", "w", encoding="utf-8") as f_out:
        f_out.write(text)