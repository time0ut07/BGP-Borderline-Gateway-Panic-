def clear_all_logs(file:str):
    with open(f'./resources/{file}', 'w') as f:
        pass
    
    print(f"[+] Cleared logs: ./resources/{file}")