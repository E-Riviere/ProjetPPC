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



def action_info():
    """Return what is happening (vehicule crossing, new priority vehicule, etc) to show on the screen."""
    # TODO : Implement the logic to generate the action info
    return "No action"




def display_crossroads(stdscr):
    """Affiche le croisement grace a curses."""

    stdscr.clear() 
    HOST = "localhost"
    PORT = 8080
    changed = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        while True:  # Simule 10 cycles
            if changed:
                stdscr.clear()
                changed = False

            data = client_socket.recv(1024)

            if data:
                data = data.decode()
                try:
                    data = eval(data)
                except ValueError:
                    stdscr(16,0,str(data))
                i = 0
                for k,v in light_states.items():
                    if light_states[k] != data[0][i] or vehicles[k] != data[i+1]:
                        changed = True
                        
                        break   
                light_states["North"] = data[0][0]
                light_states["South"] = data[0][1]
                light_states["West"] = data[0][2]
                light_states["East"] = data[0][3]
                vehicles["North"] = data[1]
                vehicles["West"] = data[2]
                vehicles["East"] = data[3]
                vehicles["South"] = data[4]
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
                stdscr.addstr(row, 0, f"{section}: {vehicles[section] if vehicles[section] != "" else 'No vehicle'}")
                row += 1

            stdscr.addstr(13, 0, "Action:")
            stdscr.addstr(14, 0, act_info)

            # Refresh the screen to show updates
            if changed:
                act_info = "Changement"
                stdscr.addstr(14, 0, act_info)
                stdscr.refresh()
            act_info = action_info()

    # Display the generated vehicle info
            height, width = stdscr.getmaxyx()
            if height >= 15 and width >= 40:
                stdscr.addstr(14, 0, act_info)
                
                key = stdscr.getch()
                
            if key == ord('q'):
                client_socket.sendall(b"exit")
                client_socket.close()
                break
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Simulation ended. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()
    

def simulate(stdscr):
    """Simulate the crossroads for a few cycles."""
    curses.curs_set(0)  
    stdscr.nodelay(1)  

    
    display_crossroads(stdscr)

   # Wait 2 seconds between cycles

        # Check for user input to exit early
    

if __name__ == "__main__":


    curses.wrapper(simulate)  # Use curses wrapper to handle setup/cleanup