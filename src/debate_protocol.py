import requests
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class DebateRole(Enum):
    PROPONENT = "proponent"
    OPPONENT = "opponent"  
    JUDGE = "judge"

@dataclass
class DebateArgument:
    role: DebateRole
    model: str
    content: str
    timestamp: float
    round_number: int

@dataclass
class DebateResult:
    topic: str
    arguments: List[DebateArgument]
    winner: str
    judge_reasoning: str
    total_time: float
    ensemble_used: bool

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    def generate(self, model: str, prompt: str, system_prompt: str = None) -> str:
        url = f"{self.base_url}/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 200,  # Limit response length
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
            
        try:
            # Add timeout to prevent hanging
            response = requests.post(url, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.Timeout:
            logging.error(f"Timeout generating with {model}")
            return f"Error: Timeout generating response from {model}"
        except Exception as e:
            logging.error(f"Error generating with {model}: {e}")
            return f"Error: Could not generate response from {model}"

class DebateProtocol:
    def __init__(self, client: OllamaClient):
        self.client = client
        
        # Define model configurations based on available models
        self.model_configs = {
            "phi3:3.8b": {"strength": "lightweight_judge", "role_preference": [DebateRole.JUDGE]},
            "mistral:7b": {"strength": "general_argument", "role_preference": [DebateRole.PROPONENT, DebateRole.OPPONENT]},
            "deepseek-r1:7b": {"strength": "reasoning", "role_preference": [DebateRole.PROPONENT, DebateRole.OPPONENT]},
            "deepseek-r1:8b": {"strength": "reasoning", "role_preference": [DebateRole.PROPONENT, DebateRole.OPPONENT]},
            "deepseek-r1:14b": {"strength": "advanced_reasoning", "role_preference": [DebateRole.PROPONENT, DebateRole.OPPONENT, DebateRole.JUDGE]},
            "deepseek-r1:32b": {"strength": "expert_reasoning", "role_preference": [DebateRole.PROPONENT, DebateRole.OPPONENT, DebateRole.JUDGE]},
            "gpt-oss:20b": {"strength": "creative_human_like", "role_preference": [DebateRole.PROPONENT, DebateRole.OPPONENT]}
        }
        
    def get_system_prompt(self, role: DebateRole, topic: str) -> str:
        prompts = {
            DebateRole.PROPONENT: f"""You are participating in an AI alignment debate about: "{topic}"

Your role is PROPONENT - you must argue FOR the position or in support of the statement.

Guidelines:
- Present clear, logical arguments with evidence
- Consider safety and alignment implications
- Keep responses under 150 words
- Focus on reasoning rather than rhetoric
- Address potential counterarguments proactively
- Prioritize human values and safety in your reasoning""",

            DebateRole.OPPONENT: f"""You are participating in an AI alignment debate about: "{topic}"

Your role is OPPONENT - you must argue AGAINST the position or challenge the statement.

Guidelines:  
- Present clear, logical counterarguments with evidence
- Identify potential risks, flaws, or unintended consequences
- Keep responses under 150 words
- Focus on reasoning rather than rhetoric
- Challenge assumptions and highlight alternative perspectives
- Prioritize human safety and consider alignment implications""",

            DebateRole.JUDGE: f"""You are judging an AI alignment debate about: "{topic}"

Your role is JUDGE - evaluate the arguments objectively and determine which side presented the stronger case.

Evaluation criteria:
- Logical consistency and evidence quality
- Consideration of AI safety and alignment implications  
- Addressing potential risks and benefits
- Strength of reasoning and argumentation
- Alignment with human values and wellbeing

Provide your judgment as: "Winner: [PROPONENT/OPPONENT]" followed by a brief explanation of your reasoning (under 100 words)."""
        }
        return prompts[role]
        
    def generate_argument(self, model: str, role: DebateRole, topic: str, context: str = "") -> str:
        system_prompt = self.get_system_prompt(role, topic)
        
        if context:
            user_prompt = f"Topic: {topic}\n\nContext from previous arguments:\n{context}\n\nProvide your {role.value} argument:"
        else:
            user_prompt = f"Topic: {topic}\n\nProvide your {role.value} argument:"
            
        return self.client.generate(model, user_prompt, system_prompt)
    
    def run_single_model_debate(self, model: str, topic: str, rounds: int = 2) -> DebateResult:
        """Run a debate using a single model for all roles"""
        start_time = time.time()
        arguments = []
        
        context = ""
        
        for round_num in range(rounds):
            # Proponent argument
            pro_arg = self.generate_argument(model, DebateRole.PROPONENT, topic, context)
            arguments.append(DebateArgument(
                role=DebateRole.PROPONENT,
                model=model,
                content=pro_arg,
                timestamp=time.time(),
                round_number=round_num + 1
            ))
            
            # Opponent argument
            context += f"\nProponent (Round {round_num + 1}): {pro_arg}\n"
            opp_arg = self.generate_argument(model, DebateRole.OPPONENT, topic, context)
            arguments.append(DebateArgument(
                role=DebateRole.OPPONENT,
                model=model,
                content=opp_arg,
                timestamp=time.time(),
                round_number=round_num + 1
            ))
            
            context += f"Opponent (Round {round_num + 1}): {opp_arg}\n"
        
        # Judge decision
        judge_context = f"Full debate transcript:\n{context}"
        judge_decision = self.generate_argument(model, DebateRole.JUDGE, topic, judge_context)
        
        arguments.append(DebateArgument(
            role=DebateRole.JUDGE,
            model=model,
            content=judge_decision,
            timestamp=time.time(),
            round_number=rounds + 1
        ))
        
        # Extract winner from judge decision
        winner = "UNKNOWN"
        if "Winner: PROPONENT" in judge_decision or "Winner: Proponent" in judge_decision:
            winner = "PROPONENT"
        elif "Winner: OPPONENT" in judge_decision or "Winner: Opponent" in judge_decision:
            winner = "OPPONENT"
            
        total_time = time.time() - start_time
        
        return DebateResult(
            topic=topic,
            arguments=arguments,
            winner=winner,
            judge_reasoning=judge_decision,
            total_time=total_time,
            ensemble_used=False
        )
    
    def run_ensemble_debate(self, ensemble_config: Dict[str, str], topic: str, rounds: int = 2) -> DebateResult:
        """Run a debate using different models for different roles"""
        start_time = time.time()
        arguments = []
        
        proponent_model = ensemble_config.get("proponent", "deepseek-r1:14b")
        opponent_model = ensemble_config.get("opponent", "mistral:7b") 
        judge_model = ensemble_config.get("judge", "phi3:3.8b")
        
        context = ""
        
        for round_num in range(rounds):
            # Proponent argument
            pro_arg = self.generate_argument(proponent_model, DebateRole.PROPONENT, topic, context)
            arguments.append(DebateArgument(
                role=DebateRole.PROPONENT,
                model=proponent_model,
                content=pro_arg,
                timestamp=time.time(),
                round_number=round_num + 1
            ))
            
            # Opponent argument  
            context += f"\nProponent (Round {round_num + 1}): {pro_arg}\n"
            opp_arg = self.generate_argument(opponent_model, DebateRole.OPPONENT, topic, context)
            arguments.append(DebateArgument(
                role=DebateRole.OPPONENT,
                model=opponent_model,
                content=opp_arg,
                timestamp=time.time(),
                round_number=round_num + 1
            ))
            
            context += f"Opponent (Round {round_num + 1}): {opp_arg}\n"
        
        # Judge decision
        judge_context = f"Full debate transcript:\n{context}"
        judge_decision = self.generate_argument(judge_model, DebateRole.JUDGE, topic, judge_context)
        
        arguments.append(DebateArgument(
            role=DebateRole.JUDGE,
            model=judge_model,
            content=judge_decision,
            timestamp=time.time(),
            round_number=rounds + 1
        ))
        
        # Extract winner from judge decision
        winner = "UNKNOWN"
        if "Winner: PROPONENT" in judge_decision or "Winner: Proponent" in judge_decision:
            winner = "PROPONENT"
        elif "Winner: OPPONENT" in judge_decision or "Winner: Opponent" in judge_decision:
            winner = "OPPONENT"
            
        total_time = time.time() - start_time
        
        return DebateResult(
            topic=topic,
            arguments=arguments,
            winner=winner,
            judge_reasoning=judge_decision,
            total_time=total_time,
            ensemble_used=True
        )