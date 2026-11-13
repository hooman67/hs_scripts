"""Use the user's approved refreshed credentials through the frozen safe parser."""
import importlib.util
from pathlib import Path

BUCKET = "foundry-hp-enterprise-adobe-assets"


def s3_client(bucket=BUCKET):
    if bucket != BUCKET:
        raise ValueError("this task is scoped to the HP bucket")
    prior = Path(__file__).resolve().parent.parent / "hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/report.py"
    spec = importlib.util.spec_from_file_location("prior_safe_s3_parser", prior)
    report = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(report)
    return report.s3_client(Path("/mnt/localssd/temp_creds.txt"))
