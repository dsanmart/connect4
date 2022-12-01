from utils import *


# ------- THE 4 RULES --------

def disjoint(s1, s2) -> bool:
    """Returns True if the sets of squares are disjoint. Otherwise, False.
    Args:
        solution (Solution): a Solution.
        other (Solution): a Solution.
    Returns:
        True if the sets of squares are disjoint. Otherwise, False
    """
    return set(s1["squares"]).isdisjoint(s2["squares"])

def no_claimeven_below_or_at_inverse(inverse_solution, claimeven_solution):
    """Returns True if there is no Claimeven in claimeven_solution below or at the Inverse of inverse_solution.
    Args:
        inverse_solution (Solution): either a Lowinverse or Highinverse Solution.
        claimeven_solution (Solution): a Claimeven, Aftereven, Baseclaim, Before, or Specialbefore Solution.
    Returns:
        False if there exists a lower Claimeven square in claimeven_solution equal to or
            above a square in inverse_solution.
        Otherwise, True.
    """
    #
    for i_square in inverse_solution["squares"]:
        for c_square in claimeven_solution["squares"][1]: # Lower Claimeven squares.
            # If the inverse has a square above or equal to the bottom square of a Claimeven in other:
            if i_square[1] == c_square[1] and i_square[0] <= c_square[0]:
                return False
    return True

def column_wise_disjoint_or_equal(s1, s2):
    s1_square_by_column = cols_to_squares(s1)
    s2_square_by_column = cols_to_squares(s2)
    for col in s1_square_by_column:
        if col in s2_square_by_column:
            # If the two sets of Squares are not equal but share a Square:
            if (s1_square_by_column[col].intersection(s2_square_by_column[col]) and
                    s1_square_by_column[col] != s2_square_by_column[col]):
                return False
    return True

def combination_allowed(s1, s2):
    """Check if the combination of two solutions is allowed based in section 7.4 of the thesis.

    Parameters
        sol1 : The first solution.
        sol2 : The second solution.

    Returns
        True if the combination is allowed, False otherwise.
    """
    # If either Solution is an Oddthreat or ThreatCombination.
    if s1["rule"] == "odd_threat" or s1["rule"] == "threat_combination":
        return allowed_with_odd_threat_or_threat_combination(s1, s2)
    if s2["rule"] == "odd_threat" or s2["rule"] == "threat_combination":
        return allowed_with_odd_threat_or_threat_combination(s2, s1)

    # If either Solution is a Claimeven.
    if s1["rule"] == "claimeven":
        return allowed_with_claimeven(s1, s2)
    if s2["rule"] == "claimeven":
        return allowed_with_claimeven(s2, s1)

    # If either Solution is a Baseinverse:
    if s1["rule"] == "baseinverse":
        return allowed_with_baseinverse(s1, s2)
    if s2["rule"] == "baseinverse":
        return allowed_with_baseinverse(s2, s1)

    # If either Solution is a Vertical:
    if s1["rule"] == "vertical":
        return allowed_with_vertical(s1, s2)
    if s2["rule"] == "vertical":
        return allowed_with_vertical(s2, s1)

    # If either Solution is a Before:
    if s1["rule"] == "before":
        return allowed_with_vertical(s1, s2)
    if s2["rule"] == "before":
        return allowed_with_vertical(s2, s1)
    

def allowed_with_claimeven(s1, s2):
    if s2["rule"] in ["claimeven", "baseinverse", "vertical", "aftereven", "baseclaim", "before", "specialbefore"]:
        return disjoint(s1, s2)
    if s2["rule"] in ["lowinverse", "highinverse"]:
        return no_claimeven_below_or_at_inverse(inverse_solution=s2, claimeven_solution=s1)
    raise ValueError("invalid other.rule_instance for allowed_with_claimeven:", s2["rule"])

def allowed_with_baseinverse(s1, s2):
    """Returns True if other can be combined with solution; Otherwise, False."""
    return disjoint(s1, s2)

def allowed_with_vertical(s1, s2):
    """Returns True if other can be combined with solution; Otherwise, False."""
    return disjoint(s1, s2)

def allowed_with_baseclaim(s1, s2):
    """Returns True if other can be combined with solution; Otherwise, False."""
    return disjoint(s1, s2)

def allowed_with_before(s1, s2):
    """Returns True if other can be combined with solution; Otherwise, False."""
    return column_wise_disjoint_or_equal(s1, s2)

def allowed_with_odd_threat_or_threat_combination(s1, s2):
    """Requires:
    1. sol must be rule=Oddthreat or rule=ThreatCombination.
    """






# ----------- TESTING ----------- #

if __name__ == "__main__":

    s1 = {'squares': [(1, 5), (4, 2), (4, 2), (3, 2), (1, 5), (0, 5)], 'groups': {((2, 5), (3, 4), (4, 3), (5, 2))}, 'rule': 'before'}
    s2 = {'squares': ((5, 5), (4, 5)), 'groups': [((2, 5), (3, 5), (4, 5), (5, 5)), ((5, 2), (5, 3), (5, 4), (5, 5)), ((5, 3), (5, 4), (5, 5), (5, 6))], 'rule': 'claimeven'}
    print(combination_allowed(s1, s2))
