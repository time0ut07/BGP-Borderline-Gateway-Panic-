def clear_all_logs():
    with open('./resources/logs.txt', 'w') as f:
        pass
    
    print("[+] Cleared logs")