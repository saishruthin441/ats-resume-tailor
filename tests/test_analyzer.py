"""
Unit Tests for ATS Analyzer
"""

from ats_tailor.analyzer import analyze, tokenize


def test_tokenize_basic():
    tokens = tokenize("Python developer with FastAPI and PostgreSQL experience")
    assert "python" in tokens
    assert "fastapi" in tokens
    assert "with" not in tokens  # stopword filtered


def test_tokenize_no_short_words():
    tokens = tokenize("AI is key to ML")
    # "is" and "to" are short/stopwords; "key" is 3 chars, should be included
    assert "is" not in tokens


def test_analyze_perfect_match():
    resume = "Python FastAPI PostgreSQL Docker Kubernetes REST APIs AWS"
    job = "Python FastAPI PostgreSQL Docker Kubernetes REST APIs AWS"
    result = analyze(resume, job)
    assert result.score >= 90.0


def test_analyze_zero_match():
    resume = "Microsoft Word Excel PowerPoint email communication"
    job = "Python FastAPI PostgreSQL pgvector embeddings"
    result = analyze(resume, job)
    assert result.score < 20.0
    assert len(result.missing_keywords) > 0


def test_analyze_partial_match():
    resume = "Python developer with REST API experience"
    job = "Python FastAPI PostgreSQL Docker AWS Kubernetes REST API microservices"
    result = analyze(resume, job)
    assert 0 < result.score < 100
    assert "fastapi" in result.missing_keywords or "postgresql" in result.missing_keywords


def test_recommendations_generated():
    resume = "HTML CSS JavaScript"
    job = "React TypeScript Next.js Tailwind CSS Node.js PostgreSQL"
    result = analyze(resume, job)
    assert len(result.recommendations) > 0
    assert any("react" in r.lower() or "typescript" in r.lower() for r in result.recommendations)
