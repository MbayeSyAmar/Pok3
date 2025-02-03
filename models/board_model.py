class BoardModel:
    def __init__(self, board_id, title, user_id):
        self.id = board_id
        self.title = title
        self.user_id = user_id
        self.lists = []

    def add_list(self, list_model):
        self.lists.append(list_model)

    def remove_list(self, list_model):
        self.lists.remove(list_model)

    def get_list_by_id(self, list_id):
        return next((list_model for list_model in self.lists if list_model.id == list_id), None)

