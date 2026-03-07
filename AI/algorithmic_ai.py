import random
from typing import List, Tuple, Optional, Dict, Set
from enum import Enum

class AIStrategy(Enum):
    """Enum for different AI strategies"""
    SEARCH = "search"   # Look for any ship
    DESTROY = "destroy"  # Finish off a damaged ship

class SimpleBattleshipAI:
    """
    Stateless Battleship AI that reads board state directly.
    
    No internal hit/miss tracking - everything is derived from the board.
    """
    
    def __init__(self, board_size: int = 10):
        """Initialize the AI player."""
        self.board_size = board_size
        self.current_strategy = AIStrategy.SEARCH
        self.last_shots: Set[Tuple[int, int]] = set()  # Only track what we've shot
        
    def decide_shot(self, board: Tuple) -> Tuple[int, int]:
        """
        Decide where to shoot based on current board state.
        
        Args:
            board: 10x10 tuple of dicts with keys 'is_shot' and 'ship'
        
        Returns:
            Tuple of (row, col) coordinates for next shot
        """
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
        Search strategy: Randomized checkerboard with corner/edge priority.
        
        Priority order:
        1. Corners (highest priority - statistically good ship placement)
        2. Edges (medium priority - near borders)
        3. Interior (lower priority - fill remaining areas)
        
        Within each zone, randomly select from unshot checkerboard cells.
        """
        # Define priority zones
        corners = [(0, 0), (0, 9), (9, 0), (9, 9)]
        edges = []
        interior = []
        
        # Build edge and interior zones (checkerboard only: row + col is even)
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Skip corners
                if (row, col) in corners:
                    continue
                
                # Checkerboard check: only even sum
                if (row + col) % 2 == 0:
                    # Edge: on border or very close to it
                    if row == 0 or row == 9 or col == 0 or col == 9:
                        edges.append((row, col))
                    else:
                        interior.append((row, col))
        
        # Filter corners to checkerboard pattern
        corners_checkerboard = [c for c in corners if (c[0] + c[1]) % 2 == 0]
        
        # Try in priority order: corners → edges → interior
        for zone in [corners_checkerboard, edges, interior]:
            # Find unshot cells in this zone
            available = [c for c in zone if c not in self.last_shots]
            
            if available:
                return random.choice(available)
        
        # Checkerboard exhausted, try remaining cells in random order
        remaining = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                coords = (row, col)
                if coords not in self.last_shots:
                    remaining.append(coords)
        
        if remaining:
            return random.choice(remaining)
        
        # Fallback (shouldn't happen)
        return (0, 0)
    
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