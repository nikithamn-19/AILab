# Vacuum Cleaner Agent

def vacuum_cleaner():
    room_A = input("Enter status of Room A (Dirty/Clean): ")
    room_B = input("Enter status of Room B (Dirty/Clean): ")
    location = input("Enter vacuum location (A/B): ")

    room_A = room_A.lower()
    room_B = room_B.lower()
    location = location.upper()

    print("\nInitial State:")
    print("Room A:", room_A)
    print("Room B:", room_B)
    print("Vacuum Location:", location)

    # Clean Room A
    if location == "A":

        if room_A == "dirty":
            print("\nRoom A is dirty.")
            print("Action: SUCK")
            room_A = "clean"

        print("Action: MOVE RIGHT")
        location = "B"

        if room_B == "dirty":
            print("Room B is dirty.")
            print("Action: SUCK")
            room_B = "clean"

    # Clean Room B
    elif location == "B":

        if room_B == "dirty":
            print("\nRoom B is dirty.")
            print("Action: SUCK")
            room_B = "clean"

        print("Action: MOVE LEFT")
        location = "A"

        if room_A == "dirty":
            print("Room A is dirty.")
            print("Action: SUCK")
            room_A = "clean"

    print("\nFinal State:")
    print("Room A:", room_A)
    print("Room B:", room_B)
    print("Vacuum Location:", location)

    if room_A == "clean" and room_B == "clean":
        print("\nGoal achieved! Both rooms are clean.")
    else:
        print("\nGoal not achieved.")


vacuum_cleaner()