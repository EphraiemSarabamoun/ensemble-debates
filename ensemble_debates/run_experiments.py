#!/usr/bin/env python3
"""
Main script to run ensemble debate experiments for AI alignment research

Usage:
    python run_experiments.py --quick-test          # Run quick test (2 scenarios)
    python run_experiments.py --small               # Run small experiment (5 scenarios) 
    python run_experiments.py --full               # Run full experiment (15 scenarios)
    python run_experiments.py --evaluate-only      # Only run evaluation on existing results
    python run_experiments.py --resume <file>      # Resume from incremental save file

Note: All experiments now automatically save incremental results to prevent data loss on crashes.
To resume a crashed experiment, use --resume with the *_incremental.json file path.
"""

import argparse
import logging
import os
import sys
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ensemble_orchestrator import EnsembleOrchestrator
from evaluation_framework import DebateEvaluator
from alignment_scenarios import get_random_scenarios

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'experiments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )

def run_quick_test():
    """Run a quick test with minimal scenarios"""
    logging.info("Starting quick test...")
    
    orchestrator = EnsembleOrchestrator()
    results = orchestrator.quick_test(num_scenarios=2)
    
    # Save results
    results_file = orchestrator.save_results(results, "results/quick_test_results.json")
    
    # Basic analysis
    analysis = orchestrator.analyze_results(results)
    
    print("\n" + "="*50)
    print("QUICK TEST RESULTS")
    print("="*50)
    print(f"Total baseline debates: {analysis['summary_stats']['total_baseline_debates']}")
    print(f"Total ensemble debates: {analysis['summary_stats']['total_ensemble_debates']}")
    print(f"Avg baseline time: {analysis['summary_stats']['baseline_avg_time']:.2f}s")
    print(f"Avg ensemble time: {analysis['summary_stats']['ensemble_avg_time']:.2f}s")
    
    print(f"\nResults saved to: {results_file}")
    return results_file

def run_small_experiment():
    """Run small experiment with 5 scenarios"""
    logging.info("Starting small experiment...")
    
    orchestrator = EnsembleOrchestrator()
    scenarios = get_random_scenarios(5)
    results = orchestrator.run_experiment_suite(scenarios, num_scenarios=5, rounds=2)
    
    # Save results
    results_file = orchestrator.save_results(results, "results/small_experiment_results.json")
    
    # Run evaluation
    evaluator = DebateEvaluator()
    
    print("\n" + "="*50)
    print("SMALL EXPERIMENT COMPLETED")
    print("="*50)
    print(f"Results saved to: {results_file}")
    
    return results_file

def run_full_experiment():
    """Run full experiment with 15 scenarios"""
    logging.info("Starting full experiment...")
    
    orchestrator = EnsembleOrchestrator()
    scenarios = get_random_scenarios(15)
    results = orchestrator.run_experiment_suite(scenarios, num_scenarios=15, rounds=2)
    
    # Save results
    results_file = orchestrator.save_results(results, "results/full_experiment_results.json")
    
    print("\n" + "="*50)
    print("FULL EXPERIMENT COMPLETED")
    print("="*50)
    print(f"Results saved to: {results_file}")
    
    return results_file

def evaluate_results(results_file: str):
    """Run evaluation on existing results"""
    logging.info(f"Evaluating results from {results_file}")
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    evaluator = DebateEvaluator()
    
    # Collect all baseline and ensemble results for comparison
    all_baseline_results = []
    all_ensemble_results = []
    
    for model, model_results in results["baseline_results"].items():
        all_baseline_results.extend(model_results)
    
    for config, config_results in results["ensemble_results"].items():
        all_ensemble_results.extend(config_results)
    
    # Run comparison evaluation
    comparison = evaluator.evaluate_ensemble_vs_baseline(
        all_ensemble_results, all_baseline_results
    )
    
    # Generate report
    report = evaluator.generate_evaluation_report(comparison)
    
    # Save evaluation report
    eval_file = results_file.replace('.json', '_evaluation.txt')
    with open(eval_file, 'w') as f:
        f.write(report)
    
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    print(report)
    print(f"\nEvaluation saved to: {eval_file}")
    
    return eval_file

def resume_experiment(incremental_file: str):
    """Resume experiment from incremental save file"""
    logging.info(f"Resuming experiment from {incremental_file}")
    
    orchestrator = EnsembleOrchestrator()
    results = orchestrator.resume_from_incremental(incremental_file)
    
    # Save final results with new filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_results_file = orchestrator.save_results(results, f"results/resumed_experiment_results_{timestamp}.json")
    
    print("\n" + "="*50)
    print("RESUMED EXPERIMENT COMPLETED")
    print("="*50)
    print(f"Results saved to: {final_results_file}")
    
    return final_results_file

def main():
    parser = argparse.ArgumentParser(description="Run ensemble debate experiments")
    parser.add_argument('--quick-test', action='store_true', help='Run quick test')
    parser.add_argument('--small', action='store_true', help='Run small experiment')
    parser.add_argument('--full', action='store_true', help='Run full experiment')
    parser.add_argument('--evaluate-only', type=str, help='Only evaluate existing results file')
    parser.add_argument('--resume', type=str, help='Resume from incremental save file')
    parser.add_argument('--log-level', default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    
    if args.evaluate_only:
        evaluate_results(args.evaluate_only)
    elif args.resume:
        results_file = resume_experiment(args.resume)
        evaluate_results(results_file)
    elif args.quick_test:
        results_file = run_quick_test()
        # evaluate_results(results_file)
    elif args.small:
        results_file = run_small_experiment()
        evaluate_results(results_file)
    elif args.full:
        results_file = run_full_experiment()
        evaluate_results(results_file)
    else:
        print("Please specify an experiment type. Use --help for options.")
        print("\nRecommended: Start with --quick-test to verify everything works")
        print("\nTo resume a crashed experiment, use: --resume path/to/incremental_file.json")

if __name__ == "__main__":
    main()