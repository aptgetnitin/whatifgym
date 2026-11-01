from pathlib import Path

from whatifgym.tasks import current_task_files


def test_superseded_files_and_paraphrases_are_left_out(tmp_path: Path):
    root = tmp_path / "tasks"
    for name in ("m/a_v0.jsonl", "m/a_v1.jsonl", "m/b_v0.jsonl", "m/b_v0_nl.jsonl"):
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text("")
    (root / "superseded.txt").write_text("# comment\ntasks/m/a_v0.jsonl   # replaced by a_v1\n\n")
    names = lambda files: [p.relative_to(root).as_posix() for p in files]
    assert names(current_task_files(root=root)) == ["m/a_v1.jsonl", "m/b_v0.jsonl", "m/b_v0_nl.jsonl"]
    assert names(current_task_files(paraphrases=False, root=root)) == ["m/a_v1.jsonl", "m/b_v0.jsonl"]
