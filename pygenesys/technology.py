class Technology(object):
    """
    This class contains attributes to
    characterize a specific technology
    in a system.
    """

    def __init__(self,
                 region_name,
                 technology_name,
                 technology_label,
                 capacity_units,
                 input_commodity,
                 efficiency,
                 output_commodity,
                 capacity_to_activity,
                 capacity_factor,
                 lifetime,
                 lifetime_loan,
                 existing_capacity):
        """
        Parameters
        ----------
        region_name : string
            The name of the region where the 
            technology is located.
        technology_name : string
            The name of the technology.
        technology_label : string
            The label attached to the type of
            technology.
        capacity_units : string
            The units for the capacity of the 
            technology.
        input_commodity : string
            The type of commodity that goes
            into a technology.
        efficiency : float
            The efficiency of the technology.
        output_commodity : string
            The type of commodity that goes
            out of a technology.
        capacity_to_activity : float
            The factor relating capacity and 
            activity.
        capacity_factor : float
            The measure of how often the
            technology runs over time.
        lifetime : float
            The time between when the 
            technology starts running 
            and when it is retired.
        lifetime_loan : float
            t
        existing_capacity : float
            All installed, in-service, generating 
            capacity.
        """

        self.region_name = region_name
        self.technology_name = technology_name
        self.technology_label = technology_label
        self.capacity_units = capacity_units
        self.input_commodity = input_commodity
        self.efficiency = efficiency
        self.output_commodity = output_commodity
        self.capacity_to_activity = capacity_to_activity
        self.capacity_factor = capacity_factor
        self.lifetime = lifetime
        self.lifetime_loan = lifetime_loan
        self.existing_capacity = existing_capacity

        return

    def placeholder(self):
        """
        This function does nothing except
        print the Zen of Python.
        """

        import this

        return


if __name__ == "__main__":
    s = Technology('Chambana', 'Tech',
                   'Label', 'Units',
                   'Input', 7,
                   'Output', 7, 7,
                   7, 7, 7)

    print('Test')
    print(s.region_name)
    print(s.technology_name)
    print(s.technology_label)
    print(s.capacity_units)
    print(s.input_commodity)
    print(s.efficiency)
    print(s.output_commodity)
    print(s.capacity_to_activity)
    print(s.capacity_factor)
    print(s.lifetime)
    print(s.lifetime_loan)
    print(s.existing_capacity)
