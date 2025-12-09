import caseworker
import sys

# Redirect stdout to suppress game intro
sys.stdout = open("test_output.txt", "w")

player = caseworker.Player("TestWorker")

# Check initial state
initial_clients = player.caseload.clients
print("Initial Client States:")
for name, c in initial_clients.items():
    print(f"{name}: {c.status}")

# Force cooldown on one client
client_name = "Chloe"
player.caseload.clients[client_name].status = "Chill"
player.caseload.clients[client_name].cooldown = 5
print(f"\nSet {client_name} cooldown to 5.")

# Simulate turns
print("\nSimulating turns...")
for i in range(3):
    player.caseload.update_all()
    print(f"Turn {i+1} - {client_name} Cooldown: {player.caseload.clients[client_name].cooldown}")

# Verify cooldown decreased
assert player.caseload.clients[client_name].cooldown == 2
print("\nCooldown logic verified.")

# Verify crisis persistence
player.caseload.clients[client_name].trigger_crisis()
print(f"\nTriggered crisis for {client_name}. Status: {player.caseload.clients[client_name].status}")
player.caseload.update_all()
print(f"Next turn. Status: {player.caseload.clients[client_name].status}")
assert player.caseload.clients[client_name].status == "Crisis"
print("Crisis persistence verified.")
