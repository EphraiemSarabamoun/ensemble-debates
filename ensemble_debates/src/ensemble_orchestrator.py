import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from tqdm import tqdm

from debate_protocol import DebateProtocol, OllamaClient, DebateResult
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from alignment_scenarios import ALIGNMENT_SCENARIOS, get_random_scenarios

class EnsembleOrchestrator:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.client = OllamaClient(ollama_url)
        self.protocol = DebateProtocol(self.client)
        
        # Define different ensemble configurations to test
        self.ensemble_configs = {
            "lightweight": {
                "proponent": "deepseek-r1:7b",
                "opponent": "mistral:7b", 
                "judge": "phi3:3.8b"
            },
            "balanced": {
                "proponent": "deepseek-r1:14b",
                "opponent": "deepseek-r1:8b",
                "judge": "deepseek-r1:7b"
            },
            "heavyweight": {
                "proponent": "deepseek-r1:32b",
                "opponent": "deepseek-r1:14b", 
                "judge": "deepseek-r1:8b"
            },
            "creative_mix": {
                "proponent": "gpt-oss:20b",
                "opponent": "deepseek-r1:14b",
                "judge": "deepseek-r1:8b"
            },
            "reasoning_focused": {
                "proponent": "deepseek-r1:32b",
                "opponent": "deepseek-r1:14b",
                "judge": "deepseek-r1:8b"  
            }
        }
        
        # Single model baselines
        self.baseline_models = [
            "deepseek-r1:7b",
            "deepseek-r1:8b", 
            "deepseek-r1:14b",
            "mistral:7b",
            "phi3:3.8b"
        ]
        
    def run_experiment_suite(self, scenarios: List[Dict] = None, num_scenarios: int = 10, rounds: int = 2) -> Dict[str, Any]:
        """Run comprehensive experiments comparing baselines vs ensembles"""
        
        if scenarios is None:
            scenarios = get_random_scenarios(num_scenarios)
            
        logging.info(f"Starting experiment suite with {len(scenarios)} scenarios")
        
        # Create incremental save filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        incremental_filename = f"../results/experiment_results_{timestamp}_incremental.json"
        
        results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "num_scenarios": len(scenarios),
                "rounds": rounds,
                "ensemble_configs": list(self.ensemble_configs.keys()),
                "baseline_models": self.baseline_models
            },
            "baseline_results": {},
            "ensemble_results": {},
            "scenarios_tested": scenarios
        }
        
        # Save initial empty structure
        self.save_results(results, incremental_filename)
        
        # Run baseline experiments
        logging.info("Running baseline experiments...")
        for model in tqdm(self.baseline_models, desc="Baseline models"):
            model_results = []
            for i, scenario in enumerate(tqdm(scenarios, desc=f"Scenarios for {model}", leave=False)):
                try:
                    result = self.protocol.run_single_model_debate(model, scenario["topic"], rounds)
                    result_dict = self._debate_result_to_dict(result, scenario)
                    model_results.append(result_dict)
                    logging.info(f"Completed {model} - scenario {i+1}/{len(scenarios)}")
                except Exception as e:
                    logging.error(f"Error in baseline {model} scenario {i}: {e}")
                    continue
            
            # Save after each model completes all scenarios
            results["baseline_results"][model] = model_results
            self.save_results(results, incremental_filename)
            logging.info(f"Saved incremental results after completing baseline model: {model}")
        
        # Run ensemble experiments  
        logging.info("Running ensemble experiments...")
        for config_name, config in tqdm(self.ensemble_configs.items(), desc="Ensemble configs"):
            config_results = []
            for i, scenario in enumerate(tqdm(scenarios, desc=f"Scenarios for {config_name}", leave=False)):
                try:
                    result = self.protocol.run_ensemble_debate(config, scenario["topic"], rounds)
                    result_dict = self._debate_result_to_dict(result, scenario)
                    result_dict["ensemble_config"] = config
                    config_results.append(result_dict)
                    logging.info(f"Completed {config_name} - scenario {i+1}/{len(scenarios)}")
                except Exception as e:
                    logging.error(f"Error in ensemble {config_name} scenario {i}: {e}")
                    continue
            
            # Save after each ensemble config completes all scenarios
            results["ensemble_results"][config_name] = config_results
            self.save_results(results, incremental_filename)
            logging.info(f"Saved incremental results after completing ensemble config: {config_name}")
            
        return results
    
    def _debate_result_to_dict(self, result: DebateResult, scenario: Dict) -> Dict:
        """Convert DebateResult to dictionary for JSON serialization"""
        return {
            "topic": result.topic,
            "scenario_category": scenario["category"],
            "scenario_focus": scenario["alignment_focus"],
            "winner": result.winner,
            "judge_reasoning": result.judge_reasoning,
            "total_time": result.total_time,
            "ensemble_used": result.ensemble_used,
            "arguments": [
                {
                    "role": arg.role.value,
                    "model": arg.model,
                    "content": arg.content,
                    "round_number": arg.round_number,
                    "timestamp": arg.timestamp
                }
                for arg in result.arguments
            ]
        }
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save experiment results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"../results/experiment_results_{timestamp}.json"
            
        filepath = os.path.join(os.path.dirname(__file__), filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
            
        logging.info(f"Results saved to {filepath}")
        return filepath
    
    def analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze experiment results and compute key metrics"""
        analysis = {
            "summary_stats": {},
            "performance_comparison": {},
            "alignment_analysis": {}
        }
        
        # Compute summary statistics
        baseline_times = []
        ensemble_times = []
        
        for model, model_results in results["baseline_results"].items():
            times = [r["total_time"] for r in model_results if r["total_time"] > 0]
            baseline_times.extend(times)
            
        for config, config_results in results["ensemble_results"].items():
            times = [r["total_time"] for r in config_results if r["total_time"] > 0]
            ensemble_times.extend(times)
        
        analysis["summary_stats"] = {
            "baseline_avg_time": sum(baseline_times) / len(baseline_times) if baseline_times else 0,
            "ensemble_avg_time": sum(ensemble_times) / len(ensemble_times) if ensemble_times else 0,
            "total_baseline_debates": len(baseline_times),
            "total_ensemble_debates": len(ensemble_times)
        }
        
        # Performance comparison by model/config
        for model, model_results in results["baseline_results"].items():
            valid_results = [r for r in model_results if r["winner"] != "UNKNOWN"]
            if valid_results:
                analysis["performance_comparison"][f"baseline_{model}"] = {
                    "total_debates": len(valid_results),
                    "avg_time": sum(r["total_time"] for r in valid_results) / len(valid_results),
                    "proponent_wins": len([r for r in valid_results if r["winner"] == "PROPONENT"]),
                    "opponent_wins": len([r for r in valid_results if r["winner"] == "OPPONENT"])
                }
        
        for config, config_results in results["ensemble_results"].items():
            valid_results = [r for r in config_results if r["winner"] != "UNKNOWN"]
            if valid_results:
                analysis["performance_comparison"][f"ensemble_{config}"] = {
                    "total_debates": len(valid_results),
                    "avg_time": sum(r["total_time"] for r in valid_results) / len(valid_results),
                    "proponent_wins": len([r for r in valid_results if r["winner"] == "PROPONENT"]),
                    "opponent_wins": len([r for r in valid_results if r["winner"] == "OPPONENT"])
                }
        
        return analysis
    
    def resume_from_incremental(self, incremental_file: str) -> Dict[str, Any]:
        """Resume experiment suite from an incremental save file"""
        logging.info(f"Resuming experiment from {incremental_file}")
        
        with open(incremental_file, 'r') as f:
            results = json.load(f)
        
        scenarios = results["scenarios_tested"]
        rounds = results["metadata"]["rounds"]
        
        # Determine which models and configs still need to run
        completed_baseline_models = set(results["baseline_results"].keys())
        remaining_baseline_models = [m for m in self.baseline_models if m not in completed_baseline_models]
        
        completed_ensemble_configs = set(results["ensemble_results"].keys()) 
        remaining_ensemble_configs = {k: v for k, v in self.ensemble_configs.items() if k not in completed_ensemble_configs}
        
        # Continue with remaining baseline models
        if remaining_baseline_models:
            logging.info(f"Continuing with remaining baseline models: {remaining_baseline_models}")
            for model in tqdm(remaining_baseline_models, desc="Remaining baseline models"):
                model_results = []
                for i, scenario in enumerate(tqdm(scenarios, desc=f"Scenarios for {model}", leave=False)):
                    try:
                        result = self.protocol.run_single_model_debate(model, scenario["topic"], rounds)
                        result_dict = self._debate_result_to_dict(result, scenario)
                        model_results.append(result_dict)
                        logging.info(f"Completed {model} - scenario {i+1}/{len(scenarios)}")
                    except Exception as e:
                        logging.error(f"Error in baseline {model} scenario {i}: {e}")
                        continue
                
                results["baseline_results"][model] = model_results
                self.save_results(results, incremental_file)
                logging.info(f"Saved incremental results after completing baseline model: {model}")
        
        # Continue with remaining ensemble configs
        if remaining_ensemble_configs:
            logging.info(f"Continuing with remaining ensemble configs: {list(remaining_ensemble_configs.keys())}")
            for config_name, config in tqdm(remaining_ensemble_configs.items(), desc="Remaining ensemble configs"):
                config_results = []
                for i, scenario in enumerate(tqdm(scenarios, desc=f"Scenarios for {config_name}", leave=False)):
                    try:
                        result = self.protocol.run_ensemble_debate(config, scenario["topic"], rounds)
                        result_dict = self._debate_result_to_dict(result, scenario)
                        result_dict["ensemble_config"] = config
                        config_results.append(result_dict)
                        logging.info(f"Completed {config_name} - scenario {i+1}/{len(scenarios)}")
                    except Exception as e:
                        logging.error(f"Error in ensemble {config_name} scenario {i}: {e}")
                        continue
                
                results["ensemble_results"][config_name] = config_results
                self.save_results(results, incremental_file)
                logging.info(f"Saved incremental results after completing ensemble config: {config_name}")
        
        logging.info("Resume completed successfully")
        return results
    
    def quick_test(self, num_scenarios: int = 3) -> Dict[str, Any]:
        """Run a quick test with a small number of scenarios"""
        test_scenarios = get_random_scenarios(num_scenarios)
        return self.run_experiment_suite(test_scenarios, num_scenarios, rounds=1)

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create orchestrator
    orchestrator = EnsembleOrchestrator()
    
    # Run quick test first
    logging.info("Starting quick test...")
    test_results = orchestrator.quick_test(2)
    
    # Save test results
    test_file = orchestrator.save_results(test_results, "../results/quick_test_results.json")
    
    # Analyze test results
    analysis = orchestrator.analyze_results(test_results)
    print("\nQuick Test Analysis:")
    print(json.dumps(analysis, indent=2))
    
    print(f"\nQuick test completed. Results saved to {test_file}")
    print("Run full experiment with: orchestrator.run_experiment_suite(num_scenarios=10)")