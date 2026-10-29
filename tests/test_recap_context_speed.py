import re
import threading
import time

from app.pipeline.recap_formula import STORY_CONTEXT_KEYS, build_story_context


class FakeRewriter:
    def __init__(self):
        self.lock = threading.Lock()
        self.active = 0
        self.peak_active = 0
        self.prompts = []

    def _generate_json(self, prompt, model_order):
        with self.lock:
            self.prompts.append(prompt)
            self.active += 1
            self.peak_active = max(self.peak_active, self.active)
        try:
            time.sleep(0.03)
            match = re.search(r"SOURCE CHUNK (\d+)/(\d+):", prompt)
            if match:
                number = int(match.group(1))
                return {
                    **{key: [] for key in STORY_CONTEXT_KEYS},
                    "characters": [f"character-from-chunk-{number}"],
                    "plot_state": [f"plot-from-chunk-{number}"],
                }
            return {
                **{key: [] for key in STORY_CONTEXT_KEYS},
                "characters": ["character-from-chunk-1", "character-from-chunk-2"],
                "plot_state": ["plot-from-chunk-1", "plot-from-chunk-2"],
            }
        finally:
            with self.lock:
                self.active -= 1


def test_context_chunks_are_merged_in_source_order():
    rw = FakeRewriter()
    units = [
        {"id": i, "timestamp": "00:00.00-00:01.00", "source_text": f"source sentence {i}"}
        for i in range(1, 42)
    ]

    result = build_story_context(rw, units, ["mock-model"], lambda *_: None)

    assert result["characters"] == ["character-from-chunk-1", "character-from-chunk-2"]
    assert result["plot_state"] == ["plot-from-chunk-1", "plot-from-chunk-2"]
    assert len(rw.prompts) == 3  # two parallel extractions plus one consolidation
    assert rw.peak_active >= 2
