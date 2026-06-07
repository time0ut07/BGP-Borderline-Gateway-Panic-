def conn_menu():
    """
    Connection (Option 1) Menu
    """

    while True:
        print("\n\n===== Connection Menu =====")
        print("1. OPEN\n2. UPDATE\n")
        choice = input("Select an option: ")

        match choice:
            case "1":
                return "conn_OPEN"
            case "2":
                return "conn_UPDATE"
            case _:
                print("[x] Invalid option")
                continue