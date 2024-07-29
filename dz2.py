import requests
import re
from collections import defaultdict
from functools import reduce
import matplotlib.pyplot as plt
import argparse

# Функція для завантаження тексту за URL
def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()  # Перевірка на помилки
    return response.text

# MapReduce функції
def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [(word, 1) for word in words]

def reduce_function(word_counts):
    reduced_counts = defaultdict(int)
    for word, count in word_counts:
        reduced_counts[word] += count
    return reduced_counts

def map_reduce(text):
    mapped = map_function(text)
    reduced = reduce_function(mapped)
    return reduced

# Функція для візуалізації топ слів
def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Words by Frequency')
    plt.xticks(rotation=45)
    plt.show()

# Головний блок коду
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and analyze text from a URL.')
    parser.add_argument('url', type=str, help='The URL of the text to analyze')
    args = parser.parse_args()

    url = args.url
    try:
        text = fetch_text(url)
        word_counts = map_reduce(text)
        visualize_top_words(word_counts)
    except requests.RequestException as e:
        print(f"Error fetching text: {e}")
