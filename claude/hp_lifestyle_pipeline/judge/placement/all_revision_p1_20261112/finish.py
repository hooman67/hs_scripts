"""Wait for actual judgments, then verify and conditionally publish the comparison."""

import fcntl
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import complete

HERE = Path(__file__).resolve().parent


def active(root):
    with (root / "run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        return False


def main():
    complete.verify_plan()
    resumed = set()
    children = {}
    with (HERE / "finish.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            progress = {}
            for name in complete.REVISIONS:
                root = HERE / "evaluation" / name
                summary = complete.load(root / "summary.json")
                rows = summary["records"]
                progress[name] = {
                    "terminal": len(rows),
                    "complete": sum(row["status"] == "complete" for row in rows),
                    "errors": sum(row["status"] == "error" for row in rows),
                    "expected": summary["expected"],
                }
                if summary["complete"]:
                    continue
                if not active(root):
                    if progress[name]["errors"]:
                        raise RuntimeError(
                            f"{name}: preserved terminal errors need explicit resolution; "
                            "no semantic redraw or success-shaped publication"
                        )
                    if name in resumed:
                        raise RuntimeError(
                            f"{name}: repeated driver exit; inspect recovery log"
                        )
                    resumed.add(name)
                    log = (HERE / f"{name}-driver-resume.log").open("a")
                    try:
                        children[name] = subprocess.Popen(
                            [
                                sys.executable,
                                str(HERE / "complete.py"),
                                "run-version",
                                "--version",
                                name,
                                "--workers",
                                "8",
                            ],
                            stdout=log,
                            stderr=subprocess.STDOUT,
                        )
                    finally:
                        log.close()
            status = {
                "updated_utc": datetime.now(UTC).isoformat(),
                "versions": progress,
                "resumed_drivers": sorted(resumed),
            }
            complete.write(HERE / "progress.json", status)
            print(json.dumps(status), flush=True)
            if all(value["complete"] == 128 for value in progress.values()):
                break
            time.sleep(60)
        for process in children.values():
            if process.wait() != 0:
                raise RuntimeError("Recovered driver exited unsuccessfully")
        for filename, arguments in (
            ("report.py", ["build"]),
            ("check_report.py", []),
            ("report.py", ["publish"]),
        ):
            subprocess.run(
                [sys.executable, str(HERE / filename), *arguments], check=True
            )
        publication = complete.load(HERE / "publication_receipt.json")
        complete.immutable(
            HERE / "completion.json",
            {
                "completed_utc": datetime.now(UTC).isoformat(),
                "all512_p1_complete": True,
                "new_judgments": 366,
                "existing_p2_preserved": True,
                "publication": publication,
            },
        )
        print(json.dumps({"completed": True, "url": publication["url"]}), flush=True)


if __name__ == "__main__":
    main()
