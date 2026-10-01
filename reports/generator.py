import json
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def generate_report(
    benchmark_name,
    baseline,
    current,
    comparisons,
    triage,
    output_file
):

    template_dir = Path(
        "reports/templates"
    )

    environment = Environment(
        loader=FileSystemLoader(
            str(template_dir)
        )
    )

    template = environment.get_template(
        "report.html"
    )

    html = template.render(
        benchmark_name=benchmark_name,
        generated_at=datetime.now(),
        baseline=baseline,
        current=current,
        comparisons=comparisons,
        triage=triage
    )

    output_path = Path(
        output_file
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        html,
        encoding="utf-8"
    )

    return output_path