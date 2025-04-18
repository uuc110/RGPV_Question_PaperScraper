import json
from typing import Dict, List, DefaultDict
import matplotlib.pyplot as plt  # type: ignore
from collections import defaultdict
import re

# Load data
with open('Paper.json') as f:
    question_bank = json.load(f)['questionbank']['Information Security']

with open('syllabusStructure.json') as f:
    syllabus = json.load(f)['SubjectMapper']

# Preprocess syllabus topics
chapter_keywords = {int(k): [re.sub(r'\W+', ' ', topic.lower()) for topic in v] 
                   for k, v in syllabus.items()}
# Track frequency
chapter_counts: DefaultDict[int, int] = defaultdict(int)
question_frequency: DefaultDict[str, int] = defaultdict(int)
question_frequency = defaultdict(int)

# Analyze questions
for year, chapters in question_bank.items():
    for chap_num, questions in chapters.items():
        chap_num = int(chap_num)
        keywords = chapter_keywords.get(chap_num, [])
        
        for question in questions:
            # Preprocess question
            clean_q = re.sub(r'\W+', ' ', question.lower())
            q_words = set(clean_q.split())
            
            # Count keyword matches
            matches = sum(1 for kw in keywords 
                         if any(kw_word in q_words for kw_word in kw.split()))
            
            if matches > 0:
                chapter_counts[chap_num] += 1
                question_frequency[question] += 1

# Sort results
sorted_chapters = sorted(chapter_counts.items(), key=lambda x: x[1], reverse=True)
sorted_questions = sorted(question_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
# Plot chapter frequency
plt.figure(figsize=(12, 6))
plt.bar([f'Ch {chap}' for chap, _ in sorted_chapters], [count for _, count in sorted_chapters])
plt.title('Chapter-wise Question Frequency')
plt.title('Chapter-wise Question Frequency')
plt.xlabel('Chapters')
plt.ylabel('Number of Questions')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Print top questions
print("\nTop 10 Most Frequent Questions:")
for i, (q, count) in enumerate(sorted_questions, 1):
    print(f"{i}. {q} (Appeared {count} times)")

# Print chapter summary
print("\nChapter Frequency Summary:")
for chap, count in sorted_chapters:
    print(f"Chapter {chap}: {count} questions")