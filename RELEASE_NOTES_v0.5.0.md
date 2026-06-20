# Attention Algebra v0.5.0

Layer 3 is now a **Spectrogram Reader** — the pipeline maps algebraic math
equivalences onto a cognitive spectrum instead of emitting RL/PyTorch agent
code.

## Highlights

- **New `attention_algebra.spectrum` module.** `SpectrogramReader` synthesises
  a mixed signal from the Mathematical Schedule: each Jungian terminal
  occupies a carrier frequency band; schedule logic modulates amplitude
  envelopes; the result is rendered as a time–frequency spectrogram with
  terminal band annotations and occupancy strip.
- **Deterministic Layer 3.** No LLM call for the final layer — faster,
  reproducible, and independent of the `capo` dependency.
- **Gradio UI updated.** Layer 3 pane shows the spectrogram image plus a
  markdown spectrum reading (dominant bands, carrier table, fold energy).
- **Removed `code.py` / `CodeGenerator`.** Replaced by `SpectrogramReader`
  and `SpectrumResult` in the public API.

## Carrier frequency table

| Terminal | Hz    |
| :------: | ----: |
| Se       | 82.4  |
| Si       | 110.0 |
| Ne       | 164.8 |
| Ni       | 220.0 |
| Te       | 293.7 |
| Ti       | 392.0 |
| Fe       | 493.9 |
| Fi       | 587.3 |

## Dependencies

- Added `numpy`, `scipy`, `matplotlib`, `Pillow` to `requirements.txt`.

## Migration

```python
# Before (v0.4)
from attention_algebra import CodeGenerator
code = CodeGenerator().generate_code(schedule)

# After (v0.5)
from attention_algebra import SpectrogramReader
image, report = SpectrogramReader().read(schedule)
```