if __name__ == "__main__":
    NORTH=1
    SOUTH=4
    EAST=2
    WEST=8
    NORTH_WEST = WEST | NORTH
    # | ASSIGN
    # & COMPARE (Return 0 false, Value true)
    # &= ~ SUB

    bitv = NORTH | SOUTH | EAST # | assign

    if bitv & EAST:
        print("East")

    ...