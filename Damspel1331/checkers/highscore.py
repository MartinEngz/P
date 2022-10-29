
class HighscoreManager:
    """
    HighscoreManager instance is initialized in update() method of Menu class if menu.game has a winner. 
    
    If there is a winner in the game, the winner time and the current board size is passed 
    to an instance of this class to update a txt file where each valid board size has its own highscore list. If the 
    passed board size is invalid, no highscore list is updated. If there is no highscore file of txt format, the 
    program calls a method for creating a txt file by a given template structure that is compatible with the sorting 
    methods.
    """
    def __init__(self, filename, board_size, new_score):
        """

        Parameters:
            filename: str
                Path to highscore file to be updated.
            board_size: tuple
                Representation of current board size in format (ROWS, COLUMNS).
            new_score: str
                Winner time of finished game in format h:mm:ss.
        
        Initialized instance variables:
            self.filename: see filename parameter
            self.inv_board_size_options: dictionary
                This dictionary does the reverse of the board_size_options dictionary defined in the menu module. Given a
                board size tuple, this dictionary maps the tuple to its corresponding string which is used to find the
                highscore list of the correct board size in the txt file to update.
            self.board_size: see board_size parameter
            self.new_score: see new_score parameter
        """

        self.filename = filename
        self.inv_board_size_options = {(8, 8): '8x8', (10, 10): '10x10', (12, 12): '12x12'}
        try:
            self.board_size = self.inv_board_size_options[board_size]
            self.new_score = new_score
            self.update_highscore()
        except KeyError:
            pass
        except FileNotFoundError:
            self.create_highscore_file()
            self.update_highscore()
        

    def update_highscore(self):
        """
        The highest-level method of updating highscore and runs according to the following workflow. 
            - First, the content of the txt file is converted into a list of three strings corresponding 
            each highscore list. 
            - Out of this list, the string containing the highscore list by relevant size is picked out 
            together with its index in the list. 
            - The highscore list by size is modified by adding the new score and sorting. 
            - The modified list is then replacing its original self in the list with all highscore
            lists. 
            - This final list is then written to a target txt file.
        """
        all_highscore_lists = self.txt_to_str_list() # FileNotFoundError if file does not exist
        idx, highscore_by_size = self.get_highscore_by_size(all_highscore_lists) # makes KeyError if input board_size does not have a hs list in txt file
        modified_highscore = self.update_highscore_by_size(highscore_by_size)
        all_highscore_lists[idx] = modified_highscore
        self.write_to_txt_file(all_highscore_lists)

    def txt_to_str_list(self):
        """
        Converts txt file content to list of highscore lists by size.
    
        Output:
            all_lists: list (of strings)
                List of the three highscore lists as strings in increasing board size order. 
        """
        with open(self.filename) as file:
            long_str = file.read()
        all_hs_lists = long_str.split('========================\n')
        return all_hs_lists
        
    def get_highscore_by_size(self, all_hs_lists):
        """
        From all_hs_lists, picks out the highscore list for relevant board size.

        Parameters: 
            all_lists: list (of strings)
                List of the three highscore lists as strings in increasing board size order. 

        Output:
            idx: int
                Index in all_hs_lists from where the relevant board size highscore list is taken from.
            highscore_by_size: str
                Highscore list for relevant board size to be updated.
        """
        for idx, highscore_by_size in enumerate(all_hs_lists):
            if f"Highscore by size {self.board_size}:" in highscore_by_size:
                return idx, highscore_by_size

    def update_highscore_by_size(self, highscore_by_size):
        """
        Updates highscore list by size by adding the new score to it and then sorting it.

        Parameters:
            highscore_by_size: str
                Highscore list for relevant board size to be updated.

        Output:
            modified_highscore: str
                Sorted highscore list for relevant board size with the new score taken into account. 
        """
        rows = highscore_by_size.split('\n')
        rows = [row for row in rows if row]
        title = rows[0]
        rows = rows[1:len(rows)+1] # during sorting, exclude title row: f"Highscore by size {board_size}"
        for i, row in enumerate(rows):
            row = row.replace(" ", "").split("-")
            rows[i] = row[1]
        rows.append(self.new_score)
        rows.sort()

        if len(rows) > 10:
            rows = rows[0:10] # In order to not be excessive and unnecessarily long, each highscore list is
                              # limited to ten elements, i.e a top ten list.
        for i, row in enumerate(rows):
            rows[i] = f"{i+1} - {row}"
        modified_highscore = title + '\n' + '\n'.join(rows) + '\n'

        return modified_highscore
        

    def write_to_txt_file(self, all_hs_lists):
        """
        Compiles the all_hs_lists list to a single properly formatted string that is written to the taget
        text file.

        Parameters:
            all_lists: list (of strings)
                List of the three highscore lists as strings in increasing board size order.
        """
        final_str = '========================\n'.join(all_hs_lists)
        with open(self.filename, 'w') as file:
            file.writelines(final_str)

    def create_highscore_file(self):
        """
        Creates the text file with the template structure compatible with the methods for updating the
        highscore list.
        """
        template_str = ""
        for board_size in self.inv_board_size_options.values:
            template_str += "========================\n"
            template_str += f"Highscore by size {board_size}:\n\n"
        with open(self.filename, 'w') as file:
            file.write(template_str)