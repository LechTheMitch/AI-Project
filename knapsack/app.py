from knapsack import Knapsack as K, ProblemType
import customtkinter as ctk



def process_values():
    try:
        capacity = int(capacity_field.get())
        weights = [int(x.strip()) for x in weight_field.get().split()] 
        # Square brackets make python wait for the expression to finish executing before evaluating the expression
        values = [int(x.strip()) for x in value_field.get().split()]
        print(values)
        problem_type_raw = radio_var.get() # Needs converting to the enum we are using

        #TODO input validation

        problem_type = ProblemType.BOUNDED if problem_type_raw == "BOUNDED" else ProblemType.UNBOUNDED

        # TODO run solver function needs to be rewritten
        def run_solver():
                    knapsack = K(problem_type, capacity, weights, values)
                    solution, best_value = knapsack.solveKnapsack()

                    result_text = f"Best Value: {best_value}\n\n"
                    result_text += "Item Quantities:\n"
                    for item, qty in enumerate(solution): # enumarate returns the index and the value as a Tuple
                        #ie: if index 0 has value 5 enumerate returns the index and the value too unlike range
                        if qty > 0:
                            result_text += f"  Item {item+1}: {qty} copies (Weight: {weights[item]}, Value: {values[item]})\n"
                    
                    total_weight = sum(solution * knapsack.weights)
                    result_text += f"\nWeight Used: {total_weight}/{capacity}\n"
                    
                    results_text.configure(text=result_text)
                    solve_button.configure(state="normal")
        run_solver()
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

# TODO Impove the way results are shown
# Results

results_text = ctk.CTkLabel(mainWindow, text="")
results_text.pack(pady=10, padx=10)

# The Buttons
solve_button = ctk.CTkButton(mainWindow, text="Solve", command=process_values) # Putting the function call brackets immediately calls it which leads to program breaking behaviour 
solve_button.pack(padx=20, pady=20)

mainWindow.mainloop()