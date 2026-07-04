def clear_all_logs(file:str) -> None:
    """Erase all contents of specified log file

    Opens target file in ./resources/ in write mode to truncate its content and
    prints a confirmation message for user

    Args:
        file (str): Name of log file located in './resources/'    
    """

    with open(f'./resources/{file}', 'w') as f:
        pass
    
    print(f"[+] Cleared logs: ./resources/{file}")
