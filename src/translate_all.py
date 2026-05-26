#!/usr/bin/env python3
"""Translate every untranslated paragraph in Chapters 1–5 via `pi`.

Strategy:
- Iterate over all paragraphs (and subheadings, continuations) where zh is empty.
- Call pi with deepseek-v4-pro and the HK Catholic terminology prompt.
- Run N translations in parallel (default 4).
- After each completion, write the updated JSON back to disk so progress is preserved.
- Skip already-translated entries (resumable).
"""
import json, subprocess, time, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "data" / "encyclical.json"
PROMPT_PATH = ROOT / "src" / "translate_prompt.md"

PI_MODEL = "opencode-go/deepseek-v4-pro"
THINKING = "off"
TIMEOUT = 180
PARALLEL = int(os.environ.get("PARALLEL", "4"))

def translate_one(text: str) -> str:
    """Shell out to pi. Returns translated text or raises."""
    proc = subprocess.run(
        [
            "pi", "-p",
            "--no-session", "--no-tools", "--no-skills",
            "--model", PI_MODEL,
            "--thinking", THINKING,
            "--append-system-prompt", str(PROMPT_PATH),
            text,
        ],
        capture_output=True, text=True, timeout=TIMEOUT
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pi failed (exit {proc.returncode}): {proc.stderr[:500]}")
    out = proc.stdout.strip()
    # Strip any stray markdown wrappers the model might emit
    if out.startswith("```"):
        out = "\n".join(out.split("\n")[1:-1] if out.endswith("```") else out.split("\n")[1:])
    return out.strip()

def normalize(text: str) -> str:
    """Normalize the Chinese output to consistent traditional form."""
    # 着/著 - both are valid in traditional Chinese; keep model output as-is.
    # Just ensure no stray prefixes.
    for prefix in ("Translation:", "中文：", "翻譯：", "中文译文：", "Chinese:"):
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    return text

def collect_jobs(doc):
    """Yield (section_idx, block_idx, kind, source_text)."""
    jobs = []
    for s_idx, s in enumerate(doc["sections"]):
        # Skip Introduction and Conclusion (already done) and any block already translated
        if s["en_label"] in ("INTRODUCTION", "CONCLUSION"):
            continue
        if s["en_label"] not in ("CHAPTER ONE", "CHAPTER TWO", "CHAPTER THREE", "CHAPTER FOUR", "CHAPTER FIVE"):
            continue
        for b_idx, blk in enumerate(s["blocks"]):
            t = blk.get("type")
            if t == "paragraph":
                if blk.get("zh") and blk["zh"].strip():
                    continue
                # Source includes paragraph number for context
                src = f"{blk['num']}. {blk['en']}"
                jobs.append((s_idx, b_idx, "paragraph", src))
            elif t == "subheading":
                if blk.get("zh") and blk["zh"].strip():
                    continue
                jobs.append((s_idx, b_idx, "subheading", blk["en"]))
            elif t == "continuation":
                if blk.get("zh") and blk["zh"].strip():
                    continue
                jobs.append((s_idx, b_idx, "continuation", blk["en"]))
    return jobs

def main():
    doc = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    jobs = collect_jobs(doc)
    if not jobs:
        print("Nothing to translate. All paragraphs done.")
        return 0
    print(f"Translating {len(jobs)} blocks with parallelism={PARALLEL}, model={PI_MODEL}")
    start = time.time()
    done = 0
    fail = 0

    # Save with a lock-free approach: only the main thread writes; workers just return results
    lock = __import__("threading").Lock()
    def worker(job):
        s_idx, b_idx, kind, src = job
        try:
            zh = translate_one(src)
            zh = normalize(zh)
            # For paragraphs, the model often echoes "N. " prefix - strip if leading paragraph number matches the source
            if kind == "paragraph":
                import re
                zh = re.sub(r'^\d{1,3}\.?\s*', '', zh)
            return (s_idx, b_idx, kind, zh, None)
        except Exception as e:
            return (s_idx, b_idx, kind, None, str(e))

    with ThreadPoolExecutor(max_workers=PARALLEL) as ex:
        futures = {ex.submit(worker, j): j for j in jobs}
        for f in as_completed(futures):
            s_idx, b_idx, kind, zh, err = f.result()
            j = futures[f]
            preview = (j[3][:60] + "…") if len(j[3]) > 60 else j[3]
            if err:
                fail += 1
                print(f"  ✗ [{s_idx}/{b_idx}] {kind}: {err[:120]}", flush=True)
                continue
            done += 1
            # Update in-memory doc and persist
            with lock:
                doc["sections"][s_idx]["blocks"][b_idx]["zh"] = zh
                JSON_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            elapsed = time.time() - start
            rate = done / elapsed if elapsed > 0 else 0
            remaining = (len(jobs) - done - fail) / rate if rate > 0 else 0
            print(f"  ✓ [{s_idx}/{b_idx}] {kind} ({done}/{len(jobs)}, eta {remaining:.0f}s): {zh[:80]}…", flush=True)

    print(f"\nDone. {done} succeeded, {fail} failed. Elapsed: {time.time()-start:.1f}s")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main())
