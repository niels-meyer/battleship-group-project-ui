import random
from enum import Enum
from typing import List, Set

from utils.app_types import EAIDifficulty, TBoard, TCoordIndex


class AIStrategy(Enum):
    # Enum for high-level AI behavior.

    SEARCH = "search"
    DESTROY = "destroy"


class SimpleBattleshipAI:
    # Battleship AI with NORMAL, HARD and IMPOSSIBLE difficulties.

    def __init__(self, board_size: int = 10, difficulty: EAIDifficulty = EAIDifficulty.NORMAL):
        self.board_size = board_size
        self.difficulty = difficulty
        self.current_strategy = AIStrategy.SEARCH
        self.last_shots: Set[TCoordIndex] = set()

    # Choose the next shot from current board state.
    def decide_shot(self, board: TBoard) -> TCoordIndex:

        self._update_shots_fired(board)

        if self.difficulty == EAIDifficulty.IMPOSSIBLE:
            self.current_strategy = AIStrategy.DESTROY
            return self._impossible_shot(board)

        return self._strategic_shot(board, deterministic=self.difficulty == EAIDifficulty.HARD)

    def _strategic_shot(self, board: TBoard, deterministic: bool) -> TCoordIndex:
        # Shared logic for NORMAL and HARD modes.

        hits = self._find_unsunk_hits(board)

        if hits:
            self.current_strategy = AIStrategy.DESTROY
            shot = self._destroy_shot(hits)
            if shot is not None:
                return shot

        self.current_strategy = AIStrategy.SEARCH
        return self._search_shot(board, deterministic=deterministic)

    def _impossible_shot(self, board: TBoard) -> TCoordIndex:
        # Cheat mode: pick any unshot ship cell first.
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                if coords in self.last_shots:
                    continue
                if board[row][col]["ship"] is not None:
                    return coords

        return self._first_unshot_cell()

    def _update_shots_fired(self, board: TBoard) -> None:
        # Update local shot history from board state.
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col]["is_shot"]:
                    self.last_shots.add((row, col))

    def _find_unsunk_hits(self, board: TBoard) -> List[TCoordIndex]:
        # Return all shot cells that still contain a ship.
        hits = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = board[row][col]
                if cell["is_shot"] and cell["ship"] is not None:
                    hits.append((row, col))
        return hits

    def _destroy_shot(self, hits: List[TCoordIndex]) -> TCoordIndex | None:
        # Target around known hits to finish ships quickly.
        groups = self._group_adjacent_hits(hits)
        if not groups:
            return None

        groups.sort(key=lambda group: (-len(group), sorted(group)))

        for group in groups:
            extending = self._find_group_extension(group)
            if extending is not None:
                return extending

            adjacent = self._find_group_adjacent(group)
            if adjacent is not None:
                return adjacent

        return None

    def _group_adjacent_hits(self, hits: List[TCoordIndex]) -> List[List[TCoordIndex]]:
        # Group hits by 4-neighbor adjacency.
        hit_set = set(hits)
        visited: Set[TCoordIndex] = set()
        groups: List[List[TCoordIndex]] = []

        for start in sorted(hit_set):
            if start in visited:
                continue

            queue = [start]
            visited.add(start)
            group: List[TCoordIndex] = []

            while queue:
                row, col = queue.pop(0)
                group.append((row, col))

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row + dr, col + dc
                    neighbor = (nr, nc)
                    if neighbor in hit_set and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            groups.append(sorted(group))

        return groups

    def _find_group_extension(self, group: List[TCoordIndex]) -> TCoordIndex | None:
        # If group has a line, extend that line first.
        if len(group) < 2:
            return None

        rows = {row for row, _ in group}
        cols = {col for _, col in group}

        if len(rows) == 1:
            row = next(iter(rows))
            min_col = min(col for _, col in group)
            max_col = max(col for _, col in group)
            for candidate in [(row, max_col + 1), (row, min_col - 1)]:
                if self._is_valid_unshot(candidate):
                    return candidate

        if len(cols) == 1:
            col = next(iter(cols))
            min_row = min(row for row, _ in group)
            max_row = max(row for row, _ in group)
            for candidate in [(max_row + 1, col), (min_row - 1, col)]:
                if self._is_valid_unshot(candidate):
                    return candidate

        return None

    def _find_group_adjacent(self, group: List[TCoordIndex]) -> TCoordIndex | None:
        # Pick first valid adjacent unshot cell around group.
        for row, col in sorted(group):
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                candidate = (row + dr, col + dc)
                if self._is_valid_unshot(candidate):
                    return candidate
        return None

    def _search_shot(self, board: TBoard, deterministic: bool) -> TCoordIndex:
        # Search mode with simple checkerboard-based scoring.
        checker_candidates = [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if (row, col) not in self.last_shots and (row + col) % 2 == 0
        ]

        candidates = checker_candidates or [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if (row, col) not in self.last_shots
        ]

        if not candidates:
            return (0, 0)

        if deterministic:
            return max(candidates, key=lambda coords: self._basic_cell_score(coords[0], coords[1], board))

        weighted_candidates = []
        for row, col in candidates:
            weight = self._basic_cell_score(row, col, board) + random.uniform(0.0, 0.6)
            weighted_candidates.append(max(0.01, weight))

        return random.choices(candidates, weights=weighted_candidates, k=1)[0]

    def _basic_cell_score(self, row: int, col: int, board: TBoard) -> float:
        # Simple score: checkerboard priority + nearby-hit bonus + center proximity + heat map.
        score = 1.0

        # Checkerboard priority
        if (row + col) % 2 == 0:
            score += 0.5

        # Proximity to center
        center = (self.board_size - 1) / 2
        dist = abs(row - center) + abs(col - center)
        max_dist = self.board_size - 1
        score += (max_dist - dist) * 0.3  # Weight for center proximity

        # Nearby hits (heat map effect)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                if board[nr][nc]["is_shot"]:
                    if board[nr][nc]["ship"] is not None:
                        score += 0.5  # Higher weight for nearby hits
                    else:
                        score -= 0.2  # Penalize for being near a missed shot

        return score

    def _is_valid_unshot(self, coords: TCoordIndex) -> bool:
        row, col = coords
        return (
            0 <= row < self.board_size
            and 0 <= col < self.board_size
            and coords not in self.last_shots
        )

    # Fallback for IMPOSSIBLE mode if no unshot ship cells found (should not happen in normal play)
    def _first_unshot_cell(self) -> TCoordIndex:
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) not in self.last_shots:
                    return (row, col)
        return (0, 0)

    def reset(self) -> None:
        # Reset AI state for a new game.
        self.last_shots.clear()
        self.current_strategy = AIStrategy.SEARCH
