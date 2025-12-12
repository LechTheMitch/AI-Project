from knapsack import Knapsack as K, ProblemType
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def process_values():
    try:
        capacity = int(capacity_field.get())
        weights = [int(x.strip()) for x in weight_field.get().split()] 
        values = [int(x.strip()) for x in value_field.get().split()]
        
        problem_type_raw = radio_var.get()
        problem_type = ProblemType.BOUNDED if problem_type_raw == "BOUNDED" else ProblemType.UNBOUNDED

        #Input validation
        if len(weights) != len(values):
            results_text.configure(text = "The Number of Weights and values must be equal")
            return
        
        # --- PLOT RESET ---
        ax.clear()
        ax.set_title("Cultural Algorithm Progress", color='white')
        ax.set_xlabel("Generation", color='white')
        ax.set_ylabel("Fitness Value", color='white')
        ax.grid(True, color='#404040')
        
        # Initialize lines
        line_best, = ax.plot([], [], label="Best Fitness", color="#2CC985", linewidth=2)
        line_avg, = ax.plot([], [], label="Avg Fitness", color="#3B8ED0", linestyle="--", linewidth=1.5)
        
        # Style legend
        legend = ax.legend(facecolor='#2b2b2b', edgecolor='white')
        for text in legend.get_texts():
            text.set_color("white")
            
        canvas.draw()

        # Data storage
        gen_data, best_data, avg_data = [], [], []

        # Create Solver Instance
        knapsack = K(problem_type, capacity, weights, values)
        
        # Use the Generator method (Ensure solveKnapsackGenerator exists in knapsack.py)
        solver_gen = knapsack.solveKnapsackGenerator()
        
        solve_button.configure(state="disabled")

        def step():
            try:
                # Get next generation data
                generation, current_best, current_avg = next(solver_gen)
                
                # Update Data Lists
                gen_data.append(generation)
                best_data.append(current_best)
                avg_data.append(current_avg)

                # Update Plot every 2 frames (for performance)
                if generation % 2 == 0:
                    line_best.set_data(gen_data, best_data)
                    line_avg.set_data(gen_data, avg_data)
                    
                    ax.relim()
                    ax.autoscale_view()
                    canvas.draw()
                    canvas.flush_events()

                results_text.configure(text=f"Running Gen {generation}...\nBest Value: {current_best}")
                
                # Schedule next step (1ms delay keeps UI responsive)
                mainWindow.after(1, step)

            except StopIteration:
                # Solver Finished
                solution = knapsack.best_solution
                best_value = knapsack.best_fitness
                
                # Final Plot Update
                line_best.set_data(gen_data, best_data)
                line_avg.set_data(gen_data, avg_data)
                ax.relim()
                ax.autoscale_view()
                canvas.draw()

                # Display Results
                result_text = f"DONE! Best Value: {best_value}\n\n"
                result_text += "Item Quantities:\n"
                for item, qty in enumerate(solution):
                    if qty > 0:
                        result_text += f"  Item {item+1}: {qty} copies (Weight: {weights[item]}, Value: {values[item]})\n"
                
                total_weight = sum(solution * knapsack.weights)
                result_text += f"\nWeight Used: {total_weight}/{capacity}\n"
                
                results_text.configure(text=result_text)
                solve_button.configure(state="normal")

        step() # Start the loop

    except ValueError:
        results_text.configure(text="Error: Invalid Input")
    except Exception as e:
        results_text.configure(text=f"Error: {str(e)}")

# Just some theming stuff
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

mainWindow = ctk.CTk()
mainWindow.title("Knapsack Solver using Cultural Algorithm")
mainWindow.geometry("800x1000")
mainWindow.resizable(True, True)

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
ctk.CTkLabel(input_frame, text="A default of Unbounded is assumed").grid(row=4, column=0, padx=10, pady=10, sticky="w")
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

#Plot Code
plot_frame = ctk.CTkFrame(mainWindow, width=600, height=400)
plot_frame.pack(pady=10, padx=20)
plot_frame.pack_propagate(False)

fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
fig.patch.set_facecolor('#242424')
ax.set_facecolor('#2b2b2b')
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()

canvas.get_tk_widget().pack(fill="both", expand=True)

mainWindow.mainloop()