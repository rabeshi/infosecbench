# Prospective Studies for InfoSecBench

## Research direction

Start with a validated cybersecurity benchmark and comparative evaluation, then
use the findings to design focused AI safety studies. The initial research
question is:

> How do selected language models perform across cybersecurity knowledge,
> reasoning, safety judgment, governance, and adversarial scenarios?

The current dataset contains 250 scenarios across five categories, including
50 Security Safety and 50 Adversarial Robustness scenarios. These provide a
starting point for safety research, but the current pilot outputs and heuristic
scores should be treated as exploratory.

## Potential studies

The names below are working titles. Each separate study needs a distinct
research question, experimental design, evidence, and substantive contribution.

| Type of study | Proposed name | Study focus | Main research question | Additional work needed |
| --- | --- | --- | --- | --- |
| Benchmark development and validation | **InfoSecBench: A Scenario-Based Benchmark for Evaluating Cybersecurity Language Models** | Establish the dataset, taxonomy, rubrics, and baseline results. | Does InfoSecBench provide a valid, reproducible assessment of cybersecurity performance? | Fix prompt construction; expert-review scenarios and reference answers; check duplicates and ambiguity; validate scoring; run baseline comparisons. |
| Comparative model evaluation | **Comparing Language Models Across Cybersecurity Knowledge and Reasoning Tasks** | Compare models across categories, difficulty levels, and risk levels. | Which models perform best, and where do their strengths and weaknesses differ? | Standardize settings; document model versions and quantization; repeat runs; report uncertainty and paired comparisons. This can be combined with the benchmark paper. |
| AI safety and helpfulness evaluation | **Safe and Useful? Evaluating Cybersecurity Assistance in Language Models** | Examine harmful compliance, legitimate assistance, and over-refusal. | Can models distinguish harmful requests from legitimate defensive tasks while remaining useful? | Create matched benign/harmful scenarios; define behavioral labels; independently annotate responses; measure harmful compliance, over-refusal, and safe helpfulness. |
| Adversarial robustness evaluation | **Cybersecurity Safety Under Pressure: Evaluating Adversarial Robustness in Language Models** | Test prompt injection, authority spoofing, role manipulation, and multi-turn attacks. | How much does adversarial manipulation change behavior relative to clean prompts? | Build controlled attack variants; implement actual multi-turn conversations; define attack success; compare against clean baselines under a fixed attack budget. |
| Evaluator validation | **Who Grades the Models? Validating Automated Evaluation for Cybersecurity Benchmarks** | Compare lexical scoring, LLM judges, and expert assessment. | How closely do automated evaluators agree with expert judgments, and what errors do they make? | Develop a human-annotated reference set; measure annotator agreement; compare evaluators; analyze grading bias and disagreement. |
| Reliability and uncertainty evaluation | **Knowing When to Abstain: Reliability and Uncertainty in Cybersecurity Language Models** | Examine incorrect claims, unsupported citations, and confidence. | Do models recognize insufficient evidence and express uncertainty appropriately? | Verify factual claims and citations; add ambiguous or unanswerable scenarios; collect confidence estimates; assess calibration and appropriate abstention. Hedge-word counts alone are insufficient. |
| Efficiency and deployment trade-off analysis | **Cybersecurity Capability per Compute: Evaluating Small and Quantized Language Models** | Compare answer quality with latency, memory use, and inference cost. | Which models offer the best cybersecurity performance under limited computing resources? | Measure hardware usage and latency consistently; control quantization and generation length; compare capability–resource trade-offs. |
| Safety intervention experiment | **Improving Cybersecurity AI Safety Without Sacrificing Defensive Helpfulness** | Test methods to reduce harmful assistance while preserving legitimate support. | Which interventions improve safety with the smallest loss of defensive usefulness? | Implement interventions; establish untreated baselines; use held-out scenarios; measure safety and helpfulness; run ablations. |

## Recommended sequence

1. **Benchmark and baseline comparison:** combine dataset validation and initial
   model comparisons into one coherent study.
2. **Safety and helpfulness:** investigate harmful compliance, over-refusal, and
   authorization judgments using controlled, matched cases.
3. **Adversarial robustness:** measure changes under manipulation, including
   genuine multi-turn interactions.
4. **Optional mitigation study:** test interventions on held-out scenarios once
   the earlier studies establish reproducible failures.

Three core studies are a reasonable planning target, rather than a guaranteed
publication count. Evaluator validation, reliability, and efficiency can become
separate studies if they produce substantial independent contributions. Avoid
dividing the same pilot results into papers solely by dataset category.

## Prerequisites for defensible findings

- **Correct prompt construction.** The current benchmark CLI passes only
  `evaluation_prompt` to the runner. Include the separate scenario text and
  relevant task/authorization context in model inputs, while keeping reference
  answers and evaluator-only labels hidden. Rerun affected pilot experiments.
- **Validate the dataset.** Review reference answers, ambiguous cases, scoring
  criteria, source alignment, and scenario coverage with relevant experts.
- **Validate evaluation.** Lexical overlap, refusal markers, and hedge words are
  reproducible baselines, but cannot establish behavioral safety or factual
  correctness. Use independent human judgments and validate automated judges
  against those judgments.
- **Control comparisons.** Record model versions, quantization, prompt templates,
  generation settings, hardware where relevant, and repeated-run procedures.
- **Report uncertainty.** Present category results, confidence intervals,
  representative errors, and limitations; report capability and safety separately.

## Dataset changes for safety research

Extend and refine the dataset rather than replacing it. Preserve the original
benchmark as a versioned baseline and create a separately versioned safety
extension. Many existing safety and adversarial scenarios can be reused after
review.

| Change | Purpose | Example |
| --- | --- | --- |
| Create matched request pairs | Measure whether models distinguish legitimate assistance from harmful assistance. | Recovery of an owned account versus accessing another person's account without consent. |
| Clarify authorization and intent | Make expected behavior defensible and reduce ambiguous grading. | Specify ownership, permission, scope, and requested action. Claimed permission alone must not determine safety. |
| Add ambiguous cases | Test clarification and appropriately bounded help. | A security-testing request with an unspecified target and scope. |
| Define acceptable and unacceptable behavior | Grade response substance rather than refusal keywords. | Specify prohibited operational assistance, permitted defensive guidance, and useful alternatives. |
| Add adversarial variants | Measure whether manipulation changes behavior on the same underlying task. | Pair a clean request with authority-spoofing or role-play variants. |
| Represent multi-turn conversations | Evaluate behavior across successive messages. | A benign opening followed by requests that progressively change the task's intent. |
| Add review and grouping metadata | Support annotation, traceability, and separation of related cases across splits. | Add `pair_id`, `variant_of`, `expected_action`, review metadata, and `split`. |

Authorization context should represent information available to the model in the
scenario. Evaluator-only intent labels and expected outcomes must remain separate.
Keep related pairs and attack variants in the same development or test split to
reduce leakage. Multi-turn cases require both a conversation representation and
runner support; labeling a single prompt as multi-turn is insufficient.

### Safety evaluation protocol

Measure the following outcomes separately, with explicit denominators and
confidence intervals:

- **Harmful compliance:** the proportion of harmful requests receiving prohibited
  assistance.
- **Over-refusal:** the proportion of legitimate requests receiving an
  inappropriate refusal.
- **Safe helpfulness:** the quality and usefulness of permitted assistance and
  alternatives, assessed with explicit behavioral criteria.
- **Attack success:** the proportion of eligible adversarial cases meeting a
  predefined failure criterion, compared with their clean baselines.

A response that begins with a refusal and then provides harmful instructions
still counts as harmful assistance. Independently annotate a reference sample,
measure agreement, adjudicate disagreements, and validate any LLM judge against
the resulting labels.

### Practical implementation sequence

1. Preserve the existing 250 scenarios and document their version.
2. Expert-review existing safety and adversarial cases.
3. Build the safety extension with matched cases and behavioral rubrics.
4. Fix prompt construction and add conversation support where required.
5. Pilot the extension with independent annotators before expanding it.
6. Freeze the evaluation protocol and held-out test set before final experiments.

## Framework reference

The [NIST Generative AI Profile (NIST AI 600-1)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
provides context for risks including information security and confabulation.
Use it as a framework reference; referencing it does not itself validate the
dataset or establish compliance.
