from conn.conn_run import conn_run


def conn_menu():
    """
    Connection (Option 1) Menu
    """

    while True:
        print("\n\n===== Connection Menu =====")
        print("1. OPEN\n2. UPDATE\n")
        choice = input(">> ")

        match choice:
            case "1":
                conn_run()
            case "2":
                return "conn_UPDATE"
            case _:
                print("[x] Invalid option")
                continue