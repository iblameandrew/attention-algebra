# Attention Algebra — A Cognitive Grammar for Language

> A formal grammar that lifts natural language into a higher-dimensional
> space of *functional constituents*, and compiles the result into
> cognitive spectrograms that read a speaker's functional state like a
> sound reads on a spectrum.

<img width="1173" height="642" alt="image" src="https://github.com/user-attachments/assets/4e0e3068-5e69-47bd-a4b9-0a6e894ab56d" />


## The Idea

Every sentence a person or a model produces is a *projection* of a
high-dimensional cognitive state down to a 1-D string of tokens. The
projection is lossy: two sentences that look nothing alike can be
driven by the same internal state, and a single sentence can be the
shadow of many overlapping states.

**Attention Algebra** is a *grammar* for the inverse projection. Given a piece
of natural language, it parses the string into an expression in a
small formal language whose terminals are the eight irreducible
*functional constituents* of cognition and whose operators describe
how those constituents interact. The expression is then compiled,
layer by layer, into a mathematical schedule and finally into a
**cognitive spectrogram** — a time–frequency image of the speaker's
functional state.

In one sentence:

> *Attention Algebra is a type system and compiler for language, where the
> types are the eight Jungian functions and the compiled artefact is a
> spectrogram that maps algebraic math equivalences onto a readable
> cognitive spectrum.*

The pipeline lifts language into spectral form:

```
  string  ───parse───▶  ⟨algebra⟩  ───compose───▶  ⟨schedule⟩  ───read───▶  ⟨spectrogram⟩
       (Layer 1)            (Layer 2)                       (Layer 3)
```

---

## Why a Grammar?

A grammar is the right abstraction for three reasons:

1. **Compositionality.** A grammar's production rules are *the same
   no matter how deep you nest*. A clause in a clause in a clause is
   parsed by the same rule that parses a clause. This is exactly the
   property we need: a sentence can have arbitrarily many layers of
   motivation, conflict, and rationalisation, and we want a single
   parser to handle all of them.
2. **Type safety.** Each terminal of the grammar is tagged with its
   *domain* (Perception vs. Judgment) and its *attitude*
   (Extraverted vs. Introverted). The operators (`~`, `oo`, `→`, `|`,
   `+`) are partial functions that are only well-typed on certain
   combinations. The parser will reject `Se ~ Si` (same domain,
   different attitude — not a legal orbit) and accept `(Ne ~ Ti)`.
3. **Realisability.** Every well-typed expression has a *canonical
   mathematical image*: a sum of weighted objective functions whose
   scheduling dynamics follow directly from the operator. The reader
   in Layer 3 is total: every parseable expression renders to a
   spectrogram.

The grammar is tiny — eight terminals, fifteen operators (five
sequential, eight RNA-inspired, two grouping forms), and two numeric
attributes — but it spans the cognitive space densely because the
operators let you weave the terminals into molecules of arbitrary
complexity, including long-range secondary structure.

---

## The Grammar

### Terminals — the eight functional constituents

| Symbol | Name                    | Domain     | Attitude      |
| :----: | :---------------------- | :--------- | :------------ |
|  `Se`  | Extraverted Sensing     | Perception | Extraverted   |
|  `Si`  | Introverted Sensing     | Perception | Introverted   |
|  `Ne`  | Extraverted Intuition   | Perception | Extraverted   |
|  `Ni`  | Introverted Intuition   | Perception | Introverted   |
|  `Te`  | Extraverted Thinking    | Judgment   | Extraverted   |
|  `Ti`  | Introverted Thinking    | Judgment   | Introverted   |
|  `Fe`  | Extraverted Feeling     | Judgment   | Extraverted   |
|  `Fi`  | Introverted Feeling     | Judgment   | Introverted   |

The terminals are the *functional constituents* of the title: a
minimal, complete, and orthogonal basis for the cognitive space. No
terminal can be expressed as a combination of the others.

### Numeric attributes

Every terminal may be preceded by a bare integer that names its
**mass** (intensity, 1–10), e.g. `7Se`. A parenthesised group may
itself be preceded by a bare integer that names its **acceleration**
(frequency, any positive real), e.g. `40(Ti)`.

```
mass       ::=  [1-9][0-9]?    attached to a terminal
accel      ::=  [1-9][0-9]*    attached to a parenthesised expression
```

### Sequential operators

| Symbol | Name           | Semantics                                                                 | Schedule logic        |
| :----: | :------------- | :------------------------------------------------------------------------ | :-------------------- |
| `~`    | Orbit          | One Perception + one Judgment structure each other.                       | Orbital               |
| `oo`   | Opposition     | Same domain, opposite attitude; winner drags to opposite sub-axis.        | Adversarial           |
| `->`   | Drag           | RHS of Opposition only; single function, not a group.                      | Drag                  |
| `\|`   | Axis Switch    | Same domain, different sub-axis (S↔N or T↔F) alternation.                | Stochastic switching  |
| `+`    | Domain Switch  | Perception ↔ Judgment alternation (when operands cross domains).          | Domain switching      |
| `&`    | Conjunction    | Linear sum of independent functions.                                      | Linear                |
| `( )`  | Grouping       | Override precedence, nest molecules.                                    | —                     |

### RNA-inspired secondary-structure operators

| Symbol     | Name                  | Semantics                                      | Schedule logic          |
| :--------: | :-------------------- | :--------------------------------------------- | :---------------------- |
| `::`       | Stem Pair             | Long-range complementary binding with loop.    | Cooperative Binding     |
| `^`        | Hairpin               | Self-referential feedback fold.                | Feedback Loop           |
| `.`        | Bulge                 | Stem with one partial mismatch.                | Partial Adversarial     |
| `@`        | Pseudoknot            | Crossing non-nested pair constraints.          | Crossing Constraints    |
| `*`        | Junction              | Multi-way branch (3+ drives).                  | Softmax Junction        |
| `=`        | Stacking              | Adjacent stems reinforce (γ=1.5).              | Amplified Binding       |
| `fold[]`   | MFE Fold              | Global minimum free-energy structure.          | Global Equilibrium      |
| `>>`       | Co-transcriptional    | Left-to-right sequential commitment.           | Sequential Commitment   |

**Complementarity table** (for `::` stems):

* **Regime A (attitude):** `Se::Si`, `Ne::Ni`, `Te::Ti`, `Fe::Fi`
* **Regime B (cross-axis):** `Se::Ni`, `Si::Ne`, `Te::Fi`, `Ti::Fe`

Dot-bracket sugar: `5Ne(((3Ti)))4Fe` ≡ stem `Ne::Fe` with loop `Ti`.

### Well-typedness

* `~` requires one Perception and one Judgment terminal (either order).
* `oo` requires same domain and opposite attitude; always emits `->`
  flipping sub-axis (S↔N, T↔F) while preserving winner attitude.
* `->` is not free-standing; RHS must be a single terminal.
* `|` requires same domain, different sub-axis.
* `+` as domain switch requires Perception + Judgment operands.
* `::` requires complementary terminals under Regime A or B.
* `@` requires crossing (non-nested) stem pairings.

Grammar rules live in [`attention_algebra/algebra.py`](attention_algebra/algebra.py)
(prompt-embedded).  Programmatic validation is in
[`attention_algebra/parser.py`](attention_algebra/parser.py).

### Worked examples

| Natural language                                                              | Parse                                             |
| :----------------------------------------------------------------------------- | :------------------------------------------------ |
| "A slow, heavy realisation."                                                  | `5(Ni)`                                            |
| "Racing thoughts over and over."                                              | `50(Ti)`                                           |
| "Exploring ideas to build a system."                                          | `(Ne ~ Ti)`                                        |
| "I explore impulsively but feel held back by past regrets."                    | `7Se oo 3Si -> Ni`                                 |
| "A deep internal value conflict slowly forces me to organise my environment." | `10((Fi oo Fe) -> Te) ~ Si`                        |
| "A million racing possibilities tethered to social harmony."                  | `fold[100(Ne(((Ti)))Fe)]`                          |
| "I keep replaying the same imagined outcome."                                 | `^(5Ni)`                                           |
| "Mostly at peace with the group, one thing nags."                             | `6Fi :: . :: 5Fe`                                  |
| "Everything hits me at once."                                                 | `5Se * 4Ne * 6Fe * 3Ti`                            |

---

## The Functional Space

The eight terminals are not just labels. Each one names a direction in
a four-dimensional functional space, and the cognitive state of an
agent is a *vector* in that space. The grammar is the surface syntax
of that vector algebra:

| Dimension         | Axis 0     | Axis 1     | Basis elements       |
| :---------------- | :--------- | :--------- | :------------------- |
| **Domain**        | Perception | Judgment   | `S`/`N` vs. `T`/`F`  |
| **Attitude**      | Introvert  | Extravert  | `i` vs. `e` suffix   |
| **Mass**          | —          | —          | bare integer prefix  |
| **Acceleration**  | —          | —          | integer group prefix |

The four dimensions are independent, so the space is ℝ⁸ with two
auxiliary real axes for mass and acceleration per terminal. A sentence
like

> "I am torn between the part of me that wants to explore and the
> part that wants to hold on to the familiar, but the pull toward
> harmony keeps dragging me back."

parses to a single point in that space; a paragraph parses to a
*trajectory*; a conversation parses to a *flow*. The Attention Algebra
compiler is a differentiable readout of that flow.

---

## Model Providers

All three layers call an LLM through the **OpenAI SDK** (via
`langchain-openai`).  Two OpenAI-compatible backends are supported:

| Provider | When to use | Required config |
| :------- | :---------- | :-------------- |
| **OpenRouter** | Cloud models (Gemini, Claude, Qwen, Llama, …) | `OPENROUTER_API_KEY` |
| **llama.cpp** | Local inference with `llama-server` | `LLAMA_CPP_BASE_URL`, `LLAMA_CPP_MODEL` |

Pass `provider="openrouter"` or `provider="llama.cpp"` to each layer
class.  The Gradio UI exposes the same choice as a radio button.

---

## The Three Layers

The grammar is realised by a strict, three-stage compiler. Each layer
is a pure function of the previous layer's output, and the layers
themselves are language-model calls constrained by an explicit
production rule. You can swap any layer for your own implementation as
long as it respects the input/output contract.

### Layer 1 — The Algebraic Analyst (`attention_algebra.algebra`)

* **Input:** natural language.
* **Process:** an LLM, prompted with the grammar reference, produces
  a single parse tree flattened to a string.
* **Output:** a *type-checked* expression in the grammar.

```python
from attention_algebra import AlgebraAnalyst
analyst = AlgebraAnalyst(
    model_name="google/gemini-2.5-flash",
    provider="openrouter",
)
expr = analyst.analyze("I am torn between exploration and holding on.")
# '7Ne oo 3Si -> Fe'
```

### Layer 2 — The Harmonic Composer (`attention_algebra.composition`)

* **Input:** a grammar expression.
* **Process:** an LLM, prompted with the function-to-objective table
  below, emits a JSON *Mathematical Schedule* describing the loss
  landscape.
* **Output:** a JSON object with `schedule_logic`, `score`, and
  `math_narrative`.

The canonical mapping from terminal to optimisation objective:

| Terminal | Objective class        | Math (LaTeX)                       | Interpretation                       |
| :------: | :--------------------- | :--------------------------------- | :----------------------------------- |
| `Se`     | `ExplorationObjective` | $\mathcal{H}(\pi(a\mid s))$         | Maximise policy entropy.             |
| `Si`     | `GatheringObjective`   | $e^{-\lVert s-\mu\rVert}$            | Cluster around the centroid.         |
| `Ne`     | `ExtrapolationObjective` | $e^{\lVert s-\mu\rVert}$           | Seek novel states.                   |
| `Ni`     | `InterpolationObjective` | $\text{proj}_{\vec v}(s)$          | Follow an imagined trajectory.       |
| `Te`     | `ExploitationObjective` | $\mathbb{E}[V(s)]$                  | Maximise value.                      |
| `Ti`     | `ContrastObjective`    | $\lvert d(s,a)-d(s,b)\rvert$         | Maximise discrimination.             |
| `Fe`     | `IntegrationObjective` | $\mathcal{H} + \alpha V(s)$         | Balance exploration and value.       |
| `Fi`     | `SelectionObjective`   | $e^{-d(s, s_{t-1})}$                | Stay consistent with the past.       |

```python
from attention_algebra import Composer
composer = Composer(
    model_name="google/gemini-2.5-flash",
    provider="openrouter",
)
schedule = composer.compose("7Ne oo 3Si -> Fe")
# {'schedule_logic': 'Adversarial',
#  'global_frequency': 1.0,
#  'score': [{'voice': '...', 'symbol': 'ExtrapolationObjective', ...}, ...],
#  'math_narrative': '...'}
```

### Layer 3 — The Spectrogram Reader (`attention_algebra.spectrum`)

* **Input:** the Mathematical Schedule.
* **Process:** deterministic synthesis — each Jungian terminal maps to a
  carrier frequency; schedule logic modulates amplitude envelopes over
  time (`sin`/`cos` for Orbital, `exp(-λt)` for Drag, softmax for
  Junction, etc.); the mixed signal is rendered as a spectrogram with
  terminal band annotations.
* **Output:** a spectrogram image plus a spectrum reading report
  (dominant bands, carrier table, fold energy).

| Terminal | Carrier (Hz) | Spectral region |
| :------: | -----------: | :-------------- |
| `Se`     | 82.4         | Low perception  |
| `Si`     | 110.0        | Low perception  |
| `Ne`     | 164.8        | Mid perception  |
| `Ni`     | 220.0        | Mid perception  |
| `Te`     | 293.7        | Mid judgment    |
| `Ti`     | 392.0        | Mid judgment    |
| `Fe`     | 493.9        | High judgment   |
| `Fi`     | 587.3        | High judgment   |

```python
from attention_algebra import SpectrogramReader

reader = SpectrogramReader()
image, report = reader.read(schedule)
# image: numpy RGB array; report: markdown spectrum reading
```

---

## Installation

### Prerequisites

* Python 3.10 or newer
* An LLM backend — pick one:
  * **[OpenRouter](https://openrouter.ai/)** — easiest path; one API key
    gives access to Gemini, Claude, Qwen, Llama, and other models.
  * **[llama.cpp](https://github.com/ggerganov/llama.cpp) server** — run
    models locally via the OpenAI-compatible endpoint:

    ```bash
    llama-server -m model.gguf --port 8080
    ```

### Install

```bash
git clone https://github.com/iblameandrew/attention-algebra.git
cd attention-algebra
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root (or export the variables in
your shell):

```bash
# OpenRouter (cloud)
echo 'OPENROUTER_API_KEY=your_api_key_here' > .env

# llama.cpp server (local) — optional overrides
# LLAMA_CPP_BASE_URL=http://127.0.0.1:8080/v1
# LLAMA_CPP_MODEL=local
# LLAMA_CPP_API_KEY=no-key
```

---

## Usage

### Interactive UI

```bash
python app.py
```

This launches a three-pane Gradio interface. Type a sentence in
*Context*, choose **OpenRouter** or **llama.cpp (Local)**, enter a model slug,
click *Analyze*, and watch the algebra, the math schedule, and the
cognitive spectrogram appear in order.

### Programmatic

```python
import os
from attention_algebra import AlgebraAnalyst, Composer, SpectrogramReader

os.environ.setdefault("OPENROUTER_API_KEY", "...")
model = "google/gemini-2.5-flash"

# Layer 1: parse.
algebra = AlgebraAnalyst(model_name=model, provider="openrouter").analyze(
    "I explore impulsively but feel held back by past regrets."
)

# Layer 2: compose.
schedule = Composer(model_name=model, provider="openrouter").compose(algebra)

# Layer 3: spectrogram.
image, report = SpectrogramReader().read(schedule)
```

### Local llama.cpp

```python
import os

os.environ["LLAMA_CPP_BASE_URL"] = "http://127.0.0.1:8080/v1"
os.environ["LLAMA_CPP_MODEL"] = "local"  # must match the loaded model

algebra = AlgebraAnalyst(model_name="local", provider="llama.cpp").analyze(
    "Racing thoughts over and over."
)
```

---

## Repository Layout

```
attention-algebra/
├── assets/                # README banner image
├── app.py                 # Gradio front-end
├── attention_algebra/
│   ├── algebra.py         # Layer 1 — the grammar + the analyst
│   ├── composition.py     # Layer 2 — the harmonic composer
│   ├── spectrum.py        # Layer 3 — the spectrogram reader
│   ├── parser.py          # Programmatic grammar validation
│   ├── config.py          # Model factory (OpenRouter / llama.cpp)
│   ├── utils.py           # strip_think_tags, strip_code_fences
│   └── __init__.py
├── requirements.txt
└── README.md
```

---

## Roadmap to AGI

We use the grammar as an *evaluation instrument*. A model that can
parse into, reason over, and emit from all eight terminals in all
five operator configurations is by construction manipulating the
same functional constituents a human does. Coupled with a target
distribution over parse trees (derived empirically from a corpus of
human reasoning traces), the grammar lets us define a *cognitive
completeness* criterion for AGI that is independent of any particular
benchmark: a model is generally intelligent iff its distribution
over grammar expressions matches the human distribution under KL
divergence below a threshold.

In the meantime, Attention Algebra is a tool for *diagnosing* what a model is
doing. Drop a chain-of-thought trace in, get the grammar expression
out, and read the cognitive state of the model the way a spectrogram
reads a sound.

---

## License

MIT. See [`LICENSE`](LICENSE).
