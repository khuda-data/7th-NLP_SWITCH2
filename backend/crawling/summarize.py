

from konlpy.tag import Okt
import re

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_relevant_sentences(text):
    keywords = ["대회", "공모전", "참가", "제출", "심사", "수상", "시상", "평가", "우승"]
    sentences = re.split(r'[.!?。\n]', text)
    return [s.strip() for s in sentences if any(k in s for k in keywords)]

def extract_keywords(sentences):
    okt = Okt()
    text = " ".join(sentences)
    korean_nouns = okt.nouns(text)
    english_words = re.findall(r'\b[a-zA-Z]{2,}\b', text)
    keywords = set(word.lower() for word in korean_nouns + english_words if len(word) > 1)
    return sorted(keywords)

if __name__ == "__main__":
    text = load_text("cleaned_text.txt")
    relevant_sentences = extract_relevant_sentences(text)
    
    print("📌 대회 관련 요약 문장:")
    for s in relevant_sentences:
        print("-", s)

    print("\n🔑 추출된 핵심 키워드:")
    keywords = extract_keywords(relevant_sentences)
    print(", ".join(keywords))