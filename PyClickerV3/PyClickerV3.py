import tkinter as tk
import time

# Initialize global variables
click_count = 0
click_multiplier = 1
multiplier_cost = 10  # Initial cost of the multiplier
click_auto = False
automation_cost = 10  # Initial cost of automation
automation_click_rate = 1  # Initial click rate of automation
automation_level = 0  # Initial automation level
start_time = time.time()

# Function to update the click count
def update_count():
    global click_count, click_multiplier
    click_count += click_multiplier
    count_label.config(text=f"Click Count: {click_count}")

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

# Function to toggle click automation
def toggle_automation():
    global click_auto, automation_cost, click_count  # Declare click_count as a global variable
    if click_auto:
        click_auto = False
        automation_label.config(text=f"Automation: OFF (Upgrade: {automation_cost} clicks)")
        toggle_auto_button.config(text=f"Turn On Automation (Cost: {automation_cost} clicks)")
    else:
        if click_count >= automation_cost:
            click_count -= automation_cost
            click_auto = True
            automation_cost += 50  # Increase cost by 50 clicks each time
            automation_label.config(text=f"Automation: ON (Upgrade: {automation_cost} clicks)")
            toggle_auto_button.config(text=f"Turn Off Automation (Cost: {automation_cost} clicks)")
            update_automation_level()  # Update automation level when turning on automation
        else:
            automation_label.config(text="Not enough clicks to turn on automation!")

def auto_click():
    if click_auto:
        update_count()
    root.after(1000 // automation_click_rate, auto_click)  # Auto click every N milliseconds (faster with higher click_rate)

# Function to upgrade automation click rate
def upgrade_automation():
    global automation_click_rate, automation_cost, click_count, automation_level
    if click_count >= automation_cost and automation_level < 200:  # Limit automation upgrade to level 200
        click_count -= automation_cost
        automation_click_rate += 1
        automation_cost += 100  # Increase cost by 100 clicks each time
        automation_label.config(text=f"Automation: ON (Upgrade: {automation_cost} clicks)")
        toggle_auto_button.config(text=f"Turn Off Automation (Cost: {automation_cost} clicks)")
        upgrade_auto_button.config(text=f"Upgrade Automation (Upgrade: {automation_cost} clicks)")
        update_automation_level()  # Update automation level after upgrade

# Function to update the automation level
def update_automation_level():
    global automation_level
    automation_level += 1
    automation_level_label.config(text=f"Automation Level: {automation_level}")

# Function to reset the click count and timer
def reset_game():
    save_click_count()
    exit()

def update_timer():
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Time Elapsed: {int(elapsed_time)} seconds")
    root.after(1000, update_timer)  # Update timer every 1000 milliseconds (1 second)

# Function to save the click count, multiplier, automation, automation cost, automation click rate, and automation level to a file
def save_click_count():
    with open("click_data.txt", "w") as file:
        file.write(f"{click_count}\n{click_multiplier}\n{'True' if click_auto else 'False'}\n{automation_cost}\n{automation_click_rate}\n{automation_level}")

# Function to load the click count, multiplier, automation, automation cost, automation click rate, and automation level from a file
def load_click_data():
    try:
        with open("click_data.txt", "r") as file:
            data = file.read().splitlines()
            if len(data) >= 6:
                return int(data[0]), int(data[1]), data[2] == 'True', int(data[3]), int(data[4]), int(data[5])
            else:
                return 0, 1, False, 10, 1, 0  # Default values if data is incomplete
    except FileNotFoundError:
        return 0, 1, False, 10, 1, 0  # Default values if the file doesn't exist

# Create the main window
root = tk.Tk()
root.title("PyClickerV3")

# Set background color to black for the main window
root.configure(bg="white")

# Initialize the click count, click multiplier, automation, automation cost, automation click rate, and automation level
click_count, click_multiplier, click_auto, automation_cost, automation_click_rate, automation_level = load_click_data()

# Create and configure the count label
count_label = tk.Label(root, text=f"Click Count: {click_count}", font=("Arial", 24), bg="white", fg="black")
count_label.pack(pady=20)

# Create and configure the multiplier label
multiplier_label = tk.Label(root, text=f"Click Multiplier: {click_multiplier}", font=("Arial", 18), bg="white", fg="black")
multiplier_label.pack()

# Create and configure the automation label
automation_label = tk.Label(root, text=f"Automation: {'ON' if click_auto else 'OFF'} (Upgrade: {automation_cost} clicks)", font=("Arial", 18), bg="white", fg="black")
automation_label.pack()

# Create and configure the automation level label
automation_level_label = tk.Label(root, text=f"Automation Level: {automation_level}", font=("Arial", 18), bg="white", fg="black")
automation_level_label.pack()

# Create and configure the timer label
timer_label = tk.Label(root, text="Time Elapsed: 0 seconds", font=("Arial", 18), bg="white", fg="black")
timer_label.pack()

# Create the click button
click_button = tk.Button(root, text="Click Me!", command=update_count, font=("Arial", 18), bg="white", fg="black")
click_button.pack()

# Create the buy multiplier button
buy_button = tk.Button(root, text=f"Buy Multiplier (Upgrade: {multiplier_cost} clicks)", command=buy_multiplier, font=("Arial", 18), bg="white", fg="black")
buy_button.pack()

# Create the toggle automation button
toggle_auto_button = tk.Button(root, text=f"Turn {'Off' if click_auto else 'On'} Automation (Upgrade: {automation_cost} clicks)", command=toggle_automation, font=("Arial", 18), bg="white", fg="black")
toggle_auto_button.pack()

# Create the upgrade automation button
upgrade_auto_button = tk.Button(root, text=f"Upgrade Automation (Upgrade: {automation_cost} clicks)", command=upgrade_automation, font=("Arial", 18), bg="white", fg="black")
upgrade_auto_button.pack()

# Create the reset button
reset_button = tk.Button(root, text="I'm Feeling Lucky", command=reset_game, font=("Arial", 18), bg="white", fg="black")
reset_button.pack()

# Start auto-clicking
auto_click()

# Start the timer
update_timer()

# Run the main loop
root.mainloop()
