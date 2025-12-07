from knapsack import Knapsack as K, ProblemType
import customtkinter as ctk

def get_knapvalues(itemname: str):
    while True:
        try:
            knapvalues = list(map(int, input(f"Enter the {itemname} Seprated by spaces ").split()))

            if any(knapvalue <= 0 for knapvalue in knapvalues):
                print(f"All {itemname.lower()} must be positive integers")
                continue
        
            return knapvalues

        except ValueError:
            print(f"{itemname} must be positive integers")

# capacity = int(input("Please enter the Sack's capacity "))
# weights = get_knapvalues("Weights")

# while True:
#     values = get_knapvalues("Values")
    
#     if len(weights) == len(values):
#         break

#     print("There must be as many values as there are weights")

# capacity = 60

# weights = [3, 2, 8, 3]
# values = [10, 20, 15, 9]

#s = K(ProblemType.UNBOUNDED, capacity, weights, values)

def process_values():
    try:
        capacity = int(capacity_field.get())
        weights = [int(x.strip()) for x in weight_field.get().split()] 
        # Square brackets make python wait for the expression to finish executing before evaluating the expression
        values = [int(x.strip()) for x in value_field.get().split()]
        problem_type_raw = radio_var.get() # Needs converting to the enum we are using

        #TODO input validation

        problem_type = ProblemType.BOUNDED if problem_type_raw == "BOUNDED" else ProblemType.UNBOUNDED

        def run_solver():# Stolen Code
                    knapsack = K(problem_type, capacity, weights, values)
                    solution, best_value = knapsack.solveKnapsack()
                    
                    result_text = f"Best Value: {best_value}\n\n"
                    result_text += "Item Quantities:\n"
                    for i, qty in enumerate(solution):
                        if qty > 0:
                            result_text += f"  Item {i}: {qty} copies (Weight: {weights[i]}, Value: {values[i]})\n"
                    
                    total_weight = sum(solution * knapsack.weights)
                    result_text += f"\nTotal Weight: {total_weight}/{capacity}\n"
                    result_text += f"Remaining Capacity: {capacity - total_weight}\n"
                    
                    results_text.delete("1.0", "end")
                    results_text.insert("1.0", result_text)
                    solve_button.configure(state="normal")
    except:
        pass

# Just some theming stuff
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

mainWindow = ctk.CTk()
mainWindow.title("Knapsack Solver using Cultural Algorithm")
mainWindow.geometry("700x800")
mainWindow.resizable(False, False)

input_frame = ctk.CTkFrame(mainWindow) # Container for inputs
input_frame.pack(pady=10, padx=20, fill="x")

# Enables auto width by allowing expansion of columns
input_frame.grid_columnconfigure(1, weight=1)

# Adding Capacity to the container
ctk.CTkLabel(input_frame, text="Capacity:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
capacity_field = ctk.CTkEntry(input_frame, placeholder_text="Enter the Knapsack's Capacity")
capacity_field.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Adding Weights to the container which must be inputted separated by commas
ctk.CTkLabel(input_frame, text="Weights:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
weight_field = ctk.CTkEntry(input_frame, placeholder_text="Please Enter the Weights separated by Spaces")
weight_field.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Adding Values
ctk.CTkLabel(input_frame, text="Values:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
value_field = ctk.CTkEntry(input_frame, placeholder_text="Please Enter the Values separated by Spaces") # TODO add popup to explain the nature of the values
value_field.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Problem Type Radio Buttons
ctk.CTkLabel(input_frame, text="Problem Type:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
radio_var = ctk.StringVar(value="")

bounded_button = ctk.CTkRadioButton(input_frame, text="Bounded", value="BOUNDED", variable=radio_var)
bounded_button.grid(row = 3, column = 1, padx=10, pady=10)

unbounded_button = ctk.CTkRadioButton(input_frame, text="Unbounded", value="UNBOUNDED", variable=radio_var)
unbounded_button.grid(row = 3, column = 2, padx=10, pady=10, sticky="w")

# Results
results_frame = ctk.CTkFrame(mainWindow)
results_frame.pack(pady=10, padx=20, fill="both", expand=True)

ctk.CTkLabel(results_frame, text="Results:").pack(pady=10)

results_text = ctk.CTkTextbox(results_frame, width=700, height=250, font=("Courier", 12))
results_text.pack(pady=10, padx=10, fill="both", expand=True)

# The Buttons
solve_button = ctk.CTkButton(mainWindow, text="Solve", command=process_values) # Putting the function call brackets immediately calls it which leads to program breaking behaviour 
solve_button.pack(padx=20, pady=20)

clear_button = ctk.CTkButton(mainWindow, text="Clear", command=lambda: print([int(x.strip()) for x in weight_field.get().split()] )) # Putting the function call brackets immediately calls it which leads to program breaking behaviour 
clear_button.pack(padx=20, pady=20)

mainWindow.mainloop()