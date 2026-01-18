# app/utils/sentiment.py

"""
Advanced Sentiment Analysis Utility
"""

from __future__ import annotations
import re
from typing import Dict, Tuple
from collections import Counter
print("=== SENTIMENT MODULE STARTED ===")

print("sentiment.py loaded")

class SentimentAnalyzer:
    """Advanced sentiment analyzer with toxicity detection"""

    def __init__(self):
        self.positive_words = {
            'love', 'awesome', 'great', 'excellent', 'amazing', 'wonderful',
            'fantastic', 'perfect', 'beautiful', 'brilliant', 'outstanding',
            'superb', 'terrific', 'incredible', 'good', 'happy', 'joy',
            'excited', 'best', 'nice', 'lovely', 'pleased', 'grateful',
            'thankful', 'blessed', 'delighted', 'thrilled', 'enjoy',
            'celebrate', 'success', 'win', 'victory', 'achieve', 'proud'
        }

        self.negative_words = {
            'hate', 'bad', 'terrible', 'awful', 'horrible', 'worst',
            'angry', 'sad', 'disappointed', 'sick', 'disgusting', 'evil',
            'stupid', 'useless', 'pathetic', 'disgusted', 'annoyed',
            'frustrated', 'upset', 'miserable', 'failure', 'lose', 'lost',
            'wrong', 'problem', 'issue', 'difficult', 'hard', 'struggle',
            'pain', 'hurt', 'broken', 'failed', 'poor', 'weak'
        }

        self.toxic_words = {
            'kill', 'death', 'die', 'violence', 'attack', 'abuse',
            'racist', 'sexist', 'harassment', 'threat', 'assault',
            'scam', 'fraud', 'illegal', 'weapon', 'bomb', 'terrorist',
            'extremist', 'radical', 'murder', 'rape', 'torture'
        }

        self.very_toxic_patterns = [
            r'\b(kill\s+yourself|kys)\b',
            r'\b(commit\s+suicide)\b',
            r'\b(hate\s+speech)\b',
            r'\b(death\s+threat)\b'
        ]

        self.negation_words = {
            'not', 'no', 'never', 'neither', 'nobody', 'nothing',
            'none', 'nowhere', "don't", "doesn't", "didn't", "won't",
            "wouldn't", "can't", "couldn't", "shouldn't"
        }

        self.intensifiers = {
            'very', 'extremely', 'absolutely', 'really', 'totally',
            'completely', 'utterly', 'highly', 'so', 'super'
        }

        self.emoji_sentiment = {
            '😊': 0.8, '😃': 0.9, '😄': 0.9, '😁': 0.8, '🙂': 0.7,
            '❤️': 0.9, '💕': 0.9, '💖': 0.9, '💗': 0.9, '🥰': 0.9,
            '😍': 0.95, '🤩': 0.9, '✨': 0.7, '🌟': 0.7, '⭐': 0.7,
            '👍': 0.7, '👏': 0.8, '🎉': 0.8, '🎊': 0.8, '🚀': 0.8,
            '😢': -0.8, '😭': -0.9, '😞': -0.7, '😔': -0.7, '☹️': -0.7,
            '😠': -0.9, '😡': -0.95, '🤬': -1.0, '😤': -0.8, '💔': -0.9,
            '👎': -0.7, '🤮': -0.9, '😑': -0.5, '😐': 0.0, '😶': 0.0
        }

    def analyze(self, text: str) -> Dict:
        if not text or not text.strip():
            return self._neutral_result()

        text_lower = text.lower()
        words = self._tokenize(text_lower)

        sentiment_score = 0.0
        word_count = 0

        for i, word in enumerate(words):
            if len(word) < 2:
                continue

            word_count += 1
            is_negated = i > 0 and words[i-1] in self.negation_words
            is_intensified = i > 0 and words[i-1] in self.intensifiers
            intensity_multiplier = 1.5 if is_intensified else 1.0

            word_sentiment = 0.0
            if word in self.positive_words:
                word_sentiment = 0.15 * intensity_multiplier
            elif word in self.negative_words:
                word_sentiment = -0.15 * intensity_multiplier

            if is_negated:
                word_sentiment *= -1

            sentiment_score += word_sentiment

        emoji_score = self._analyze_emojis(text)
        sentiment_score += emoji_score

        exclamation_count = text.count('!')
        if exclamation_count > 0:
            sentiment_score += min(exclamation_count * 0.05, 0.2)

        if word_count > 0:
            sentiment_score = sentiment_score / max(1, word_count / 5)
        sentiment_score = max(-1.0, min(1.0, sentiment_score))

        if sentiment_score > 0.15:
            label = 'positive'
        elif sentiment_score < -0.15:
            label = 'negative'
        else:
            label = 'neutral'

        confidence = min(abs(sentiment_score) * 1.2, 1.0)
        toxicity_level, toxicity_score = self._detect_toxicity(text_lower, words)

        return {
            'label': label,
            'score': abs(sentiment_score),
            'confidence': confidence,
            'toxicity': toxicity_level,
            'toxicity_score': toxicity_score,
            'raw_score': sentiment_score
        }

    def _tokenize(self, text: str) -> list:
        # Safe tokenizer (Windows & Python 3.12 compatible)
        text = re.sub(r"[^\w\s]", " ", text)
        return text.split()

    def _analyze_emojis(self, text: str) -> float:
        score = 0.0
        for emoji, value in self.emoji_sentiment.items():
            count = text.count(emoji)
            score += value * count * 0.2
        return score

    def _detect_toxicity(self, text_lower: str, words: list) -> Tuple[str, float]:
        toxicity_score = 0.0

        for pattern in self.very_toxic_patterns:
            if re.search(pattern, text_lower):
                return 'high', 1.0

        toxic_count = sum(1 for word in words if word in self.toxic_words)

        if toxic_count > 0:
            toxicity_score = min(toxic_count * 0.25, 1.0)

            if toxicity_score >= 0.75:
                return 'high', toxicity_score
            elif toxicity_score >= 0.5:
                return 'medium', toxicity_score
            elif toxicity_score >= 0.25:
                return 'low', toxicity_score

        caps_ratio = sum(1 for c in text_lower if c.isupper()) / max(len(text_lower), 1)
        if caps_ratio > 0.6 and len(text_lower) > 10:
            toxicity_score = max(toxicity_score, 0.3)
            return 'low', toxicity_score

        return 'none', toxicity_score

    def _neutral_result(self) -> Dict:
        return {
            'label': 'neutral',
            'score': 0.0,
            'confidence': 0.0,
            'toxicity': 'none',
            'toxicity_score': 0.0,
            'raw_score': 0.0
        }

    def should_flag_for_moderation(self, analysis: Dict) -> bool:
        if analysis['toxicity'] in ['high', 'medium']:
            return True
        if analysis['label'] == 'negative' and analysis['confidence'] > 0.8:
            return True
        return False


sentiment_analyzer = SentimentAnalyzer()


def analyze_sentiment(text: str) -> Dict:
    return sentiment_analyzer.analyze(text)


def extract_hashtags(text: str) -> list:
    hashtags = re.findall(r'#(\w+)', text)
    return [tag.lower() for tag in hashtags]


def extract_mentions(text: str) -> list:
    mentions = re.findall(r'@(\w+)', text)
    return [mention.lower() for mention in mentions]

print("=== SENTIMENT MODULE FINISHED ===")
