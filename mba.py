import pandas as pd
import tkinter as tk
from tkinter import ttk
from apyori import apriori

data = pd.read_csv("C:/Users/Vaishnavi/Desktop/Groceries data.csv")

transaction = data.groupby(['Member_number'])['itemDescription'].apply(list).values.tolist()
rules2 = apriori(transaction, min_support=0.00002, min_confidence=0.0005, min_lift=1.0001, min_length=2, max_length=2)
sorted_rules2 = sorted(rules2, key=lambda x: x.ordered_statistics[0].lift, reverse=True)


def show_item_count():
    # Calculate item count
    item_count = data['itemDescription'].value_counts().reset_index()
    item_count.columns = ['Item', 'Count']
    
    # Create a new window for the table
    window = tk.Toplevel(root)

    # Create a Treeview widget to display the table
    table_treeview = ttk.Treeview(window)
    table_treeview.pack()

    # Configure the Treeview columns
    table_treeview["columns"] = ("Item", "Count")
    table_treeview["show"] = "headings"

    # Set the column headings
    table_treeview.heading("Item", text="Item")
    table_treeview.heading("Count", text="Count")

    # Insert the table content into the Treeview
    for _, row in item_count.iterrows():
        table_treeview.insert("", "end", values=row.tolist())

def market_analysis():
    transaction = data.groupby(['Member_number'])['itemDescription'].apply(list).values.tolist()

    rules1 = apriori(transaction, min_support=0.002, min_confidence=0.05, min_lift=3, min_length=2, max_length=2)
    sorted_rules1 = sorted(rules1, key=lambda x: x.ordered_statistics[0].lift, reverse=True)

    rules2 = apriori(transaction, min_support=0.00002, min_confidence=0.0005, min_lift=1.00001, min_length=2, max_length=2)
    sorted_rules2 = sorted(rules2, key=lambda x: x.ordered_statistics[0].lift, reverse=True)


    # Function to get the pairs with highest lift for each LHS item
    def get_highest_lift_pairs():
        pairs_dict = {}
        for rule in sorted_rules1:
            lhs = ', '.join(rule.ordered_statistics[0].items_base)
            rhs = ', '.join(rule.ordered_statistics[0].items_add)
            lift = rule.ordered_statistics[0].lift
            
            if lhs not in pairs_dict or lift > pairs_dict[lhs]['lift']:
                pairs_dict[lhs] = {'rhs': rhs, 'lift': lift}
        
        return pairs_dict

    def display_highest_selling_pair():
        # Create a new window for displaying the pairs with highest lift
        window = tk.Toplevel(root)

        # Create a Treeview widget to display the pairs
        pairs_treeview = ttk.Treeview(window)
        pairs_treeview.pack()

        # Configure the Treeview columns
        pairs_treeview["columns"] = ("LHS", "RHS", "Lift")
        pairs_treeview["show"] = "headings"

        # Set the column headings
        pairs_treeview.heading("LHS", text="LHS")
        pairs_treeview.heading("RHS", text="RHS")
        pairs_treeview.heading("Lift", text="Lift")

        # Get the pairs with highest lift for each LHS item
        pairs_dict = get_highest_lift_pairs()

        # Insert the pairs into the Treeview
        for lhs, pair_info in pairs_dict.items():
            pairs_treeview.insert("", "end", values=(lhs, pair_info['rhs'], pair_info['lift']))

    def display_all_data():
        # Create a new window for displaying all pairs
        window = tk.Toplevel(root)

        
        # Create a Treeview widget to display the pairs
        pairs_treeview = ttk.Treeview(window)
        pairs_treeview.pack()

        # Configure the Treeview columns
        pairs_treeview["columns"] = ("LHS", "RHS", "Lift")
        pairs_treeview["show"] = "headings"

        # Set the column headings
        pairs_treeview.heading("LHS", text="LHS")
        pairs_treeview.heading("RHS", text="RHS")
        pairs_treeview.heading("Lift", text="Lift")

        # Insert all pairs into the Treeview
        for rule in sorted_rules2:
            lhs = ', '.join(rule.ordered_statistics[0].items_base)
            rhs = ', '.join(rule.ordered_statistics[0].items_add)
            lift = rule.ordered_statistics[0].lift
            pairs_treeview.insert("", "end", values=(lhs, rhs, lift))

    # Create a new window for the market analysis options
    window = tk.Toplevel(root)

    # Add a button to display the highest selling pair
    highest_selling_pair_button = tk.Button(window, text="Highest Selling Pair", command=display_highest_selling_pair)
    highest_selling_pair_button.pack()

    # Add a button to display all data
    all_data_button = tk.Button(window, text="All Data", command=display_all_data)
    all_data_button.pack()

def predict():
    selected_item = item_combobox.get()
    predicted_item = None
    
    for rule in sorted_rules2:
        lhs_items = rule.ordered_statistics[0].items_base
        if selected_item in lhs_items:
            rhs_items = rule.ordered_statistics[0].items_add
            predicted_item = list(rhs_items)[0]
            break
    
    if predicted_item:
        prediction_label.config(text=f"Predicted item to pair with '{selected_item}': {predicted_item}")
    else:
        prediction_label.config(text=f"No prediction available for '{selected_item}'")

# Create the main window
root = tk.Tk()

# Add a button to trigger the show_item_count() function
item_count_button = tk.Button(root, text="Show Item Count", command=show_item_count)
item_count_button.pack()

# Add a button to trigger the market_analysis() function
market_analysis_button = tk.Button(root, text="Market Analysis", command=market_analysis)
market_analysis_button.pack()

# Create a Combobox to select an item for prediction
item_combobox = ttk.Combobox(root, values=data['itemDescription'].unique().tolist())
item_combobox.pack()

# Create a Predict button to trigger the predict() function
predict_button = tk.Button(root, text="Predict", command=predict)
predict_button.pack()

# Create a Label to display the prediction result
prediction_label = tk.Label(root, text="Predicted item to pair with '':")
prediction_label.pack()

root.mainloop()
