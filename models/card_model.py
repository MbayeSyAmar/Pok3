class CardModel:
    def __init__(self, card_id, title, description, due_date, position, list_id):
        self.id = card_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.position = position
        self.list_id = list_id
        self.labels = []

    def add_label(self, label):
        self.labels.append(label)

    def remove_label(self, label):
        self.labels.remove(label)

