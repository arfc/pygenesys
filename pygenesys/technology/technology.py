
#==============================================================================
#==============================================================================
# Defines Technology
#==============================================================================
#==============================================================================
class Technology(object):
    """
    This class holds the information for technologies
    in a Temoa simulation. A ``Technology`` transforms
    one energy carrier into another. E.g. a nuclear plant
    might transform a uranium commodity into heat or electricity.
    """

    def __init__(self,
                 tech_name,
                 input_comm,
                 output_comm,
                 units,
                 tech_label='p',
                 description='',
                 category=''):
        """
        This class contains information about a technology used
        in a Temoa model.

        Parameters
        ----------
        tech_name : string
            The name of the technology
        tech_label : string
            The label of the technology. Describes how the technology
            is used in Temoa. Currently accepts:
            * 'r' (resource import)
            * 'p' (production, general)
            * 'ps' (production, storage)
            * 'pb' (production, baseload)

        """
