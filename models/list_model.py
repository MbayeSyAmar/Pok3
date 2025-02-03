class ListModel:
    def __init__(self, list_id, title, position, board_id):
        self.id = list_id
        self.title = title
        self.position = position
        self.board_id = board_id
        self.cards = []

    def add_card(self, card_model):
        self.cards.append(card_model)

    def remove_card(self, card_model):
        self.cards.remove(card_model)

    def get_card_by_id(self, card_id):
        return next((card_model for card_model in self.cards if card_model.id == card_id), None)

