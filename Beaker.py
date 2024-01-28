"""
    Author:     Brian Mburu
    Date:       28/01/2024
    Overview:   An implementation of the beaker object and related methods.
    Context:    Its an attempt to recreate some of the mechanics in liquid transfer puzzle games.
                The beaker object is primarily a list.
                Elements in this list represent sections and the values represent liquids.
                Empty spaces are denoted as zero while liquids are +ve intagers.
                The top of most section in the beaker is index 0 while the lowest is len(beaker).
"""

class BeakerMethods:
    """ Conatins static methods for managing beaker and beaker actions. """

    @staticmethod
    def check_is_full(beaker):
        """ Checks if the beaker is full """
        return beaker[0] != 0


    @staticmethod
    def check_is_empty(beaker):
        """ Checks if the beaker is empty """
        return beaker[-1] == 0


    @staticmethod
    def get_top_liquid(beaker):
        """ Get the top most liquid in beaker """
        for idx, section in enumerate(beaker):
            if section != 0:
                return (idx, section)
        return (len(beaker) -1, 0)


    @staticmethod
    def check_is_solved(beaker):
        """ Check if the beaker contains a liquid of the same type in all the sections. """
        is_solved = False

        is_empty = BeakerMethods.check_is_empty(beaker)
        not_full = not BeakerMethods.check_is_full(beaker)
        if is_empty or not_full:
            return is_solved

        # if all colors are the same as the first then its locked
        top_liquid = BeakerMethods.get_top_liquid(beaker)[-1]
        for liquid in beaker:
            if top_liquid != liquid:
                return is_solved

        is_solved = True
        return is_solved


    @staticmethod
    def check_is_miscible(source, destination):
        """ Check if two beakers contain miscible liquids at the top """
        source_top_liquid = BeakerMethods.get_top_liquid(source)[-1]
        destination_top_liquid = BeakerMethods.get_top_liquid(destination)[-1]
        return source_top_liquid == destination_top_liquid


    @staticmethod
    def transfer_liquid(source, destination):
        """ Transfers liquid form on beaker to the other. """
        destination_is_full = BeakerMethods.check_is_full(destination)
        destination_is_solved = BeakerMethods.check_is_solved(destination)
        source_is_empty = BeakerMethods.check_is_empty(source)
        source_is_solved = BeakerMethods.check_is_solved(source)

        if(destination_is_full or source_is_empty or destination_is_solved or source_is_solved):
            return [source, destination]

        # the liquids can be transfered
        destination_is_empty = BeakerMethods.check_is_empty(destination)
        liquids_are_miscible = BeakerMethods.check_is_miscible(source, destination)
        if(destination_is_empty or liquids_are_miscible):
            source_top_liquid_idx, source_top_liquid = BeakerMethods.get_top_liquid(source)
            destination_top_liquid_idx, _ = BeakerMethods.get_top_liquid(destination)
            # Transfer the liquid to destination and remove from source.
            source[source_top_liquid_idx] = 0
            if destination_is_empty:
                destination[destination_top_liquid_idx]  = source_top_liquid
            else:
                destination[destination_top_liquid_idx - 1]  = source_top_liquid

        # Continue transterirng the liquid untill
        still_miscible = BeakerMethods.check_is_miscible(source, destination)
        if still_miscible:
            return BeakerMethods.transfer_liquid(source, destination)

        #  No more transfers can be made.
        return[source, destination]


class Beaker(BeakerMethods):
    """ Creates a beaker object implements the methods """
    def __init__(self, beaker):
        self.beaker = beaker
        self.capacity = len(beaker)


    def __repr__(self):
        return str(self.beaker)


    def __getitem__(self, key):
        return self.beaker[key]


    def __setitem__(self, key, value):
        self.beaker[key] = value
        return self.beaker

    def __len__(self):
        return len(self.beaker)

    def is_empty(self):
        """ Checks if the beaker object is has no liquids """
        return super().check_is_empty(self.beaker)


    def is_full(self):
        """ Checks if the beaker object is full """
        return super().check_is_full(self.beaker)


    def top_liquid(self):
        """ Returns top most liquid and its index """
        return super().get_top_liquid(self.beaker)

    def is_solved(self):
        """ Checks if all segments in the beaker contain the same liquid. """
        return super().check_is_solved(self.beaker)
