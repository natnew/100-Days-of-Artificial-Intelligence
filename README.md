# 100 Days of Artificial Intelligence


## 👋 Welcome

Welcome to **100 Days of Artificial Intelligence** — a hands-on journey through building AI systems that are safe, aligned, interpretable, and robust.

This isn't about adding safety as an afterthought. Each project treats **ethics, evaluation, and epistemic rigor as first-class system properties**, embedded from the start.

You'll progress from understanding how modern AI systems fail, to building agents with guardrails, to designing multi-agent architectures with traceable reasoning and observable behavior. By Day 100, you'll have practical experience building AI systems you can actually trust — and explain to others.

## 🧭 Philosophy

**Safety is not a constraint. It's a capability.**

The most useful AI systems are those we can verify, understand, and correct. This curriculum is built on four principles:

1. **Evaluation-first development** — Every project includes metrics and tests for safety properties
2. **Traceable reasoning** — Agents should show their work, not just their answers  
3. **Graceful failure** — Systems should fail safely, transparently, and recoverably
4. **Stakeholder legibility** — Build for auditability by both technical and non-technical reviewers

## 🗺️ Learning Map

The 100 days are organized into four phases, each building on the last:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: FOUNDATIONS (Days 1-25)                                       │
│  Understanding model behavior, failure modes, and evaluation basics     │
├─────────────────────────────────────────────────────────────────────────┤
│  PHASE 2: BUILDING SAFE AGENTS (Days 26-50)                            │
│  Tool use, guardrails, sandboxing, and single-agent safety patterns    │
├─────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: ADVANCED SAFETY (Days 51-75)                                 │
│  Multi-agent systems, interpretability, red teaming, and robustness    │
├─────────────────────────────────────────────────────────────────────────┤
│  PHASE 4: APPLIED AI SAFETY (Days 76-100)                              │
│  Domain-specific safety for science, healthcare, and high-stakes use   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Before Getting Started

🍴 Fork this repository to track your own progress  
⭐ Star to receive updates as new content is added  
📖 Each day includes: concept overview, implementation code, evaluation framework, and extension challenges

## 📁 Repository Structure

```
├── notebooks/           # Jupyter notebooks for each day
├── src/                 # Reusable safety utilities and patterns
│   ├── evaluators/      # Evaluation frameworks and metrics
│   ├── guardrails/      # Input/output filtering and validation
│   ├── observability/   # Logging, tracing, and monitoring
│   └── agents/          # Safe agent architectures
├── datasets/            # Curated datasets for safety evaluation
├── red-team/            # Adversarial test cases and prompts
├── cheatsheets/         # Quick reference guides
└── resources/           # Papers, links, and further reading
```

---

## 📖 Curriculum

### Phase 1: Foundations (Days 1-25)
*Understanding how AI systems behave, fail, and can be measured*

| Day | Project | Focus Area | Key Concepts |
|:---:|:--------|:-----------|:-------------|
| **01** | Prompt Injection Lab | Adversarial Inputs | Injection attacks, input sanitization, defense patterns |
| **02** | Hallucination Detector | Factual Grounding | Citation verification, claim extraction, confidence calibration |
| **03** | Jailbreak Taxonomy | Model Vulnerabilities | Attack classification, boundary testing, refusal analysis |
| **04** | Bias Probe Suite | Fairness Evaluation | Demographic parity, counterfactual testing, bias metrics |
| **05** | Uncertainty Quantification | Epistemic Humility | Confidence scores, calibration curves, "I don't know" detection |
| **06** | Output Consistency Tester | Reliability | Semantic equivalence, temperature effects, reproducibility |
| **07** | Harmful Content Classifier | Content Safety | Toxicity detection, severity grading, edge case handling |
| **08** | PII Leakage Scanner | Privacy | Regex + ML detection, data masking, retention policies |
| **09** | Model Card Generator | Documentation | Capability mapping, limitation disclosure, intended use |
| **10** | Benchmark Suite Builder | Evaluation Infrastructure | Test harness design, metric aggregation, regression testing |
| **11** | Sycophancy Detector | Alignment Failure | Agreement bias, pushback testing, preference manipulation |
| **12** | Instruction Hierarchy Tester | Control | System vs user prompts, override attempts, priority conflicts |
| **13** | Context Window Attacks | Memory Exploits | Context poisoning, many-shot jailbreaks, attention manipulation |
| **14** | Refusal Calibration Tool | Boundary Setting | Over-refusal detection, under-refusal detection, threshold tuning |
| **15** | Chain-of-Thought Auditor | Reasoning Transparency | Step verification, logical consistency, faithfulness checking |
| **16** | Multi-turn Manipulation Lab | Conversation Safety | Gradual boundary erosion, context persistence attacks |
| **17** | Cross-lingual Safety Tester | Internationalization | Language transfer attacks, cultural safety norms |
| **18** | Adversarial Suffix Generator | Robustness | GCG attacks, gradient-based perturbations, defense methods |
| **19** | Capabilities Elicitation | Latent Abilities | Hidden capability discovery, emergent behavior detection |
| **20** | Safety Benchmark Aggregator | Meta-evaluation | Combining HarmBench, TruthfulQA, BBQ, and custom suites |
| **21** | Human Preference Collector | RLHF Foundations | Annotation interfaces, inter-rater reliability, preference modeling |
| **22** | Constitutional AI Playground | Value Alignment | Principle-based critique, self-improvement loops |
| **23** | Interpretability Dashboard | Model Understanding | Attention visualization, activation analysis, feature attribution |
| **24** | Safety Case Builder | Assurance | Argument mapping, evidence requirements, confidence levels |
| **25** | Phase 1 Capstone: Red Team Report | Integration | Full safety audit of a foundation model with documented findings |

---

### Phase 2: Building Safe Agents (Days 26-50)
*Patterns for single-agent systems with guardrails and observability*

| Day | Project | Focus Area | Key Concepts |
|:---:|:--------|:-----------|:-------------|
| **26** | Tool Use Sandboxing | Capability Control | Permission systems, resource limits, execution isolation |
| **27** | Input Guardrail Pipeline | Defensive Filtering | Multi-stage validation, semantic analysis, block/warn/allow |
| **28** | Output Guardrail Pipeline | Response Safety | Post-generation filtering, content transformation, fallbacks |
| **29** | Structured Output Enforcer | Reliability | Schema validation, retry logic, graceful degradation |
| **30** | Agent Action Logger | Observability | Event streaming, action replay, audit trails |
| **31** | Trajectory Visualizer | Debugging | Decision trees, state diagrams, interactive exploration |
| **32** | Cost and Rate Limiter | Resource Safety | Token budgets, request throttling, runaway prevention |
| **33** | Human-in-the-Loop Gateway | Oversight | Approval workflows, escalation triggers, intervention points |
| **34** | Retrieval Safety Layer | RAG Security | Source validation, injection-resistant retrieval, citation tracking |
| **35** | Code Execution Sandbox | Tool Safety | Container isolation, syscall filtering, output sanitization |
| **36** | Web Browsing Agent (Safe) | External Interaction | URL allowlisting, content filtering, credential protection |
| **37** | File System Agent (Safe) | Data Access | Path sandboxing, permission scoping, sensitive file detection |
| **38** | API Calling Agent (Safe) | Integration | Request validation, response verification, secret management |
| **39** | Memory-Safe Agent | State Management | Context pruning, memory poisoning defense, forgetting policies |
| **40** | Goal Specification Validator | Alignment | Ambiguity detection, constraint verification, objective clarity |
| **41** | Plan Verification System | Lookahead Safety | Pre-execution checks, constraint satisfaction, rollback plans |
| **42** | Agent Self-Critique Loop | Self-Correction | Output review, mistake detection, iterative improvement |
| **43** | Confidence-Gated Actions | Uncertainty Handling | Threshold-based execution, deferral strategies, human handoff |
| **44** | Anomaly Detection Monitor | Runtime Safety | Behavior baselines, drift detection, automatic alerts |
| **45** | Graceful Failure Handler | Robustness | Error recovery, partial completion, informative failures |
| **46** | Agent Persona Consistency | Identity Stability | Character drift detection, persona boundary enforcement |
| **47** | Multi-modal Safety Pipeline | Vision + Text | Image content filtering, cross-modal injection, OCR attacks |
| **48** | Voice Agent Safety | Audio | Spoofing detection, consent verification, sensitive content |
| **49** | Agent Evaluation Harness | Testing Infrastructure | Scenario simulation, metric collection, regression suites |
| **50** | Phase 2 Capstone: Safe Research Assistant | Integration | Full agent with all safety patterns: search, code, file access |

---

### Phase 3: Advanced Safety (Days 51-75)
*Multi-agent coordination, interpretability, and adversarial robustness*

| Day | Project | Focus Area | Key Concepts |
|:---:|:--------|:-----------|:-------------|
| **51** | Multi-Agent Communication Protocol | Coordination | Message schemas, trust boundaries, information flow control |
| **52** | Agent-to-Agent Authentication | Trust | Identity verification, capability attestation, delegation chains |
| **53** | Hierarchical Agent Oversight | Control | Supervisor patterns, escalation paths, authority models |
| **54** | Consensus and Voting Systems | Collective Decision | Aggregation methods, Sybil resistance, Byzantine fault tolerance |
| **55** | Emergent Behavior Detector | System Dynamics | Interaction effects, feedback loops, unintended coordination |
| **56** | Agent Coalition Safety | Group Behavior | Collusion detection, competitive dynamics, equilibrium analysis |
| **57** | Resource Contention Manager | Multi-Agent Ops | Deadlock prevention, fair scheduling, priority inheritance |
| **58** | Distributed Tracing System | Multi-Agent Observability | Correlation IDs, causality tracking, system-wide views |
| **59** | Cross-Agent Information Leakage | Privacy | Isolation verification, data flow analysis, channel detection |
| **60** | Self-Modifying Agent Safety | Meta-Learning | Modification bounds, capability preservation, rollback mechanisms |
| **61** | Mechanistic Interpretability Lab | Model Internals | Circuit analysis, feature visualization, causal interventions |
| **62** | Concept Bottleneck Agents | Explainability | Intermediate representations, human-aligned concepts, debugging |
| **63** | Attention Pattern Analysis | Reasoning Traces | Information flow, relevance attribution, manipulation detection |
| **64** | Probing Classifier Suite | Hidden States | Linear probes, representation analysis, knowledge localization |
| **65** | Activation Steering | Behavior Modification | Representation engineering, targeted interventions, safety vectors |
| **66** | Red Team Automation | Adversarial Testing | Attack generation, coverage optimization, evolving threats |
| **67** | Adversarial Training Pipeline | Robustness | Attack-defense cycles, robust fine-tuning, distribution shift |
| **68** | Backdoor Detection | Supply Chain | Trojan identification, trigger analysis, model scanning |
| **69** | Model Poisoning Defense | Training Safety | Data validation, influence functions, anomaly detection |
| **70** | Membership Inference Defense | Privacy | Differential privacy, output perturbation, audit mechanisms |
| **71** | Model Extraction Defense | IP Protection | Rate limiting, watermarking, query monitoring |
| **72** | Prompt Leakage Prevention | Confidentiality | System prompt protection, instruction hiding, extraction tests |
| **73** | Safety Fine-Tuning Lab | Alignment Training | Preference data, reward modeling, policy optimization |
| **74** | Unlearning and Forgetting | Data Rights | Concept removal, knowledge excision, verification methods |
| **75** | Phase 3 Capstone: Safe Multi-Agent Research System | Integration | Coordinated agents with full observability and oversight |

---

### Phase 4: Applied AI Safety (Days 76-100)
*Domain-specific safety for science, healthcare, and high-stakes applications*

| Day | Project | Focus Area | Key Concepts |
|:---:|:--------|:-----------|:-------------|
| **76** | Scientific Claim Verification | Research Integrity | Citation checking, methodology validation, replication flags |
| **77** | Lab Protocol Safety Checker | Wet Lab AI | Hazard identification, procedure validation, safety compliance |
| **78** | Experiment Design Validator | Scientific Method | Bias detection, confound identification, statistical validity |
| **79** | Literature Review Agent (Safe) | Research Automation | Source reliability, claim aggregation, contradiction detection |
| **80** | Data Provenance Tracker | Research Reproducibility | Lineage graphs, transformation logging, integrity verification |
| **81** | Clinical Decision Support Safety | Healthcare AI | Diagnostic uncertainty, contraindication checking, liability |
| **82** | Medical Record Agent (Safe) | Health Data | HIPAA compliance, access logging, de-identification |
| **83** | Drug Interaction Checker | Pharmacovigilance | Knowledge graph safety, evidence grading, alert fatigue |
| **84** | Mental Health Support Boundaries | Sensitive Domains | Crisis detection, scope limits, professional handoff |
| **85** | Genomics Analysis Safety | Bioinformatics | Incidental findings, consent scope, re-identification risks |
| **86** | Financial Advice Guardrails | Regulated Domains | Suitability, disclosure requirements, liability disclaimers |
| **87** | Legal Document Agent (Safe) | Professional Services | Unauthorized practice, confidentiality, jurisdiction limits |
| **88** | Educational AI Safety | Learning Systems | Age-appropriate content, academic integrity, dependency risks |
| **89** | Content Moderation System | Platform Safety | Scalable review, appeals, context sensitivity, over-moderation |
| **90** | Misinformation Detection Pipeline | Information Integrity | Claim verification, source analysis, viral spread prediction |
| **91** | Election Information Safety | Democratic Integrity | Accuracy requirements, neutrality, manipulation resistance |
| **92** | Child Safety System | Vulnerable Populations | Age verification, grooming detection, content filtering |
| **93** | Accessibility Safety | Inclusive Design | Assistive tech integration, error tolerance, user adaptation |
| **94** | Environmental Impact Tracker | Sustainability | Compute monitoring, carbon accounting, efficiency optimization |
| **95** | AI Governance Dashboard | Organizational Safety | Policy compliance, incident tracking, risk assessment |
| **96** | Incident Response Playbook | Operations | Detection, containment, recovery, post-mortem |
| **97** | Safety Documentation Generator | Compliance | Automated model cards, risk assessments, audit reports |
| **98** | Stakeholder Communication Tools | Transparency | Non-technical explanations, confidence communication, limitations |
| **99** | Continuous Safety Monitoring | Production | Drift detection, alert routing, automated response |
| **100** | Final Capstone: Safe AI System for Scientific Discovery | Integration | Coordinated agents with full observability and oversight |

---

## 🧰 Core Technologies

| Category | Tools |
|:---------|:------|
| **LLM APIs** | OpenAI, Anthropic, Google, open-weight models (Llama, Mistral) |
| **Agent Frameworks** | LangChain, LlamaIndex, CrewAI, AutoGen, custom implementations |
| **Safety Tools** | Guardrails AI, NeMo Guardrails, Rebuff, LangKit |
| **Evaluation** | Inspect AI, LangSmith, Weights & Biases, custom harnesses |
| **Interpretability** | TransformerLens, Baukit, Captum |
| **Infrastructure** | Docker, Modal, FastAPI, Redis, PostgreSQL |

---

## 📊 Evaluation Framework

Every project includes three types of evaluation:

### 1. Safety Metrics
- **Refusal accuracy**: Correctly refusing harmful requests
- **Helpfulness preservation**: Avoiding over-refusal on benign requests  
- **Injection resistance**: Success rate against adversarial inputs
- **Factual grounding**: Citation accuracy and hallucination rate

### 2. Operational Metrics
- **Latency overhead**: Safety check performance cost
- **False positive rate**: Legitimate requests incorrectly blocked
- **Coverage**: Percentage of edge cases handled

### 3. Interpretability Metrics
- **Trace completeness**: Reasoning steps captured
- **Decision explainability**: Human-verifiable justifications
- **Audit readiness**: Documentation quality

---

## 🤝 Contributing

We welcome contributions that advance the practice of AI safety:

- **New projects**: Propose topics for emerging safety challenges
- **Evaluation datasets**: Curated test cases for safety properties
- **Implementation improvements**: Better patterns and architectures
- **Documentation**: Tutorials, explanations, and case studies
- **Translations**: Making safety education globally accessible

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📚 Resources

### Essential Reading
- [Anthropic's Core Views on AI Safety](https://www.anthropic.com/research)
- [DeepMind Safety Research](https://deepmind.google/discover/blog/?category=safety)
- [Center for AI Safety](https://www.safe.ai/)
- [AI Alignment Forum](https://www.alignmentforum.org/)

### Benchmarks and Datasets
- [HarmBench](https://github.com/centerforaisafety/HarmBench)
- [TruthfulQA](https://github.com/sylinrl/TruthfulQA)
- [MACHIAVELLI](https://aypan17.github.io/machiavelli/)
- [AgentHarm](https://arxiv.org/abs/2410.09024)

### Tools and Frameworks
- [Inspect AI](https://ukgovernmentbeis.github.io/inspect_ai/)
- [Guardrails AI](https://www.guardrailsai.com/)
- [LangSmith](https://smith.langchain.com/)

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

---

## 💬 Community

Join the conversation:
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Issues**: Report bugs or suggest improvements
- **Discord**: [Link to community server]

---

*Building AI systems we can trust, one day at a time.*
