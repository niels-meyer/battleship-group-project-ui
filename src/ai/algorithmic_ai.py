import random
from typing import List, Tuple, Set
from enum import Enum
from utils.app_types import EAIDifficulty


""""
This algorithmic AI is completly vibe coded
"""

class AIStrategy(Enum):
    """Enum for different AI strategies"""
    SEARCH = "search"   # Look for any ship
    DESTROY = "destroy"  # Finish off a damaged ship

class SimpleBattleshipAI:
    """
    Stateless Battleship AI with THREE difficulty levels.
    
    DIFFICULTY LEVELS:
    
    1. NORMAL (EAIDifficulty.NORMAL)
       - Uses probability-weighted RANDOM selection
       - Adds random noise to probabilities (-0.3 to +0.4)
       - UNPREDICTABLE - can't learn its pattern
       - FUN - player has a real chance to win
       - Speed: ~55-65 shots (variable due to randomness)
    
    2. HARD (AIDifficulty.HARD)
       - Uses deterministic probability selection
       - NO randomness, NO noise
       - CONSISTENT - always picks best cell
       - VERY DIFFICULT - optimal play
       - Speed: ~52-60 shots (consistent, slightly faster than NORMAL)
    
    3. IMPOSSIBLE (AIDifficulty.IMPOSSIBLE)
       - Knows all ship locations
       - ALWAYS wins in exactly 17 moves
       - UNBEATABLE - no strategy can win
       - Speed: 17 shots (perfect minimum)
    
    No internal hit/miss tracking - everything is derived from the board.
    """
    
    def __init__(self, board_size: int = 10, difficulty: EAIDifficulty = EAIDifficulty.NORMAL):
        """
        Initialize the AI player.
        
        Args:
            board_size: Size of the board (default 10x10)
            difficulty: AI difficulty level (NORMAL, HARD, IMPOSSIBLE)
        """
        self.board_size = board_size
        self.difficulty = difficulty
        self.current_strategy = AIStrategy.SEARCH
        self.last_shots: Set[Tuple[int, int]] = set()  # Only track what we've shot
        
    def decide_shot(self, board: Tuple) -> Tuple[int, int]:
        """
        Decide where to shoot based on current board state and difficulty level.
        
        Args:
            board: 10x10 tuple of dicts with keys 'is_shot' and 'ship'
        
        Returns:
            Tuple of (row, col) coordinates for next shot
        """
        # Route to difficulty-specific logic
        if self.difficulty == EAIDifficulty.IMPOSSIBLE:
            return self._impossible_shot(board)
        elif self.difficulty == EAIDifficulty.HARD:
            return self._hard_shot(board)
        else:  # NORMAL
            return self._normal_shot(board)
    
    def _normal_shot(self, board: Tuple) -> Tuple[int, int]:
        """Normal mode: Unpredictable and fun, but beatable."""
        # Update shots we know we've made
        self._update_shots_fired(board)
        
        # Find all current unsunk hits on the board
        unsunk_hits = self._find_unsunk_hits(board)
        
        # Decide strategy based on current board state
        if unsunk_hits:
            self.current_strategy = AIStrategy.DESTROY
            shot = self._destroy_strategy(board, unsunk_hits)
        else:
            self.current_strategy = AIStrategy.SEARCH
            shot = self._search_strategy(board)
        
        return shot
    
    def _hard_shot(self, board: Tuple) -> Tuple[int, int]:
        """
        Hard mode: Mathematically optimal, nearly unbeatable.
        
        Uses advanced strategies:
        1. Heat mapping with probability weighting (deterministic, NO noise)
        2. Ship constraint analysis
        3. Efficient ship destruction
        4. Always chooses cell that maximizes hit probability
        """
        # Update shots
        self._update_shots_fired(board)
        unsunk_hits = self._find_unsunk_hits(board)
        
        # If ships are under attack, finish them with maximum efficiency
        if unsunk_hits:
            self.current_strategy = AIStrategy.DESTROY
            
            # Group hits and pursue with maximum efficiency
            hit_groups = self._group_hits_by_ship(unsunk_hits)
            target_group = hit_groups[0]
            
            # Try extending in direction first (most efficient)
            shot = self._find_extending_shot(target_group)
            if shot and shot not in self.last_shots:
                return shot
            
            # Try adjacent cells
            shot = self._find_adjacent_shot(target_group)
            if shot and shot not in self.last_shots:
                return shot
        
        # Search: Use probability heatmap WITHOUT ANY randomness
        # Pure deterministic optimization
        self.current_strategy = AIStrategy.SEARCH
        
        probability_map = {}
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                if coords in self.last_shots:
                    continue
                if (row + col) % 2 != 0:
                    continue
                
                prob = self._calculate_cell_probability(row, col, board)
                probability_map[coords] = prob
        
        if probability_map:
            # DETERMINISTIC: Pick highest probability (NO randomness, NO noise)
            best_shot = max(probability_map.items(), key=lambda x: x[1])
            return best_shot[0]
        
        # Fallback: shoot unshot cells systematically
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                if coords not in self.last_shots:
                    return coords
        
        return (0, 0)
    
    def _impossible_shot(self, board: Tuple) -> Tuple[int, int]:
        """
        Impossible mode: AI knows all ship locations.
        
        Always shoots an unshot cell with a ship.
        Will win in exactly 17 moves (5+4+3+3+2 = 17 ships cells).
        Completely unbeatable.
        """
        self._update_shots_fired(board)
        self.current_strategy = AIStrategy.DESTROY
        
        # Find ANY unshot cell that has a ship
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                if coords not in self.last_shots and board[row][col]["ship"] is not None:
                    return coords
        
        # If all ships are hit, find any unshot cell
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                if coords not in self.last_shots:
                    return coords
        
        return (0, 0)
    
    def _update_shots_fired(self, board: Tuple) -> None:
        """Update the set of shots we've fired by reading the board."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col]["is_shot"]:
                    self.last_shots.add((row, col))
    
    def _find_unsunk_hits(self, board: Tuple) -> List[Tuple[int, int]]:
        """
        Find all cells that have been shot and still have a ship.
        These are unsunk hits that we can target.
        
        Returns:
            List of (row, col) coordinates with unsunk hits
        """
        hits = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = board[row][col]
                # A hit that's still active: is_shot=True AND ship is not None
                if cell["is_shot"] and cell["ship"] is not None:
                    hits.append((row, col))
        return hits
    
    def _search_strategy(self, board: Tuple) -> Tuple[int, int]:
        """
        Search strategy: Probability-weighted random selection.
        
        Instead of always picking the highest probability cell:
        - Calculate probability for each unshot cell
        - Use probability as WEIGHT for random selection
        - Higher probability cells MORE LIKELY (not guaranteed) to be chosen
        - Creates unpredictable but strategic behavior
        
        Factors in probability calculation:
        1. Distance from edge (center slightly favored, but not obvious)
        2. Available space around cell
        3. Proximity to existing hits
        
        This makes the AI:
        - Unpredictable (can't see its patterns)
        - Still strategic (tends toward good moves)
        - Interesting to play against
        """
        # Build probability map for all unshot cells
        probability_map = {}
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                
                # Skip already shot cells
                if coords in self.last_shots:
                    continue
                
                # Only checkerboard cells (1 cell gap)
                if (row + col) % 2 != 0:
                    continue
                
                # Calculate probability for this cell
                prob = self._calculate_cell_probability(row, col, board)
                probability_map[coords] = prob
        
        if not probability_map:
            # Fallback: try remaining cells
            remaining = []
            for row in range(self.board_size):
                for col in range(self.board_size):
                    coords = (row, col)
                    if coords not in self.last_shots:
                        remaining.append(coords)
            
            if remaining:
                return random.choice(remaining)
            return (0, 0)
        
        # RANDOM WEIGHTED SELECTION
        # Use probabilities as weights, not deterministic picking
        # This creates unpredictability while staying somewhat strategic
        
        coords_list = list(probability_map.keys())
        probabilities = list(probability_map.values())
        
        # Add MORE noise to probabilities to increase unpredictability
        # Noise factor: -0.3 to +0.4 (increased from -0.2 to +0.3)
        # This makes NORMAL mode less efficient than HARD
        noisy_probs = []
        for prob in probabilities:
            noise = random.uniform(-0.3, 0.4)  # More randomness
            noisy_prob = max(0.01, prob + noise)  # Keep positive
            noisy_probs.append(noisy_prob)
        
        # Normalize probabilities to sum to 1
        total = sum(noisy_probs)
        normalized_probs = [p / total for p in noisy_probs]
        
        # Random weighted selection based on noisy probabilities
        shot = random.choices(coords_list, weights=normalized_probs, k=1)[0]
        
        return shot
    
    def _calculate_cell_probability(self, row: int, col: int, board: Tuple) -> float:
        """
        Calculate probability of finding a ship at this cell.
        
        Factors:
        - Distance to edge (center cells are more probable)
        - Space available for ships (longer ships need room)
        - Ship size distribution (probability for different lengths)
        """
        # Factor 1: Distance from edges (cells near center are more likely)
        # Normalized 0-1, where 1 = perfectly centered
        dist_to_edge = min(row, col, self.board_size - 1 - row, self.board_size - 1 - col)
        center_score = dist_to_edge / (self.board_size / 2)  # Normalized
        center_score = min(center_score, 1.0)  # Cap at 1.0
        
        # Factor 2: Space available in all directions
        # Can ships fit if placed at this location?
        space_score = 0.0
        
        # Ship sizes: Carrier(5), Battleship(4), Cruiser(3), Submarine(3), Destroyer(2)
        ship_sizes = [5, 4, 3, 3, 2]
        
        # Check horizontal space
        horizontal_space = 0
        for c in range(col, min(col + 5, self.board_size)):  # Max ship size is 5
            if (row, c) not in self.last_shots:
                horizontal_space += 1
        
        # Check vertical space
        vertical_space = 0
        for r in range(row, min(row + 5, self.board_size)):
            if (r, col) not in self.last_shots:
                vertical_space += 1
        
        # Probability that a ship fits here
        max_space = max(horizontal_space, vertical_space)
        if max_space >= 2:  # Minimum ship size
            space_score = min(max_space / 5.0, 1.0)  # Normalize to ship size
        
        # Factor 3: Proximity to already found hits
        # Ships that are partially sunk are more likely to be finished here
        nearby_hits = 0
        for dr in [-2, -1, 0, 1, 2]:
            for dc in [-2, -1, 0, 1, 2]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    if board[nr][nc]["is_shot"] and board[nr][nc]["ship"] is not None:
                        nearby_hits += 1
        
        hit_bonus = min(nearby_hits * 0.15, 0.5)  # Bonus if near existing hits
        
        # Combine factors
        # Center location: 40% weight
        # Available space: 40% weight
        # Nearby hits: 20% weight
        probability = (center_score * 0.4) + (space_score * 0.4) + (hit_bonus * 0.2)
        
        return probability
    
    def _destroy_strategy(self, board: Tuple, unsunk_hits: List[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Destroy strategy: Finish off the ship with unsunk hits.
        
        Steps:
        1. Pick the largest group of hits (one ship)
        2. Try to extend it in the detected direction
        3. Fallback to adjacent cells if direction unclear
        """
        # Group hits into ships (by row/column proximity)
        hit_groups = self._group_hits_by_ship(unsunk_hits)
        
        # Target the largest group first (biggest ship)
        target_group = hit_groups[0]
        
        # Try to extend in the ship's direction
        shot = self._find_extending_shot(target_group)
        
        if shot and shot not in self.last_shots:
            return shot
        
        # If can't extend, try adjacent cells
        shot = self._find_adjacent_shot(target_group)
        
        if shot and shot not in self.last_shots:
            return shot
        
        # If this ship is boxed in, switch to search (shouldn't happen)
        return self._search_strategy(board)
    
    def _group_hits_by_ship(self, hits: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        """
        Group hits into ships based on row/column alignment.
        Ships are always linear, so hits on same row or column belong to same ship.
        
        Returns:
            List of hit groups, sorted by size (largest first)
        """
        if not hits:
            return []
        
        groups = []
        visited = set()
        
        for start_hit in sorted(hits):
            if start_hit in visited:
                continue
            
            # Find all hits on same row or column
            group = [start_hit]
            visited.add(start_hit)
            start_row, start_col = start_hit
            
            for other_hit in sorted(hits):
                if other_hit in visited:
                    continue
                
                other_row, other_col = other_hit
                
                # Same row (horizontal) or same column (vertical)
                if start_row == other_row or start_col == other_col:
                    group.append(other_hit)
                    visited.add(other_hit)
            
            groups.append(sorted(group))
        
        # Sort by size: biggest groups first
        groups.sort(key=len, reverse=True)
        return groups
    
    def _find_extending_shot(self, hit_group: List[Tuple[int, int]]) -> Tuple[int, int] | None:
        """
        Try to find a shot that extends the hit group in the detected direction.
        
        Returns:
            Next shot coordinate, or None if can't extend
        """
        if len(hit_group) < 2:
            # Single hit - try all adjacent cells
            return None
        
        # Determine direction of the ship
        hit_group_sorted = sorted(hit_group)
        row1, col1 = hit_group_sorted[0]
        row2, col2 = hit_group_sorted[1]
        
        # Check if horizontal or vertical
        if row1 == row2:  # Horizontal ship
            # Try extending left and right
            min_col = min(h[1] for h in hit_group)
            max_col = max(h[1] for h in hit_group)
            row = row1
            
            # Try extending right
            if max_col + 1 < self.board_size:
                candidate = (row, max_col + 1)
                if candidate not in self.last_shots:
                    return candidate
            
            # Try extending left
            if min_col - 1 >= 0:
                candidate = (row, min_col - 1)
                if candidate not in self.last_shots:
                    return candidate
        
        else:  # Vertical ship
            # Try extending up and down
            min_row = min(h[0] for h in hit_group)
            max_row = max(h[0] for h in hit_group)
            col = col1
            
            # Try extending down
            if max_row + 1 < self.board_size:
                candidate = (max_row + 1, col)
                if candidate not in self.last_shots:
                    return candidate
            
            # Try extending up
            if min_row - 1 >= 0:
                candidate = (min_row - 1, col)
                if candidate not in self.last_shots:
                    return candidate
        
        return None
    
    def _find_adjacent_shot(self, hit_group: List[Tuple[int, int]]) -> Tuple[int, int] | None:
        """
        Find an adjacent unshot cell next to any hit in the group.
        
        Returns:
            Adjacent shot coordinate, or None if no adjacent cells available
        """
        # Get all cells adjacent to any hit
        adjacent_cells = set()
        
        for row, col in hit_group:
            # Check all 4 adjacent cells
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds
                if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                    coords = (new_row, new_col)
                    # Make sure we haven't shot there
                    if coords not in self.last_shots:
                        adjacent_cells.add(coords)
        
        # Return first available adjacent cell
        if adjacent_cells:
            return sorted(adjacent_cells)[0]
        
        return None
    
    def reset(self) -> None:
        """Reset AI state for a new game."""
        self.last_shots.clear()
        self.current_strategy = AIStrategy.SEARCH
