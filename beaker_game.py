"""
    Author:     Brian Mburu
    Date:       28/01/2024
    Overview:   Implementaion of interaitons between beakers
    Context:    Its an attempt to recreate some of the mechanics in liquid transfer puzzle games.
                There is fixed number of beakers each either empty or with a liquid.
                Transfer of liquid from one beaker to another changes the state of the game. 
                Here I shall attempt to implement the mechanics for transfer and state management.
"""
from beaker import BeakerMethods, Beaker

class BeakerGameStates:
    """ Contains conditions for a game to different states"""
    PLAY:str = "PLAY"
    WON:str = "WON"
    LOST:str = "LOST"

    @staticmethod
    def check_is_won(beakers:list[Beaker])->bool:
        """ Checks if the game is won. 
        Only won if each beaker only contains one liquid type or the beaker is empty """
        for beaker in beakers:
            is_empty = beaker.is_empty()
            is_solved = beaker.is_solved()

            if not(is_empty or is_solved):
                return False

        return True


    @staticmethod
    def check_is_play(beakers:list[Beaker]):
        """ Check if there is at least one valid move. """
        top_liquids = [ beaker.top_liquid() for beaker in beakers ]

        for index_1, liquid_1 in enumerate(top_liquids):
            # Find similar liquids
            for index_2, liquid_2 in enumerate(top_liquids):
                # top liquids, similar types, and space above in atleast one of them.
                is_same_liquid_type = liquid_1[-1] ==  liquid_2[-1]
                is_differnt_container = index_1 != index_2
                has_space = (liquid_1[0] + liquid_2[0]) > 0

                if is_same_liquid_type and is_differnt_container and has_space:
                    return True

        return False

    @staticmethod
    def check_is_lost(beakers):
        """ check if the game is still in play state. """
        if BeakerGameStates.check_is_won(beakers):
            return False
        elif  BeakerGameStates.check_is_play(beakers):
            return False
        else:
            return True




class BeakerGame(BeakerGameStates):
    """ Liquid transfers and state management"""

    def __init__(self, beakers):
        """ initializing the beakers """
        self.beakers = beakers
        self.game_state = self.get_state()


    def __repr__(self):
        return str(self.beakers)


    def __getitem__(self, key):
        return self.beakers[key]


    def __setitem__(self, key, value):
        self.beakers[key] = value
        return self.beakers


    def __len__(self):
        return len(self.beakers)


    def transfer_liquid(self, source_idx, destination_idx):
        """ transfers the liquids, and updates the state. """

        if self.game_state == super().PLAY:
            source, destination = BeakerMethods.transfer_liquid(
                self.beakers[source_idx],
                self.beakers[destination_idx]
            )

            self.beakers[source_idx] = source
            self.beakers[destination_idx] = destination

            self.game_state = self.get_state()

        return self.game_state

    def get_state(self):
        """ Checks which state the game is in. """
        if BeakerGameStates.check_is_won(self.beakers):
            return BeakerGameStates.WON
        elif BeakerGameStates.check_is_play(self.beakers):
            return BeakerGameStates.PLAY
        else:
            return BeakerGameStates.LOST

if __name__ == "__main__":
    beaker_1 = Beaker([0, 2, 1, 1])
    beaker_2 = Beaker([0, 3, 1, 1])
    beaker_3 = Beaker([0, 1, 1, 1])

    beakers = BeakerGame([beaker_1, beaker_2, beaker_3])
    beakers.transfer_liquid(0, 1)
    beakers.transfer_liquid(0, -1)
    print(beakers) # Game is lost

    