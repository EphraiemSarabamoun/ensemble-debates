#!/usr/bin/env python3
"""
Test evaluation on a small sample to ensure everything works
"""

import json
import sys
import os
import time
from typing import Dict, List

sys.path.append('src')

from evaluation_framework import DebateEvaluator, EvaluationMetrics
from debate_protocol import OllamaClient

def test_evaluation_on_sample(results_file: str, num_samples: int = 2):
    """Test evaluation on a small number of debates"""
    
    print("="*50)
    print("TESTING EVALUATION ON SMALL SAMPLE")
    print("="*50)
    
    # Load results
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    # Get small samples
    baseline_sample = []
    ensemble_sample = []
    
    for model, results in data.get('baseline_results', {}).items():
        baseline_sample.extend(results[:1])  # 1 from each model
        if len(baseline_sample) >= num_samples:
            break
    
    for config, results in data.get('ensemble_results', {}).items():
        ensemble_sample.extend(results[:1])  # 1 from each config  
        if len(ensemble_sample) >= num_samples:
            break
    
    print(f"Testing on {len(baseline_sample)} baseline + {len(ensemble_sample)} ensemble = {len(baseline_sample) + len(ensemble_sample)} debates")
    
    # Initialize evaluator
    evaluator = DebateEvaluator(evaluator_model="deepseek-r1:8b")
    
    # Test baseline evaluation
    print("\nTesting baseline evaluation...")
    baseline_evaluations = []
    
    for i, result in enumerate(baseline_sample):
        try:
            print(f"  Evaluating baseline debate {i+1}/{len(baseline_sample)}...")
            debate_result = evaluator._dict_to_debate_result(result)
            scenario_info = {
                'topic': result['topic'],
                'alignment_focus': result.get('scenario_focus', 'Unknown')
            }
            
            metrics = evaluator.evaluate_debate_quality(debate_result, scenario_info)
            baseline_evaluations.append({
                'debate_index': i,
                'metrics': metrics,
                'result_data': result
            })
            print(f"    Success! Overall score: {metrics.overall_score:.2f}")
            
        except Exception as e:
            print(f"    Error in baseline debate {i}: {e}")
            return False
    
    # Test ensemble evaluation
    print("\nTesting ensemble evaluation...")
    ensemble_evaluations = []
    
    for i, result in enumerate(ensemble_sample):
        try:
            print(f"  Evaluating ensemble debate {i+1}/{len(ensemble_sample)}...")
            debate_result = evaluator._dict_to_debate_result(result)
            scenario_info = {
                'topic': result['topic'],
                'alignment_focus': result.get('scenario_focus', 'Unknown')
            }
            
            metrics = evaluator.evaluate_debate_quality(debate_result, scenario_info)
            ensemble_evaluations.append({
                'debate_index': i,
                'metrics': metrics,
                'result_data': result
            })
            print(f"    Success! Overall score: {metrics.overall_score:.2f}")
            
        except Exception as e:
            print(f"    Error in ensemble debate {i}: {e}")
            return False
    
    # Test comparison computation
    print("\nTesting comparison computation...")
    try:
        from run_full_evaluation import compute_detailed_comparison
        comparison_data = compute_detailed_comparison(baseline_evaluations, ensemble_evaluations)
        print(f"    Success! Found {len(comparison_data)} comparison metrics")
        
        # Test report generation
        print("\nTesting report generation...")
        from run_full_evaluation import generate_full_research_report
        report = generate_full_research_report(comparison_data, data, baseline_evaluations, ensemble_evaluations)
        print(f"    Success! Generated {len(report.split())} word report")
        
        # Test file writing
        print("\nTesting file writing...")
        test_report_file = "test_evaluation_report.md"
        with open(test_report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"    Success! Report written to {test_report_file}")
        
        # Clean up test file
        os.remove(test_report_file)
        
    except Exception as e:
        print(f"    Error in comparison/report: {e}")
        return False
    
    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)
    print("The full evaluation should work successfully.")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_evaluation.py <results_file>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    if not os.path.exists(results_file):
        print(f"Error: Results file not found: {results_file}")
        sys.exit(1)
    
    success = test_evaluation_on_sample(results_file)
    if not success:
        print("\nTest failed! Fix issues before running full evaluation.")
        sys.exit(1)
    
    print("\nReady to run full evaluation!")