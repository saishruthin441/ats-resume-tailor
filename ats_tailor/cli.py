"""
Typer CLI — user-facing commands for ATS analysis.

Usage:
  ats-tailor score --resume resume.pdf --job job.txt
  ats-tailor analyze --resume resume.pdf --job job.txt
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from ats_tailor.parser import extract_text
from ats_tailor.analyzer import analyze

app = typer.Typer(help="ATS Resume Tailor — optimize your resume for any job posting.")
console = Console()


@app.command()
def score(
    resume: Path = typer.Option(..., help="Path to your resume (.pdf or .docx)"),
    job: Path = typer.Option(..., help="Path to job description text file"),
):
    """Quick ATS score — returns a 0-100 match percentage."""
    with Progress(SpinnerColumn(), TextColumn("[bold blue]Analyzing..."), transient=True) as p:
        p.add_task("", total=None)
        resume_text = extract_text(resume)
        job_text = job.read_text(encoding="utf-8")
        result = analyze(resume_text, job_text)

    color = "green" if result.score >= 75 else "yellow" if result.score >= 50 else "red"
    console.print(Panel(
        f"[bold {color}]ATS Score: {result.score}/100[/bold {color}]\n"
        f"Matched {len(result.matched_keywords)} of {len(result.matched_keywords) + len(result.missing_keywords)} key terms",
        title="📊 Quick Score",
        border_style=color,
    ))


@app.command()
def analyze_cmd(
    resume: Path = typer.Option(..., "--resume", help="Resume file path"),
    job: Path = typer.Option(..., "--job", help="Job description file path"),
):
    """Full analysis: score, keyword gaps, and actionable recommendations."""
    resume_text = extract_text(resume)
    job_text = job.read_text(encoding="utf-8")
    result = analyze(resume_text, job_text)

    # Score panel
    color = "green" if result.score >= 75 else "yellow" if result.score >= 50 else "red"
    console.print(Panel(f"[bold {color}]{result.score}/100[/bold {color}]", title="ATS Score"))

    # Gaps table
    table = Table(title="Keyword Analysis", show_lines=True)
    table.add_column("Status", style="bold")
    table.add_column("Keyword")
    for kw in result.matched_keywords[:8]:
        table.add_row("✅ Present", kw)
    for kw in result.missing_keywords[:8]:
        table.add_row("❌ Missing", kw)
    console.print(table)

    # Recommendations
    if result.recommendations:
        console.print("\n[bold yellow]💡 Recommendations:[/bold yellow]")
        for rec in result.recommendations:
            console.print(f"  • {rec}")


if __name__ == "__main__":
    app()
