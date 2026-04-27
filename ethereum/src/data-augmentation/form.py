from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Label, Static
from textual.containers import VerticalScroll

from params import PipelineParams


class PipelineForm(App):
    CSS = """
    Screen {
        align: center top;
    }

    #form {
        width: 60;
        height: 100%;
        padding: 1 2;
        border: round $primary;
    }

    .section-header {
        text-style: bold;
        margin-top: 1;
        margin-bottom: 0;
        color: $accent;
    }

    .field-label {
        margin-top: 1;
    }

    #run {
        margin-top: 1;
        margin-bottom: 2;
        margin-left: 1;
    }
    """

    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        defaults = PipelineParams()
        with VerticalScroll(id="form"):
            yield Static("Pipeline Configuration", classes="section-header")

            yield Static("Seed Sampling", classes="section-header")

            yield Label("Few-shot k", classes="field-label")
            yield Input(value=str(defaults.few_shot_k), id="few_shot_k")

            yield Label("Random seed", classes="field-label")
            yield Input(value=str(defaults.random_seed), id="random_seed")

            yield Static("Generation", classes="section-header")

            yield Label("Model", classes="field-label")
            yield Input(value=defaults.model, id="model")

            yield Label("Temperature", classes="field-label")
            yield Input(value=str(defaults.temperature), id="temperature")

            yield Label("Top-p", classes="field-label")
            yield Input(value=str(defaults.top_p), id="top_p")

            yield Label("Top-k", classes="field-label")
            yield Input(value=str(defaults.top_k), id="top_k")

            yield Label("Samples (n)", classes="field-label")
            yield Input(value=str(defaults.n_samples), id="n_samples")

            yield Label("Max tokens", classes="field-label")
            yield Input(value=str(defaults.max_tokens), id="max_tokens")

            yield Button(label="Run", variant="primary", id="run")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            self.exit(self._collect_params())

    def _collect_params(self) -> PipelineParams:
        def get(field_id: str) -> str:
            return self.query_one(f"#{field_id}", Input).value

        return PipelineParams(
            few_shot_k=int(get("few_shot_k")),
            random_seed=int(get("random_seed")),
            model=get("model"),
            temperature=float(get("temperature")),
            top_p=float(get("top_p")),
            top_k=int(get("top_k")),
            n_samples=int(get("n_samples")),
            max_tokens=int(get("max_tokens")),
        )
