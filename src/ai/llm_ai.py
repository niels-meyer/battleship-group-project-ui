import json
import re
from typing import Any
from ollama import chat
from src.utils.app_types import EAIDifficulty, TCoord, TRemainingCells
from src.utils.helpers import parse_coord

class LLM_AI:
    def __init__(self, difficulty: EAIDifficulty, model: str = "llama3.1:8b"):
        self.difficulty = difficulty
        self.model = model

    def _build_prompt(self, board: TRemainingCells, remaining_ships: list[str]) -> str:
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
- Hits: {board["hits"]}
- Missed shots: {board["missed_shots"]}
- Remaining unknown cells: {board["remaining"]}

Remaining ships you know are still afloat:
- Remaining ships: {remaining_ships}

Analyze the board. Look for patterns:
1. Where have you hit before? Follow those hits to find and sink ships.
2. Where should the remaining ships be? Use logic to predict.
3. Which cells give you the best chances?

Think like a real player. Make your next attack decision.

Return exactly one JSON object and nothing else.
Do not include markdown, code fences, comments, or explanation.
Use this format only:

{{"row": "A", "column": "1"}}

"""

    def get_next_attack(self, board: TRemainingCells, remaining_ships: list[str]) -> TCoord | None:
        prompt = self._build_prompt(board, remaining_ships)
        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0
            },
            stream=False
        )
        return self._parse_coord(response.message.content, set(board["remaining"]))

    def _parse_coord(self, llm_output: Any, remaining_cells: set[str]) -> TCoord | None:
        if isinstance(llm_output, dict):
            return self._normalize_coord(llm_output.get("row"), llm_output.get("column"), remaining_cells)

        if isinstance(llm_output, (tuple, list)) and len(llm_output) == 2:
            return self._normalize_coord(llm_output[0], llm_output[1], remaining_cells)

        if not isinstance(llm_output, str):
            return None

        stripped = llm_output.strip()

        try:
            parsed_json = json.loads(stripped)
            coord = self._parse_coord(parsed_json, remaining_cells)
            if coord is not None:
                return coord
        except json.JSONDecodeError:
            pass

        json_match = re.search(r"\{[\s\S]*?\}", stripped)
        if json_match:
            try:
                coord = self._parse_coord(json.loads(json_match.group(0)), remaining_cells)
                if coord is not None:
                    return coord
            except json.JSONDecodeError:
                pass

        coord_match = re.search(r"([A-Za-z])\s*([0-9]+)", stripped)
        if coord_match:
            return self._normalize_coord(coord_match.group(1), coord_match.group(2), remaining_cells)

        return None

    def _normalize_coord(self, row: Any, column: Any, remaining_cells: set[str]) -> TCoord | None:
        try:
            coord = parse_coord(f"{row} {column}")
        except ValueError:
            return None

        key = f"{coord[0]}{coord[1]}"
        return coord if key in remaining_cells else None