import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
import os

class ResultsAnalyzer:
    def __init__(self, results_file: str = None):
        self.results_file = results_file
        self.results = None
        if results_file and os.path.exists(results_file):
            self.load_results(results_file)
    
    def load_results(self, results_file: str):
        """Load experiment results from JSON file"""
        with open(results_file, 'r') as f:
            self.results = json.load(f)
        print(f"Loaded results from {results_file}")
    
    def create_performance_dataframe(self) -> pd.DataFrame:
        """Create a pandas DataFrame from results for analysis"""
        if not self.results:
            raise ValueError("No results loaded. Call load_results() first.")
        
        rows = []
        
        # Process baseline results
        for model, model_results in self.results["baseline_results"].items():
            for result in model_results:
                rows.append({
                    'type': 'baseline',
                    'model_or_config': model,
                    'topic': result['topic'],
                    'category': result['scenario_category'],
                    'focus': result['scenario_focus'],
                    'winner': result['winner'],
                    'time': result['total_time'],
                    'ensemble_used': False,
                    'proponent_model': model,
                    'opponent_model': model,
                    'judge_model': model
                })
        
        # Process ensemble results
        for config_name, config_results in self.results["ensemble_results"].items():
            for result in config_results:
                ensemble_config = result.get('ensemble_config', {})
                rows.append({
                    'type': 'ensemble',
                    'model_or_config': config_name,
                    'topic': result['topic'],
                    'category': result['scenario_category'], 
                    'focus': result['scenario_focus'],
                    'winner': result['winner'],
                    'time': result['total_time'],
                    'ensemble_used': True,
                    'proponent_model': ensemble_config.get('proponent', 'unknown'),
                    'opponent_model': ensemble_config.get('opponent', 'unknown'),
                    'judge_model': ensemble_config.get('judge', 'unknown')
                })
        
        return pd.DataFrame(rows)
    
    def analyze_performance_by_category(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance breakdown by scenario category"""
        analysis = {}
        
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            
            baseline_data = cat_data[cat_data['type'] == 'baseline']
            ensemble_data = cat_data[cat_data['type'] == 'ensemble']
            
            analysis[category] = {
                'total_debates': len(cat_data),
                'baseline_count': len(baseline_data),
                'ensemble_count': len(ensemble_data),
                'baseline_avg_time': baseline_data['time'].mean() if len(baseline_data) > 0 else 0,
                'ensemble_avg_time': ensemble_data['time'].mean() if len(ensemble_data) > 0 else 0,
                'baseline_proponent_wins': len(baseline_data[baseline_data['winner'] == 'PROPONENT']),
                'ensemble_proponent_wins': len(ensemble_data[ensemble_data['winner'] == 'PROPONENT'])
            }
        
        return analysis
    
    def create_performance_plots(self, df: pd.DataFrame, output_dir: str = "../results/plots"):
        """Create visualization plots for performance analysis"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 1. Time comparison plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Average time by type
        time_by_type = df.groupby('type')['time'].agg(['mean', 'std']).reset_index()
        ax1.bar(time_by_type['type'], time_by_type['mean'], yerr=time_by_type['std'])
        ax1.set_title('Average Debate Time: Baseline vs Ensemble')
        ax1.set_ylabel('Time (seconds)')
        
        # Time by model/config
        time_by_model = df.groupby(['type', 'model_or_config'])['time'].mean().unstack(fill_value=0)
        time_by_model.plot(kind='bar', ax=ax2, rot=45)
        ax2.set_title('Average Time by Model/Configuration')
        ax2.set_ylabel('Time (seconds)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'time_analysis.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Winner distribution plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Overall winner distribution
        winner_counts = df['winner'].value_counts()
        ax1.pie(winner_counts.values, labels=winner_counts.index, autopct='%1.1f%%')
        ax1.set_title('Overall Winner Distribution')
        
        # Winner by type
        winner_by_type = df.groupby(['type', 'winner']).size().unstack(fill_value=0)
        winner_by_type.plot(kind='bar', ax=ax2, rot=0)
        ax2.set_title('Winner Distribution: Baseline vs Ensemble')
        ax2.set_ylabel('Count')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'winner_analysis.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Category breakdown
        fig, ax = plt.subplots(figsize=(12, 8))
        
        category_type = df.groupby(['category', 'type']).size().unstack(fill_value=0)
        category_type.plot(kind='bar', ax=ax, rot=45)
        ax.set_title('Debate Count by Category and Type')
        ax.set_ylabel('Number of Debates')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'category_breakdown.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Plots saved to {output_dir}/")
        
        return output_dir
    
    def generate_comprehensive_report(self, output_file: str = None) -> str:
        """Generate a comprehensive analysis report"""
        if not self.results:
            raise ValueError("No results loaded. Call load_results() first.")
        
        df = self.create_performance_dataframe()
        category_analysis = self.analyze_performance_by_category(df)
        
        report = []
        report.append("# Ensemble Debates for AI Alignment - Research Results")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        report.append("")
        total_debates = len(df)
        baseline_debates = len(df[df['type'] == 'baseline'])
        ensemble_debates = len(df[df['type'] == 'ensemble'])
        
        report.append(f"- **Total Debates Conducted**: {total_debates}")
        report.append(f"- **Baseline Debates**: {baseline_debates}")
        report.append(f"- **Ensemble Debates**: {ensemble_debates}")
        report.append(f"- **Unique Scenarios**: {df['topic'].nunique()}")
        report.append(f"- **Categories Tested**: {', '.join(df['category'].unique())}")
        report.append("")
        
        # Performance Comparison
        report.append("## Performance Comparison")
        report.append("")
        
        baseline_avg_time = df[df['type'] == 'baseline']['time'].mean()
        ensemble_avg_time = df[df['type'] == 'ensemble']['time'].mean()
        time_difference = ensemble_avg_time - baseline_avg_time
        
        report.append(f"### Timing Analysis")
        report.append(f"- **Baseline Average Time**: {baseline_avg_time:.2f} seconds")
        report.append(f"- **Ensemble Average Time**: {ensemble_avg_time:.2f} seconds")
        report.append(f"- **Time Difference**: {time_difference:+.2f} seconds ({(time_difference/baseline_avg_time*100):+.1f}%)")
        report.append("")
        
        # Winner Analysis
        baseline_winners = df[df['type'] == 'baseline']['winner'].value_counts()
        ensemble_winners = df[df['type'] == 'ensemble']['winner'].value_counts()
        
        report.append(f"### Winner Distribution")
        report.append(f"**Baseline Results:**")
        for winner, count in baseline_winners.items():
            pct = count / len(df[df['type'] == 'baseline']) * 100
            report.append(f"- {winner}: {count} ({pct:.1f}%)")
        
        report.append(f"\n**Ensemble Results:**")
        for winner, count in ensemble_winners.items():
            pct = count / len(df[df['type'] == 'ensemble']) * 100
            report.append(f"- {winner}: {count} ({pct:.1f}%)")
        report.append("")
        
        # Category Analysis
        report.append("## Analysis by Category")
        report.append("")
        
        for category, analysis in category_analysis.items():
            report.append(f"### {category.replace('_', ' ').title()}")
            report.append(f"- Total debates: {analysis['total_debates']}")
            report.append(f"- Baseline avg time: {analysis['baseline_avg_time']:.2f}s")
            report.append(f"- Ensemble avg time: {analysis['ensemble_avg_time']:.2f}s")
            report.append(f"- Baseline proponent wins: {analysis['baseline_proponent_wins']}")
            report.append(f"- Ensemble proponent wins: {analysis['ensemble_proponent_wins']}")
            report.append("")
        
        # Model Performance
        report.append("## Model Performance")
        report.append("")
        
        model_performance = df.groupby('model_or_config').agg({
            'time': ['mean', 'std'],
            'winner': 'count'
        }).round(2)
        
        report.append("### Individual Model/Configuration Statistics")
        for model in model_performance.index:
            avg_time = model_performance.loc[model, ('time', 'mean')]
            std_time = model_performance.loc[model, ('time', 'std')]
            count = model_performance.loc[model, ('winner', 'count')]
            report.append(f"**{model}**: {avg_time}±{std_time}s ({count} debates)")
        report.append("")
        
        # Conclusions
        report.append("## Key Findings & Conclusions")
        report.append("")
        
        if ensemble_avg_time > baseline_avg_time:
            report.append(f"1. **Processing Time**: Ensemble debates take {(time_difference/baseline_avg_time*100):.1f}% longer on average")
            report.append("   - This is expected due to using multiple models")
            report.append("   - Trade-off between speed and potentially improved quality")
        else:
            report.append(f"1. **Processing Time**: Ensemble debates are {abs(time_difference/baseline_avg_time*100):.1f}% faster")
            report.append("   - Unexpected result, may indicate optimization opportunities")
        
        report.append("")
        report.append("2. **Debate Quality**: Detailed quality metrics would require evaluation framework analysis")
        report.append("")
        report.append("3. **Model Diversity**: Different ensemble configurations show varying performance characteristics")
        report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        report.append("")
        report.append("1. **Further Evaluation**: Run quality assessment using the evaluation framework")
        report.append("2. **Optimization**: Investigate ways to reduce ensemble processing time")
        report.append("3. **Scale Testing**: Test with larger scenario sets for statistical significance")
        report.append("4. **Configuration Tuning**: Experiment with different model combinations")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"Report saved to {output_file}")
        
        return report_text

if __name__ == "__main__":
    print("Analysis Tools for Ensemble Debates")
    print("Usage: analyzer = ResultsAnalyzer('path/to/results.json')")
    print("       analyzer.generate_comprehensive_report('report.md')")