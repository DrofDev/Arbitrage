import pandas as pd
from collections import deque
class Matrix:
    def __init__(self, df):
        # Keep the original DataFrame for reference
        self.df = df
        self.matrix = self._convert_to_matrix(df.copy())

    def _convert_to_matrix(self, df):
        df = df.fillna(0)  # Replace NaN with -1
        matrix = df.map(lambda x: 1 if isinstance(x, str) else x).values  # Replace all strings with 1
        return matrix

    def print_matrix(self):
        print(self.matrix)

    def get_matrix(self):
        return self.matrix

    def get_df(self):
        return self.df

    def print_df(self):
        print(self.df)

    def get_currency(self, paths, row, col):
        # Get the base currency from the row index
        base_currency = self.df.iloc[row, 0]  # Adjust as necessary if row index is not the currency

        # Get the quote currency from the column header
        quote_currency = self.df.columns[col]  # Adjust as necessary if column headers are not the currency

        return f"{base_currency}/{quote_currency}"

    def bfs_traverse_matrix(self, start_row, start_col, max_length, conversion=True):
        all_paths = []

        # Queue stores (current_position, path, move count, last_move_was_horizontal, path_visited)
        queue = deque([((start_row, start_col), [(start_row, start_col)], 0, False, set([(start_row, start_col)]))])

        while queue:
            (row, col), path, moves_count, last_move_was_horizontal, path_visited = queue.popleft()

            # Debugging print

            if moves_count == max_length:
                if col == start_col:
                    all_paths.append(path)
                continue  # Stop exploring further for this path

            if last_move_was_horizontal:
                moves = self.get_vertical_moves(row, col)
            else:
                moves = self.get_horizontal_moves(row, col)

            for move in moves:
                new_row, new_col = move
                if (new_row, new_col) not in path_visited:
                    new_path = path + [move]
                    new_path_visited = path_visited.copy()
                    new_path_visited.add((new_row, new_col))
                    queue.append(
                        ((new_row, new_col), new_path, moves_count + 1, not last_move_was_horizontal, new_path_visited))

        if conversion:
            currency_paths = [
                [self.get_currency(all_paths, row, col) for row, col in path]
                for path in all_paths]

        else:
            currency_paths = all_paths

        return currency_paths

    def get_horizontal_moves(self, row, col):
        cols = self.matrix.shape[1]
        current = (row, col)
        moves = []
        for i in range(cols):
            if self.matrix[row][i] == 1 and (row, i) != current:
                moves.append((row, i))
        return moves

    def get_vertical_moves(self, row, col):
        rows = self.matrix.shape[0]
        current = (row, col)
        moves = []
        for i in range(rows):
            if self.matrix[i][col] == 1 and (i, col) != current:
                moves.append((i, col))
        return moves


MEXC = Matrix(df)
MEXC.print_df()

results = MEXC.bfs_traverse_matrix(0, 0, 3, conversion=True)

print("Traversal Results:")
for path in results:
    print(path)