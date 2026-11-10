"""
ATS Analyzer — Scores resume vs job description.

Algorithm:
  1. Tokenize both texts into keyword sets.
  2. Apply TF-IDF weighting to find important terms.
  3. Compute coverage ratio = (matched keywords) / (total job keywords)
  4. Score = coverage_ratio * 100 (0-100 ATS score)
"""

import re
from collections import Counter
from typing import NamedTuple
import math


class AnalysisResult(NamedTuple):
    score: float                # 0.0 - 100.0
    matched_keywords: list[str]
    missing_keywords: list[str]
    strengths: list[str]
    recommendations: list[str]


def tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, return meaningful words (3+ chars)."""
    text = text.lower()
    tokens = re.findall(r"\b[a-z][a-z0-9+#.-]{2,}\b", text)
    stopwords = {
        "the", "and", "for", "with", "that", "this", "are", "you",
        "will", "have", "our", "your", "from", "been", "not", "but",
        "can", "all", "also", "its", "their", "work", "able"
    }
    return [t for t in tokens if t not in stopwords]


def compute_tfidf(doc_tokens: list[str], corpus_tokens: list[str]) -> dict[str, float]:
    """Compute TF-IDF scores to identify the most important terms in a document."""
    tf = Counter(doc_tokens)
    total = len(doc_tokens) or 1
    df = Counter(corpus_tokens)
    corpus_size = 2  # resume + job description

    scores = {}
    for term, count in tf.items():
        tf_score = count / total
        # Add 1 smoothing to prevent log(0)
        idf_score = math.log(corpus_size / (1 + df[term])) + 1
        scores[term] = tf_score * idf_score
    return scores


def analyze(resume_text: str, job_description: str, top_n: int = 30) -> AnalysisResult:
    """
    Main analysis function.

    Args:
        resume_text:     Plain text extracted from your resume PDF/DOCX.
        job_description: Plain text of the job posting.
        top_n:           Number of most important job keywords to evaluate.

    Returns:
        AnalysisResult with score, gaps, strengths, and recommendations.
    """
    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)
    corpus = resume_tokens + job_tokens

    job_tfidf = compute_tfidf(job_tokens, corpus)
    # Pick the top-N most important job keywords
    top_keywords = sorted(job_tfidf.keys(), key=lambda k: job_tfidf[k], reverse=True)[:top_n]

    resume_set = set(resume_tokens)
    matched = [kw for kw in top_keywords if kw in resume_set]
    missing = [kw for kw in top_keywords if kw not in resume_set]

    score = round((len(matched) / max(len(top_keywords), 1)) * 100, 1)

    strengths = matched[:8]
    recommendations = [
        f"Add '{kw}' — appears {job_tokens.count(kw)} time(s) in the job description"
        for kw in missing[:5]
    ]

    return AnalysisResult(
        score=score,
        matched_keywords=matched,
        missing_keywords=missing,
        strengths=strengths,
        recommendations=recommendations,
    )
