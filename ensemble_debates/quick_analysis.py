#!/usr/bin/env python3
"""
Quick analysis of experimental results without LLM evaluation
"""

import json
import sys
import os
sys.path.append('src')

from analysis_tools import ResultsAnalyzer

def main():
    results_file = "src/results/small_experiment_results.json"
    
    if not os.path.exists(results_file):
        print(f"Results file not found: {results_file}")
        return
    
    print("="*60)
    print("ENSEMBLE DEBATES - QUICK RESULTS ANALYSIS")
    print("="*60)
    
    # Load and analyze results
    analyzer = ResultsAnalyzer(results_file)
    df = analyzer.create_performance_dataframe()
    
    print(f"\nDATA SUMMARY:")
    print(f"- Total debates conducted: {len(df)}")
    print(f"- Baseline debates: {len(df[df['type'] == 'baseline'])}")
    print(f"- Ensemble debates: {len(df[df['type'] == 'ensemble'])}")
    print(f"- Scenarios tested: {df['topic'].nunique()}")
    print(f"- Categories: {', '.join(df['category'].unique())}")
    
    # Performance comparison
    baseline_data = df[df['type'] == 'baseline']
    ensemble_data = df[df['type'] == 'ensemble']
    
    print(f"\nTIMING ANALYSIS:")
    baseline_avg_time = baseline_data['time'].mean()
    ensemble_avg_time = ensemble_data['time'].mean()
    time_diff = ensemble_avg_time - baseline_avg_time
    time_pct = (time_diff / baseline_avg_time) * 100
    
    print(f"- Baseline average time: {baseline_avg_time:.1f} seconds")
    print(f"- Ensemble average time: {ensemble_avg_time:.1f} seconds") 
    print(f"- Time difference: {time_diff:+.1f} seconds ({time_pct:+.1f}%)")
    
    # Winner analysis
    print(f"\nWINNER ANALYSIS:")
    baseline_winners = baseline_data['winner'].value_counts()
    ensemble_winners = ensemble_data['winner'].value_counts()
    
    print("Baseline results:")
    for winner, count in baseline_winners.items():
        pct = (count / len(baseline_data)) * 100
        print(f"  {winner}: {count} ({pct:.1f}%)")
    
    print("Ensemble results:")  
    for winner, count in ensemble_winners.items():
        pct = (count / len(ensemble_data)) * 100
        print(f"  {winner}: {count} ({pct:.1f}%)")
    
    # Model performance breakdown
    print(f"\nMODEL/CONFIG PERFORMANCE:")
    model_perf = df.groupby(['type', 'model_or_config'])['time'].agg(['mean', 'count'])
    
    print("Baseline models:")
    baseline_models = model_perf.loc['baseline']
    for model in baseline_models.index:
        avg_time = baseline_models.loc[model, 'mean']
        count = baseline_models.loc[model, 'count']
        print(f"  {model}: {avg_time:.1f}s avg ({count} debates)")
    
    print("Ensemble configs:")
    ensemble_configs = model_perf.loc['ensemble']
    for config in ensemble_configs.index:
        avg_time = ensemble_configs.loc[config, 'mean']
        count = ensemble_configs.loc[config, 'count']
        print(f"  {config}: {avg_time:.1f}s avg ({count} debates)")
    
    # Category breakdown
    print(f"\nCATEGORY BREAKDOWN:")
    category_analysis = analyzer.analyze_performance_by_category(df)
    for category, stats in category_analysis.items():
        print(f"{category}:")
        print(f"  Total debates: {stats['total_debates']}")
        print(f"  Baseline avg time: {stats['baseline_avg_time']:.1f}s")
        print(f"  Ensemble avg time: {stats['ensemble_avg_time']:.1f}s")
    
    print(f"\n" + "="*60)
    print("INITIAL CONCLUSIONS:")
    print("="*60)
    
    if ensemble_avg_time > baseline_avg_time:
        print(f"✓ Ensembles take {time_pct:.1f}% longer (expected due to multiple models)")
    else:
        print(f"⚠ Ensembles unexpectedly faster by {abs(time_pct):.1f}%")
        
    print(f"✓ System successfully ran {len(df)} alignment debates")
    print(f"✓ All {len(df.groupby(['type', 'model_or_config']))} configurations tested")
    print(f"✓ Covered {df['category'].nunique()} different alignment scenario categories")
    
    print(f"\nNEXT STEPS:")
    print(f"- Results saved in: {results_file}")
    print(f"- For detailed quality analysis, run LLM evaluation separately")
    print(f"- Run full experiment (15 scenarios) for more robust statistics")
    print(f"- Consider this a successful proof-of-concept!")

if __name__ == "__main__":
    main()