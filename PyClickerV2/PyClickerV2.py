import tkinter as tk
import time

# Initialize global variables
click_count = 0
click_multiplier = 1
multiplier_cost = 10  # Initial cost of the multiplier
click_auto = False
automation_cost = 10  # Initial cost of automation
start_time = time.time()

# Function to update the click count
def update_count():
    global click_count, click_multiplier
    click_count += click_multiplier
    count_label.config(text=f"Click Count: {click_count}")
    save_click_count()

# Function to increase click multiplier
def buy_multiplier():
    global click_multiplier, click_count, multiplier_cost
    if click_count >= multiplier_cost:
        click_count -= multiplier_cost
        click_multiplier += 1
        multiplier_cost += 10  # Increase cost by 10 clicks each time
        count_label.config(text=f"Click Count: {click_count}")
        multiplier_label.config(text=f"Click Multiplier: {click_multiplier}")
        buy_button.config(text=f"Buy Multiplier (Cost: {multiplier_cost} clicks)")
        save_click_count()

# Function to toggle click automation
def toggle_automation():
    global click_auto, automation_cost, click_count  # Declare click_count as a global variable
    if click_auto:
        click_auto = False
        automation_label.config(text=f"Automation: OFF (Cost: {automation_cost} clicks)")
        toggle_auto_button.config(text=f"Turn On Automation (Cost: {automation_cost} clicks)")
    else:
        if click_count >= automation_cost:
            click_count -= automation_cost
            click_auto = True
            automation_cost += 50  # Increase cost by 50 clicks each time
            automation_label.config(text=f"Automation: ON (Cost: {automation_cost} clicks)")
            toggle_auto_button.config(text=f"Turn Off Automation (Cost: {automation_cost} clicks)")
        else:
            automation_label.config(text="Not enough clicks to turn on automation!")

def auto_click():
    if click_auto:
        update_count()
    root.after(1000, auto_click)  # Auto click every 1000 milliseconds (1 second)

# Function to reset the click count and timer
def reset_game():
    save_click_count()
    exit()

def update_timer():
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Time Elapsed: {int(elapsed_time)} seconds")
    root.after(1000, update_timer)  # Update timer every 1000 milliseconds (1 second)

# Function to save the click count, multiplier, automation, and automation cost to a file
def save_click_count():
    with open("click_data.txt", "w") as file:
        file.write(f"{click_count}\n{click_multiplier}\n{'True' if click_auto else 'False'}\n{automation_cost}")

# Function to load the click count, multiplier, automation, and automation cost from a file
def load_click_data():
    try:
        with open("click_data.txt", "r") as file:
            data = file.read().splitlines()
            if len(data) >= 4:
                return int(data[0]), int(data[1]), data[2] == 'True', int(data[3])
            else:
                return 0, 1, False, 10  # Default values if data is incomplete
    except FileNotFoundError:
        return 0, 1, False, 10  # Default values if the file doesn't exist

# Create the main window
root = tk.Tk()
root.title("PyClickerV2")

# Initialize the click count, click multiplier, automation, and automation cost
click_count, click_multiplier, click_auto, automation_cost = load_click_data()

# Create and configure the count label
count_label = tk.Label(root, text=f"Click Count: {click_count}", font=("Arial", 24))
count_label.pack(pady=20)

# Create and configure the multiplier label
multiplier_label = tk.Label(root, text=f"Click Multiplier: {click_multiplier}", font=("Arial", 18))
multiplier_label.pack()

# Create and configure the automation label
automation_label = tk.Label(root, text=f"Automation: {'ON' if click_auto else 'OFF'} (Cost: {automation_cost} clicks)", font=("Arial", 18))
automation_label.pack()

# Create and configure the timer label
timer_label = tk.Label(root, text="Time Elapsed: 0 seconds", font=("Arial", 18))
timer_label.pack()

# Create the click button
click_button = tk.Button(root, text="Click Me!", command=update_count, font=("Arial", 18))
click_button.pack()

# Create the buy multiplier button
buy_button = tk.Button(root, text=f"Buy Multiplier (Cost: {multiplier_cost} clicks)", command=buy_multiplier, font=("Arial", 18))
buy_button.pack()

# Create the toggle automation button
toggle_auto_button = tk.Button(root, text=f"Turn {'Off' if click_auto else 'On'} Automation (Cost: {automation_cost} clicks)", command=toggle_automation, font=("Arial", 18))
toggle_auto_button.pack()

# Create the reset button
reset_button = tk.Button(root, text="I'm Feeling Lucky", command=reset_game, font=("Arial", 18))
reset_button.pack()

# Start auto-clicking
auto_click()

# Start the timer
update_timer()

# Run the main loop
root.mainloop()
