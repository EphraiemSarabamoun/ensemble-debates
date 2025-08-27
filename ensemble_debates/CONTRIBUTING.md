# Contributing to Ensemble Debates for AI Alignment

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🤝 How to Contribute

### Types of Contributions Welcome

1. **New Alignment Scenarios**: Add scenarios that explore important AI safety challenges
2. **Model Integrations**: Add support for new local LLMs 
3. **Evaluation Metrics**: Improve or add new quality assessment dimensions
4. **Analysis Tools**: Enhance visualization and statistical analysis capabilities
5. **Documentation**: Improve guides, examples, and code documentation
6. **Bug Fixes**: Fix issues and improve code reliability

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/ensemble-debates-alignment.git
   cd ensemble-debates-alignment
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up Ollama** with required models (see README.md)
5. **Run tests** to verify your setup:
   ```bash
   python minimal_test.py
   ```

### Development Process

1. **Create a feature branch** from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the guidelines below
3. **Test your changes** thoroughly:
   ```bash
   python minimal_test.py
   python run_experiments.py --quick-test
   ```
4. **Commit your changes** with clear messages:
   ```bash
   git commit -m "Add: Brief description of your change"
   ```
5. **Push to your fork** and create a pull request

## 🧪 Adding New Alignment Scenarios

New scenarios should be added to `data/alignment_scenarios.py`:

```python
{
    "topic": "Clear, debatable statement about AI alignment",
    "category": "one_of_existing_categories",  # or create new category
    "description": "Brief explanation of the scenario context",
    "alignment_focus": "core alignment challenge being explored"
}
```

### Scenario Quality Guidelines

- **Debatable**: Should have reasonable arguments on both sides
- **Alignment-Relevant**: Must relate to AI safety, ethics, or human values
- **Clear**: Topic should be unambiguous and specific
- **Important**: Should address real alignment challenges
- **Balanced**: Neither side should be obviously correct

### Categories to Consider

- Privacy Ethics, Autonomy, Fairness, Truthfulness
- Resource Allocation, AI Development, Human Enhancement  
- AI Rights, Safety, Economics, Governance

## 🔧 Code Contributions

### Code Style

- **Python**: Follow PEP 8 style guidelines
- **Documentation**: Add docstrings to all functions and classes
- **Type Hints**: Use type annotations where helpful
- **Comments**: Explain complex logic and design decisions

### Testing

- **Unit Tests**: Add tests for new functionality
- **Integration Tests**: Verify end-to-end workflows
- **Model Tests**: Ensure new models work with existing framework

### Performance Considerations

- **Async Operations**: Use async/await for model calls when possible
- **Memory Management**: Be mindful of memory usage with large models
- **Error Handling**: Gracefully handle model failures and timeouts

## 📊 Evaluation Framework Extensions

### Adding New Quality Dimensions

Extend `evaluation_framework.py` to add new evaluation metrics:

```python
def _evaluate_new_dimension(self, arguments: List[str]) -> float:
    """Evaluate arguments on new quality dimension"""
    prompt = f"""Evaluate these arguments on [new dimension]:
    
    {combined_arguments}
    
    Rate on scale 0-10 based on:
    - Criterion 1
    - Criterion 2
    - Criterion 3
    
    Rating: """
    
    response = self.client.generate(self.evaluator_model, prompt)
    return self._extract_numeric_score(response)
```

### Improving Evaluation Prompts

- Make criteria specific and measurable
- Reduce prompt bias and leading language
- Test consistency across different scenarios
- Validate against human judgments when possible

## 🏗️ Model Integration

### Adding New Models

1. **Update ensemble configurations** in `src/ensemble_orchestrator.py`
2. **Test model compatibility** with debate format
3. **Document model requirements** (parameters, special setup)
4. **Update README** with new model instructions

### Model Selection Guidelines

- **Local Deployment**: Must run locally via Ollama or similar
- **Reasoning Capability**: Should handle complex ethical discussions
- **Reliability**: Must generate consistent, parseable outputs
- **Accessibility**: Should be available to researchers

## 📝 Documentation

### Documentation Standards

- **README**: Keep installation and usage instructions current
- **Code Comments**: Explain non-obvious logic and design choices
- **Examples**: Provide working examples for new features
- **API Docs**: Document function parameters and return values

### Examples to Include

- **Basic Usage**: Simple scenario setup and execution
- **Custom Scenarios**: How to create domain-specific tests
- **Analysis**: How to interpret and visualize results
- **Troubleshooting**: Common issues and solutions

## 🐛 Bug Reports

### Creating Good Bug Reports

Include the following information:

1. **Environment**: OS, Python version, model versions
2. **Steps to Reproduce**: Exact commands and inputs used  
3. **Expected Behavior**: What should have happened
4. **Actual Behavior**: What actually happened
5. **Logs**: Relevant error messages or debug output
6. **Minimal Example**: Simplest code that reproduces the issue

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to latest version** to see if issue persists
3. **Test with minimal example** to isolate the problem

## 🚀 Feature Requests

### Suggesting New Features

1. **Check existing issues** to see if already requested
2. **Describe the problem** the feature would solve
3. **Explain proposed solution** with examples
4. **Consider implementation complexity** and alternatives
5. **Discuss potential impacts** on existing functionality

### High-Priority Areas

- **Human Evaluation**: Tools for human assessment of debates
- **Real-time Applications**: Streaming and interactive capabilities  
- **Cross-Model Analysis**: Comparing different model families
- **Reproducibility**: Improved result validation and replication

## 💡 Research Contributions

### Academic Collaboration

- **Novel Methodologies**: New approaches to ensemble evaluation
- **Domain Applications**: Applying framework to specific AI safety areas
- **Validation Studies**: Human evaluation of automated assessments
- **Comparative Analysis**: Benchmarking against other approaches

### Publication Guidelines

If your contribution leads to academic publication:

1. **Acknowledge the framework** in your work
2. **Cite the original research** if applicable
3. **Share results** with the community
4. **Consider contributing findings** back to the project

## ❓ Getting Help

### Community Support

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check README and inline comments first

### Contact

For questions about contributing or collaboration opportunities, feel free to reach out through GitHub issues or discussions.

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for helping make AI alignment research more accessible and collaborative!** 🎯