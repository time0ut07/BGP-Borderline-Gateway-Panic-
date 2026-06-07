from conn.conn_menu import conn_menu


def main_menu():
    """
    Main Menu Options
    """

    while True:

        print("\n\n======= Main Menu =======")
        print("1. Connection\n2. Reconnaissance\n3. Hijack\n4. Post-Exploitation\n5. Settings")
        choice = input("Select an option: ")

        match choice:
            case "1":
                conn_menu()
            case "2":
                return "recon"
            case "3":
                return "hijack"
            case "4":
                return "pe"
            case "5":
                return "settings"
            case _:
                print("[x] Invalid option")
                continue
