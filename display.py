import curses
import time
import socket

# Define the crossroads sections
sections = ["North", "South", "West", "East"]

# Define the traffic light states
light_states = {
    "North": "Red",
    "South": "Red",
    "West": "Green",
    "East": "Green"
}

# Define the vehicles in each section (test data)
vehicles = {
    "North": [],
    "South": [],
    "West": ["Car1", "Car2"],
    "East": ["Car3"]
}


def init_terminal():
    """Initialise la fenetre curses."""
    stdscr = curses.initscr()
    curses.noecho()  
    curses.cbreak() 
    curses.curs_set(0)
    stdscr.nodelay(1) 
    stdscr.keypad(True)  
    return stdscr

def update_lights():
    """Simulate the change of traffic lights."""
    global light_states
    if light_states["North"] == "Red":
        light_states["North"] = "Green"
        light_states["South"] = "Green"
        light_states["West"] = "Red"
        light_states["East"] = "Red"
    else:
        light_states["North"] = "Red"
        light_states["South"] = "Red"
        light_states["West"] = "Green"
        light_states["East"] = "Green"

def action_info():
    """Return what is happening (vehicule crossing, new priority vehicule, etc) to show on the screen."""
    # TODO : Implement the logic to generate the action info
    return "No action"




def display_crossroads(stdscr):
    """Affiche le croisement grace a curses."""

    stdscr.clear() 
    HOST = "localhost"
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        for _ in range(10):  # Simule 10 cycles
            #time.sleep(2)
            stdscr.clear()
            data = client_socket.recv(1024)

            if data:
                data = data.decode()
                time.sleep(2)
                data = eval(data)
            
            light_states["North"] = data[0][0]
            light_states["South"] = data[0][1]
            light_states["West"] = data[0][2]
            light_states["East"] = data[0][3]
            vehicles["North"] = data[1]
            vehicles["South"] = data[2]
            vehicles["West"] = data[3]
            vehicles["East"] = data[4]
            act_info = data[5]
                    

            # Recupere la taille du terminal
            height, width = stdscr.getmaxyx()

            if height < 15 or width < 40:
                stdscr.addstr(0, 0, "Erreur: terminal trop petit ! Il doit faire au moins : 15 lignes x 40 colonnes.")
                stdscr.refresh()
                return

            stdscr.addstr(0, 0, "At the crossroads", curses.A_BOLD)


            stdscr.addstr(2, 0, "Traffic Lights:")
            stdscr.addstr(3, 0, f"North: {light_states['North']}")
            stdscr.addstr(4, 0, f"South: {light_states['South']}")
            stdscr.addstr(5, 0, f"West:  {light_states['West']}")
            stdscr.addstr(6, 0, f"East:  {light_states['East']}")

            stdscr.addstr(8, 0, "Vehicules:")
            row = 9
            for section in sections:
                stdscr.addstr(row, 0, f"{section}: {', '.join(vehicles[section] if vehicles[section] else ['No vehicles'])}")
                row += 1

            stdscr.addstr(13, 0, "Action:")
            stdscr.addstr(14, 0, act_info)

            # Refresh the screen to show updates
            stdscr.refresh()
            client_socket.send(b"Received")

def simulate(stdscr):
    """Simulate the crossroads for a few cycles."""
    curses.curs_set(0)  
    stdscr.nodelay(1)  

    for _ in range(1):  # Simule 10 cycles
        display_crossroads(stdscr)
        update_lights()
        act_info = action_info()

        # Display the generated vehicle info
        height, width = stdscr.getmaxyx()
        if height >= 15 and width >= 40:
            stdscr.addstr(14, 0, act_info)
            stdscr.refresh()

   # Wait 2 seconds between cycles

        # Check for user input to exit early
        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":


    curses.wrapper(simulate)  # Use curses wrapper to handle setup/cleanup