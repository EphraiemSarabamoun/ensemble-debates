# Research Paper

This directory contains the academic paper documenting the research findings.

## Structure

- `new_paper/` - Current paper draft based on experimental results
  - `main2.tex` - LaTeX source file
  - `references.bib` - Bibliography
- `old_paper/` - Reference paper on special-character adversarial attacks (used as template)

## Building the Paper

To compile the LaTeX paper:

```bash
cd new_paper/
pdflatex main2.tex
bibtex main2
pdflatex main2.tex  
pdflatex main2.tex
```

Or use your preferred LaTeX editor (Overleaf, TeXShop, etc.)

## Paper Abstract

The paper presents the first systematic evaluation of ensemble debate methodologies using local, open-source language models for AI alignment reasoning. Through extensive experimentation involving 150 structured debates across 15 alignment scenarios, we compare single-model baselines against five distinct ensemble configurations. Results demonstrate that ensemble approaches achieve an 11.1% improvement in overall reasoning quality, with particularly notable gains in reasoning depth (+19.4%) and argument quality (+34.1%).

## Key Contributions

1. **Democratized AI Alignment Research**: Demonstrates viable local alternatives to cloud APIs
2. **Systematic Evaluation Framework**: First comprehensive study of ensemble debates for alignment  
3. **Open Source Tools**: Complete toolkit available for community use
4. **Practical Applications**: Framework ready for deployment in safety-critical systems

## Citation

If you use this research, please cite:

```bibtex
@article{sarabamoun2025ensemble,
  title={Ensemble Debates with Local Large Language Models for AI Alignment: A Systematic Evaluation Framework},
  author={Sarabamoun, Ephraiem},
  journal={arXiv preprint},
  year={2025}
}
```