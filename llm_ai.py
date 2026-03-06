from unittest import result

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient

from app_types import EAIDifficulty, TCoord, TRemainingCells
from ollama import chat, ChatResponse
import json


class LLMM_AI:
    def __init__(self, difficulty: EAIDifficulty, model: str = "gemma2:9b"):
        self.difficulty = difficulty
        self.model = model

        self._config_list = {
                "model": self.model,
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "model_info": {
                    "family": "ollama",
                    "max_tokens": 8192,
                    "token_limit": 8192,
                    "context_window": 8192,
                    "json_output": True,
                    "vision": False,
                    "function_calling": True
                }
            }
        
        model_client = OllamaChatCompletionClient(**self._config_list)

        self._admiral = AssistantAgent(
            name="Admiral",
            system_message="""You are a Battleship strategist.
            1. Use 'check_board' to see the current state.
            2. Use 'get_valid_moves' to ensure you don't repeat shots.
            3. Once you have a target, reply ONLY with: SHOT: {"row": "a-j", "column": 1-10}""",
            model_client=model_client
        )

        

    def _build_prompt(self, board: TRemainingCells) -> str:
        return f"""
You are an AI playing Battleship.

Board:
{board}

Your goal is to finde following ships on the borad:

Following ship exist:
  |- Carrier: 5 cells                      
  |- Battleship: 4 cells                   
  |- Cruiser: 3 cells                      
  |- Submarine: 3 cells                    
  |- Destroyer: 2 cells  

Give a prediction for the next attack in format:
{{"row": "a-j", "column": 1-10}}
DO not give any explanation, only the prediction in the specified format.
"""
        
    async def get_next_attack(self, board : TRemainingCells) -> TCoord:

        prompt = self._build_prompt(board)
        result = await self._admiral.run(task=prompt)
        print("LLMM_AI result:", result)
        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.message.content