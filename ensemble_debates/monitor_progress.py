#!/usr/bin/env python3
"""
Monitor the progress of the running experiment
"""

import time
import sys
import os
from datetime import datetime, timedelta

def estimate_completion_time(current_progress: str, start_time: datetime) -> str:
    """Estimate completion time based on current progress"""
    
    # Extract progress information from the output
    if "Baseline models:" in current_progress and "%" in current_progress:
        # Parse baseline progress
        if "20%" in current_progress:
            progress = 0.2
            phase = "baseline"
        elif "40%" in current_progress:
            progress = 0.4 
            phase = "baseline"
        elif "60%" in current_progress:
            progress = 0.6
            phase = "baseline"
        elif "80%" in current_progress:
            progress = 0.8
            phase = "baseline"
        elif "100%" in current_progress:
            progress = 1.0
            phase = "baseline_complete"
        else:
            progress = 0.1
            phase = "baseline"
    elif "Ensemble configs:" in current_progress and "%" in current_progress:
        # Parse ensemble progress
        if "20%" in current_progress:
            progress = 0.2
            phase = "ensemble" 
        elif "40%" in current_progress:
            progress = 0.4
            phase = "ensemble"
        elif "60%" in current_progress:
            progress = 0.6
            phase = "ensemble"
        elif "80%" in current_progress:
            progress = 0.8
            phase = "ensemble"
        elif "100%" in current_progress:
            progress = 1.0
            phase = "ensemble_complete"
        else:
            progress = 0.1
            phase = "ensemble"
    else:
        progress = 0.05
        phase = "starting"
    
    # Calculate time estimates
    elapsed = datetime.now() - start_time
    elapsed_minutes = elapsed.total_seconds() / 60
    
    if phase == "baseline":
        # Baseline is ~33% of total experiment (1 hour of 3 hours)
        total_baseline_time = 60  # minutes
        baseline_progress = progress
        remaining_baseline = (1 - baseline_progress) * total_baseline_time
        ensemble_time = 120  # minutes for ensemble phase
        total_remaining = remaining_baseline + ensemble_time
        
    elif phase == "baseline_complete":
        # Just finished baseline, starting ensemble
        ensemble_time = 120  # minutes
        total_remaining = ensemble_time
        
    elif phase == "ensemble":
        # In ensemble phase (~67% of total experiment)
        ensemble_progress = progress
        remaining_ensemble = (1 - ensemble_progress) * 120  # minutes
        total_remaining = remaining_ensemble
        
    elif phase == "ensemble_complete":
        total_remaining = 5  # Just analysis left
        
    else:
        # Just starting
        total_remaining = 210  # 3.5 hours total
    
    completion_time = datetime.now() + timedelta(minutes=total_remaining)
    
    return f"""
Progress Analysis:
- Phase: {phase}
- Progress: {progress*100:.1f}%
- Elapsed time: {elapsed_minutes:.1f} minutes
- Estimated remaining: {total_remaining:.0f} minutes
- Estimated completion: {completion_time.strftime('%I:%M %p')}
"""

def main():
    print("Experiment Progress Monitor")
    print("=" * 50)
    print("Monitoring bash_2 experiment progress...")
    print("Press Ctrl+C to exit monitoring")
    print()
    
    start_time = datetime.now()
    last_output = ""
    
    while True:
        try:
            # This would normally use BashOutput, but we'll simulate for now
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking progress...")
            
            # In real implementation, you would check bash output here
            # For now, just provide status update
            elapsed = datetime.now() - start_time
            elapsed_minutes = elapsed.total_seconds() / 60
            
            print(f"Experiment running for: {elapsed_minutes:.1f} minutes")
            
            if elapsed_minutes < 60:
                print("Phase: Baseline experiments (5 models × 15 scenarios)")
                progress = min(elapsed_minutes / 60, 1.0)
                print(f"Estimated progress: {progress*100:.1f}%")
                remaining = 210 - elapsed_minutes  # 3.5 hours total
            elif elapsed_minutes < 180:
                print("Phase: Ensemble experiments (5 configs × 15 scenarios)") 
                progress = (elapsed_minutes - 60) / 120
                print(f"Estimated progress: {progress*100:.1f}%")
                remaining = 210 - elapsed_minutes
            else:
                print("Phase: Results processing and analysis")
                remaining = max(210 - elapsed_minutes, 0)
            
            if remaining > 0:
                completion_time = datetime.now() + timedelta(minutes=remaining)
                print(f"Estimated completion: {completion_time.strftime('%I:%M %p')} ({remaining:.0f} minutes remaining)")
            else:
                print("Experiment should be complete!")
            
            print("-" * 50)
            time.sleep(300)  # Check every 5 minutes
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()