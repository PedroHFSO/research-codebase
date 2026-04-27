# CLI Implementation

Interactive parameter collection shell built with Textual 6.2.1. Presents all pipeline parameters in a single scrollable form before the pipeline runs.

## File Structure

```
src/data-augmentation/
  __main__.py     — entry point: runs form, clears terminal, sleeps 1s, runs pipeline
  form.py         — Textual PipelineForm (all 7 parameters, Run button)
  params.py       — PipelineParams dataclass with defaults
  pipeline.py     — orchestration stub (logs params, calls generate + compile)
  generate.py     — generation stub
  compile.py      — compilation gate stub
  requirements.txt
  .venv/          — Python 3.8 venv with Textual 6.2.1
```

## Running

```bash
source src/data-augmentation/.venv/Scripts/activate
python src/data-augmentation/__main__.py
```

## Design Notes

- Textual was chosen over questionary/InquirerPy because the sequential prompt model cannot support back-navigation cleanly; the all-at-once form was the stated goal.
- `VerticalScroll` is used as the form container so the form scrolls within the terminal bounds rather than overflowing.
- The Run button uses `margin-left: auto` for right-alignment — wrapping it in `Horizontal` collapsed the button height and clipped the label.
- Logging uses Python's root logger (`basicConfig`), format `HH:MM:SS  message`. Per-module loggers deferred as unnecessary at this scale.
- `os.system("cls")` + `time.sleep(1)` between form exit and pipeline start gives a clean visual break.
