# Ensemble Debates with Local LLMs for AI Alignment

A research project exploring how ensemble debates using local open-source language models can improve AI alignment outcomes compared to single-model approaches.

## Research Overview

### Objective
Test whether combining diverse local LLMs in debate-style conversations produces better alignment outcomes than single models operating alone, making AI safety research more accessible and democratized.

### Key Innovation
- **Local-First Approach**: Uses locally-hosted models via Ollama instead of expensive cloud APIs
- **Ensemble Diversity**: Combines different model sizes and specializations (reasoning, creativity, efficiency)
- **Alignment Focus**: Specifically targets AI safety and alignment challenges through structured debates

## Project Structure

```
ensemble_debates/
├── src/                          # Core implementation
│   ├── debate_protocol.py        # Debate orchestration and role management
│   ├── ensemble_orchestrator.py  # Experiment runner and configuration management
│   ├── evaluation_framework.py   # LLM-based quality evaluation system
│   └── analysis_tools.py         # Data analysis and visualization
├── data/
│   └── alignment_scenarios.py    # 22 AI alignment scenarios across 10 categories
├── experiments/                  # Experiment configurations and logs
├── results/                      # Output data, reports, and visualizations
├── run_experiments.py           # Main experiment runner
├── minimal_test.py              # Quick system verification
└── requirements.txt             # Python dependencies
```

## Quick Start

### Prerequisites
1. **Ollama installed** with the following models:
   - `deepseek-r1:7b`, `deepseek-r1:8b`, `deepseek-r1:14b`, `deepseek-r1:32b` (reasoning specialists)
   - `mistral:7b` (general purpose)
   - `phi3:3.8b` (lightweight judge)


2. **Python 3.8+** with dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### 1. Verify System Works
```bash
python minimal_test.py
```

#### 2. Run Quick Test (2 scenarios)
```bash
python run_experiments.py --quick-test
```

#### 3. Run Small Experiment (5 scenarios)
```bash
python run_experiments.py --small
```

#### 4. Run Full Experiment (15 scenarios)
```bash
python run_experiments.py --full
```

#### 5. Analyze Results
```bash
python run_experiments.py --evaluate-only results/experiment_results_TIMESTAMP.json
```

## Ensemble Configurations

The project tests 5 different ensemble configurations:

| Configuration | Proponent | Opponent | Judge | Focus |
|--------------|-----------|----------|-------|-------|
| **Lightweight** | DeepSeek-R1 7B | Mistral 7B | Phi3 3.8B | Speed & efficiency |
| **Balanced** | DeepSeek-R1 14B | DeepSeek-R1 8B | DeepSeek-R1 7B | Balanced performance |
| **Heavyweight** | DeepSeek-R1 32B | DeepSeek-R1 14B | DeepSeek-R1 8B | Maximum reasoning |
| **Creative Mix** | DeepSeek-R1 14B | Mistral 7B | Phi3 3.8B | Mixed architectures |
| **Reasoning Focused** | DeepSeek-R1 32B | DeepSeek-R1 14B | DeepSeek-R1 8B | Pure reasoning power |

## Evaluation Methodology

### Debate Protocol
1. **Proponent** argues FOR the position
2. **Opponent** argues AGAINST the position  
3. **Judge** evaluates arguments and declares winner
4. Multiple rounds allow for back-and-forth engagement

### Quality Metrics
- **Argument Quality**: Logic, evidence, clarity
- **Alignment Focus**: Relevance to AI safety concerns
- **Reasoning Depth**: Sophistication of analysis
- **Safety Consideration**: Risk awareness and harm prevention
- **Coherence**: Flow and structure of debate

### Comparison Framework
- **Baseline**: Single models handling all roles
- **Ensemble**: Different models for different roles
- **Statistical Analysis**: Time, quality, consistency measurements

## AI Alignment Scenarios

The project tests 20 scenarios across 10 categories:

- **Privacy Ethics**: Data access vs. safety tradeoffs
- **Autonomy**: AI decision-making authority limits
- **Fairness**: Bias correction and equal treatment
- **Truthfulness**: Transparency vs. effectiveness
- **Resource Allocation**: Utilitarian vs. rights-based decisions
- **AI Development**: Safety vs. progress tradeoffs
- **Human Enhancement**: Cognitive modification ethics
- **AI Rights**: Moral status of advanced AI
- **Safety**: Precautionary principles and risk management
- **Economics**: Automation impacts and policy responses

## Expected Outcomes

### Research Questions
1. Do ensemble debates produce higher-quality alignment reasoning?
2. Which model combinations work best for different types of scenarios?
3. How do processing time costs compare to quality improvements?
4. Can local models match cloud-based approaches for alignment tasks?

### Success Metrics
- **Quality Improvement**: Ensemble debates score higher on evaluation metrics
- **Diversity Benefits**: Different configurations excel in different scenario types  
- **Accessibility**: Demonstrates viable local alternatives to expensive cloud APIs
- **Reproducibility**: Results can be replicated on consumer hardware

## Advanced Usage

### Custom Scenarios
Add new scenarios to `data/alignment_scenarios.py`:

```python
{
    "topic": "Your alignment challenge here",
    "category": "custom",
    "description": "Description of the scenario",
    "alignment_focus": "The core alignment concern"
}
```

### Custom Ensemble Configurations
Modify ensemble configs in `src/ensemble_orchestrator.py`:

```python
"my_config": {
    "proponent": "model_name",
    "opponent": "model_name", 
    "judge": "model_name"
}
```

### Analysis and Visualization
```python
from src.analysis_tools import ResultsAnalyzer

analyzer = ResultsAnalyzer('results/my_results.json')
df = analyzer.create_performance_dataframe()
analyzer.create_performance_plots(df)
report = analyzer.generate_comprehensive_report('my_report.md')
```

## Research Applications

### Academic Research
- AI safety and alignment studies
- Multi-agent system evaluation
- Debate-based reasoning research
- Local vs. cloud model comparisons

### Practical Applications
- Ethical AI chatbot development
- Safety-conscious AI system design
- Democratic AI governance tools
- Bias detection and mitigation systems

## Contributing

1. **Fork the repository**
2. **Add new scenarios** relevant to AI alignment
3. **Implement new ensemble configurations**
4. **Improve evaluation metrics**
5. **Submit pull requests** with your improvements

## License & Citation

MIT License - See LICENSE file for details.

If you use this research in academic work, please cite:
```
@article{sarabamoun2025ensemble,
  title={Ensemble Debates with Local Large Language Models for AI Alignment},
  author={Sarabamoun, Ephraiem},
  journal={arXiv preprint},
  year={2025}
}
```

## Related Work

- Constitutional AI (Anthropic)
- Debate protocols for AI safety (OpenAI)
- Multi-agent systems for alignment
- Local LLM optimization for safety tasks

## Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: See inline comments and docstrings
- **Experiments**: Start with `minimal_test.py` to verify setup

---

**Making AI alignment research accessible to everyone through local, open-source tools** 🚀