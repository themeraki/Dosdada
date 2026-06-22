import socket
import json
from colorama import Fore, Style, init

# Initialize UI
init(autoreset=True)

class Controller:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print(f"{Fore.GREEN}[+] Controller started on {self.host}:{self.port}")
        print(f"{Fore.CYAN}[*] Waiting for Agent to connect...")

    def run(self):
        conn, addr = self.server.accept()
        print(f"{Fore.GREEN}[+] Agent connected from {addr}")
        
        with conn:
            while True:
                # Get User Input
                cmd = input(f"\n{Fore.YELLOW}Agent_CMD > {Style.RESET_ALL}").strip()
                
                if cmd.lower() in ['exit', 'quit']:
                    conn.sendall(json.dumps({"action": "exit"}).encode())
                    break
                
                # Dynamic Parameter Input (Optional JSON for parameters)
                params_input = input(f"{Fore.BLUE}Parameters (JSON or press Enter): {Style.RESET_ALL}")
                params = json.loads(params_input) if params_input else {}
                
                # Build Payload
                payload = json.dumps({"action": cmd, "params": params})
                conn.sendall(payload.encode())
                
                # Get Response
                try:
                    data = conn.recv(4096).decode()
                    if not data:
                        print(f"{Fore.RED}[!] Connection lost.")
                        break
                    
                    response = json.loads(data)
                    self.display_response(response)
                    
                except json.JSONDecodeError:
                    print(f"{Fore.RED}[!] Received invalid data format.")

    def display_response(self, response):
        """Cleanly format JSON responses to the screen."""
        if response.get("status") == "success":
            print(f"{Fore.GREEN}[SUCCESS] {Style.RESET_ALL}{response}")
        else:
            print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{response.get('message', 'Unknown Error')}")

if __name__ == "__main__":
    controller = Controller()
    controller.run()
