import tkinter as tk
import time

# Function to update the click count
def update_count():
    global click_count
    click_count += click_multiplier
    count_label.config(text=f"Click Count: {click_count}")
    save_click_count()

# Function to increase click multiplier
def buy_multiplier():
    global click_multiplier, click_count
    cost = 10  # Cost to buy the multiplier
    if click_count >= cost:
        click_count -= cost
        click_multiplier += 1
        count_label.config(text=f"Click Count: {click_count}")
        multiplier_label.config(text=f"Click Multiplier: {click_multiplier}")
        save_click_count()

# Function to reset the click count and timer
def reset_game():
    save_click_count()
    exit()
    

# Function to save the click count and multiplier to a file
def save_click_count():
    with open("click_data.txt", "w") as file:
        file.write(f"{click_count}\n{click_multiplier}")

# Function to load the click count and multiplier from a file
def load_click_data():
    try:
        with open("click_data.txt", "r") as file:
            data = file.read().splitlines()
            if len(data) >= 1:
                return int(data[0]), int(data[1])
            else:
                return 0, 1  # Default values if data is incomplete
    except FileNotFoundError:
        return 0, 1  # Default values if the file doesn't exist


# Function to update the timer
def update_timer():
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Time Elapsed: {int(elapsed_time)} seconds")
    root.after(1000, update_timer)  # Update timer every 1000 milliseconds (1 second)

# Create the main window
root = tk.Tk()
root.title("PyClicker")

# Initialize the click count, click multiplier, and start time
click_count, click_multiplier = load_click_data()
start_time = time.time()

# Create and configure the count label
count_label = tk.Label(root, text=f"Click Count: {click_count}", font=("Arial", 24))
count_label.pack(pady=20)

# Create and configure the multiplier label
multiplier_label = tk.Label(root, text=f"Click Multiplier: {click_multiplier}", font=("Arial", 18))
multiplier_label.pack()

# Create and configure the timer label
timer_label = tk.Label(root, text="Time Elapsed: 0 seconds", font=("Arial", 18))
timer_label.pack()

# Create the click button
click_button = tk.Button(root, text="Click Me!", command=update_count, font=("Arial", 18))
click_button.pack()

# Create the buy button
buy_button = tk.Button(root, text="Buy Multiplier (Cost: 10)", command=buy_multiplier, font=("Arial", 18))
buy_button.pack()

# Create the reset button
reset_button = tk.Button(root, text="I'm Feeling Lucky", command=reset_game, font=("Arial", 18))
reset_button.pack()

# Start the timer
update_timer()

# Run the main loop
root.mainloop()
