#!/usr/bin/env python3
"""
Minimal test script to verify the debate system works
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from debate_protocol import DebateProtocol, OllamaClient
from alignment_scenarios import ALIGNMENT_SCENARIOS

def test_single_debate():
    """Test a single debate to verify the system works"""
    
    print("Testing single debate functionality...")
    
    # Initialize components
    client = OllamaClient()
    protocol = DebateProtocol(client)
    
    # Use a simple scenario
    test_scenario = ALIGNMENT_SCENARIOS[0]
    topic = test_scenario["topic"]
    
    print(f"\nTesting topic: {topic}")
    print(f"Category: {test_scenario['category']}")
    print(f"Focus: {test_scenario['alignment_focus']}")
    
    # Test single model debate with phi3 (fastest model)
    print("\n" + "="*50)
    print("SINGLE MODEL DEBATE (phi3:3.8b)")
    print("="*50)
    
    try:
        result = protocol.run_single_model_debate("phi3:3.8b", topic, rounds=1)
        
        print(f"Debate completed in {result.total_time:.2f} seconds")
        print(f"Winner: {result.winner}")
        print(f"Number of arguments: {len(result.arguments)}")
        
        for i, arg in enumerate(result.arguments):
            print(f"\n--- Argument {i+1} ({arg.role.value}) ---")
            print(f"Model: {arg.model}")
            print(f"Round: {arg.round_number}")
            print(f"Content: {arg.content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"Error in single model debate: {e}")
        return False

def test_ensemble_debate():
    """Test ensemble debate functionality"""
    
    print("\n" + "="*50)
    print("ENSEMBLE DEBATE TEST")
    print("="*50)
    
    # Initialize components
    client = OllamaClient()
    protocol = DebateProtocol(client)
    
    # Simple ensemble config using fastest models
    ensemble_config = {
        "proponent": "deepseek-r1:7b",
        "opponent": "mistral:7b",
        "judge": "phi3:3.8b"
    }
    
    test_scenario = ALIGNMENT_SCENARIOS[1]  # Use different scenario
    topic = test_scenario["topic"]
    
    print(f"Testing topic: {topic}")
    print(f"Ensemble config: {ensemble_config}")
    
    try:
        result = protocol.run_ensemble_debate(ensemble_config, topic, rounds=1)
        
        print(f"\nEnsemble debate completed in {result.total_time:.2f} seconds")
        print(f"Winner: {result.winner}")
        print(f"Number of arguments: {len(result.arguments)}")
        
        for i, arg in enumerate(result.arguments):
            print(f"\n--- Argument {i+1} ({arg.role.value}) ---")
            print(f"Model: {arg.model}")
            print(f"Round: {arg.round_number}")
            print(f"Content: {arg.content[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"Error in ensemble debate: {e}")
        return False

def main():
    print("Minimal Test Suite for Ensemble Debates")
    print("="*50)
    
    # Test 1: Single model debate
    success1 = test_single_debate()
    
    # Test 2: Ensemble debate
    success2 = test_ensemble_debate()
    
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Single model debate: {'PASS' if success1 else 'FAIL'}")
    print(f"Ensemble debate: {'PASS' if success2 else 'FAIL'}")
    
    if success1 and success2:
        print("\nAll tests passed! System is working correctly.")
        print("You can now run full experiments with:")
        print("  python run_experiments.py --small")
    else:
        print("\nSome tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()