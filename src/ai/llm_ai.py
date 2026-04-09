from src.utils.app_types import EAIDifficulty, TCoord, TRemainingCells
from ollama import chat, ChatResponse
from typing import List, Dict
import json

class LLMM_AI:
    def __init__(self, difficulty: EAIDifficulty, model: str = "mixtral:8x22b"):
        self.difficulty = difficulty
        self.model = model

    def _build_prompt(self, board: TRemainingCells, remaining_ships: List[str]) -> str:
        return f"""
You are an expert Battleship player. You play very strategically.
You analyze the board carefully for patterns and ship positions.
You follow up on hits aggressively to sink ships.
You use logic and probability to guess where unseen ships might be.
Your success rate is 80%+.

Only take board data as input, do not hallucinate or make assumptions.
Only use remaining coordinates as possible targets.

- Battleship: 4 cells
- Cruiser: 3 cells
- Submarine: 3 cells
- Destroyer: 2 cells

Current board state:
- Hits: {board['hits']}
- Missed shots: {board['missed_shots']}
- Remaining unknown cells: {board['remaining']}

Remaining ships you know are still afloat:
- Remaining ships: {remaining_ships}

Analyze the board. Look for patterns:
1. Where have you hit before? Follow those hits to find and sink ships.
2. Where should the remaining ships be? Use logic to predict.
3. Which cells give you the best chances?

Think like a real player. Make your next attack decision.

{{"row": string, "column": string}}

"""
        
    def get_next_attack(self, board : TRemainingCells, remaining_ships: List[str]) -> TCoord:
        prompt = self._build_prompt(board, remaining_ships)
        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0
            },
            stream=False
            
        )
        return response.message.content