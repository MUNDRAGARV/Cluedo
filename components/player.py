class Player:
    """Describe a player and the cards he/she owns"""

    def __init__(self, name: str, number_of_cards: int):
        self.name = name
        self.number_of_cards = number_of_cards
        self.cards_owned = [set() for _ in range(number_of_cards)]
        self.cards_not_owned = set()

    @property
    def all_cards_known(self) -> bool:
        """Returns true if all the player's cards are known"""
        if self.cards_owned == [x for x in self.cards_owned if len(x) == 1]:
            return True
        return False

    def add_cards_not_owned(self, cards: set) -> None:
        """Add ore or more cards to the list of the not owned ones."""
        self.cards_not_owned = self.cards_not_owned.union(set(cards))
        self.remove_cards_owned(cards)

    def remove_cards_owned(self, cards: set) -> None:
        """Remove one or more cards from the list of the owned ones."""
        # Remove not owned cards from the owned ones
        self.cards_owned = [slot.difference(cards) for slot in self.cards_owned]

    def add_cards_owned(self, cards: set) -> None:
        """Add one or more cards from the list of the owned ones."""
        # Clean the incoming cards from the ones not owned
        cards = cards.difference(self.cards_not_owned)
        # Do nothing if same card(s) are already registered
        if cards in self.cards_owned:
            return

        for slot_ind, slot in enumerate(self.cards_owned):
            # If cards is more informative than an existing slot, replace it
            if cards.issubset(slot):
                self.cards_owned[slot_ind] = cards
            # Looking for the first empty slot not to overwrite info
            elif not slot:
                self.cards_owned[slot_ind] = self.cards_owned[slot_ind].union(cards)

        # Apply cleaning
        self.remove_redundant_information()

    def remove_redundant_information(self):
        """Remove redundant information generated by card adding process"""
        for slot_ind, slot in enumerate(self.cards_owned[:-1]):
            slot_ind = slot_ind + 1
            for counter, comp_slot in enumerate(self.cards_owned[slot_ind:]):
                if slot == comp_slot or slot.issubset(comp_slot):
                    self.cards_owned[slot_ind + counter] = set()

    def __str__(self):
        cards_owned = f"\nCards Owned: {self.cards_owned}"
        cards_not_owned = f"\nCards Not Owned: {self.cards_not_owned}"
        info = f"\nAll cards known: {self.all_cards_known}"
        return self.name + cards_owned + cards_not_owned + info

    def __eq__(self, other) -> bool:
        try:
            return self.name == other.name
        except AttributeError:
            return False

    def __ne__(self, other) -> bool:
        try:
            return self.name != other.name
        except AttributeError:
            return True