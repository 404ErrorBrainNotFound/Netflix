import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *
from tkinter import ttk
from statsmodels.tsa.arima.model import ARIMA
import warnings
import numpy as np

# Load the dataset
netflix_data = pd.read_csv('data.csv')  # Update 'data.csv' with your actual file name

def plot_top_10():
    selected_country = country_var.get()
    selected_category = category_var.get()

    if selected_country and selected_category:
        filtered_data = netflix_data[
            (netflix_data['country_name'] == selected_country) &
            (netflix_data['category'] == selected_category)
        ]

        if not filtered_data.empty:
            top_10_data = filtered_data.groupby('show_title')['cumulative_weeks_in_top_10'].max().nlargest(10)
            top_10_shows = list(top_10_data.index)

            filtered_top_10 = filtered_data[filtered_data['show_title'].isin(top_10_shows)]

            custom_palette = sns.color_palette('viridis', len(top_10_shows))

            plt.figure(figsize=(12, 6))

            ax1 = plt.subplot(1, 2, 1)
            sns.countplot(x='show_title', data=filtered_top_10, order=top_10_shows, palette=custom_palette)
            plt.title(f'Top 10 {selected_category} in {selected_country}', fontsize=16)
            plt.xlabel('Show Title', fontsize=12)
            plt.ylabel('Count', fontsize=12)
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=10)
            ax1.set_xticklabels([])  
            ax1.legend().set_visible(False)  

            ax2 = plt.subplot(1, 2, 2)
            show_counts = filtered_top_10['show_title'].value_counts().head(10)
            wedges, _, _ = plt.pie(show_counts, labels=None, autopct='%1.1f%%', startangle=140, colors=custom_palette)

            plt.title(f'Show Distribution in Top 10 {selected_category} ({selected_country})', fontsize=16)

            for wedge in wedges:
                wedge.set_edgecolor('white')  # Add white edges to improve visibility of pie slices

            # Create a legend for the pie chart labels
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=custom_palette[i], markersize=8, label=show)
                               for i, show in enumerate(list(show_counts.index))]
            plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), title='Show Names')

            plt.tight_layout()
            plt.show()
        else:
            print(f"No data available for {selected_country} - {selected_category}.")
    else:
        print("Please select both country and category.")


import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from statsmodels.tsa.arima.model import ARIMA

# Load the dataset
netflix_data = pd.read_csv('data.csv')  # Update 'data.csv' with your actual file name

def predict_and_plot():
    selected_country = country_var.get()
    selected_category = category_var.get()

    if selected_country and selected_category:
        filtered_data = netflix_data[
            (netflix_data['country_name'] == selected_country) &
            (netflix_data['category'] == selected_category)
        ]

        if not filtered_data.empty:
            # Assuming 'weekly_rank' and 'cumulative_weeks_in_top_10' are columns used for prediction
            time_series = filtered_data.set_index('week')['weekly_rank']

            # Fit an ARIMA model (Example purposes only, real prediction models might be different)
            model = ARIMA(time_series, order=(5, 1, 0))  # ARIMA(5,1,0) model for example
            fitted_model = model.fit()

            # Predict next week's rankings
            future_week = pd.to_datetime(filtered_data['week']).max() + pd.DateOffset(weeks=1)
            predicted_values = fitted_model.forecast(steps=10)  # Predict next 10 values

            # Replace NaN values with 0
            predicted_values = pd.Series(predicted_values).fillna(0).tolist()

            # Retrieve the show names for later display
            top_10_shows = filtered_data.groupby('show_title')['cumulative_weeks_in_top_10'].max().nlargest(10).index.tolist()
            show_colors = plt.cm.tab20c(range(len(top_10_shows)))

            # Create a color map for the pie chart
            colors = plt.cm.tab20c(range(len(predicted_values)))

            # Plotting the predicted rankings
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))

            # Bar plot for predicted values with color coordination
            bars = axs[0].bar(range(1, len(predicted_values) + 1), predicted_values, color=colors)
            axs[0].set_title(f'Predicted Top 10 {selected_category} in {selected_country}', fontsize=16)
            axs[0].set_xlabel('Rank', fontsize=12)
            axs[0].set_ylabel('Predicted Value', fontsize=12)
            axs[0].set_xticks(range(1, len(predicted_values) + 1))
            axs[0].set_xticklabels(['']*len(predicted_values))  # No show names below the bar graph
            axs[0].tick_params(axis='y', labelsize=10)

            # Create a legend box to display show names with colors (for the pie chart)
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markersize=8, markerfacecolor=show_colors[i], label=show_name)
                               for i, show_name in enumerate(top_10_shows)]
            axs[1].legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), title='Show Names')

            # Pie chart for predicted values without show names displayed as labels
            axs[1].pie(predicted_values, labels=None, autopct='%1.1f%%', startangle=140, colors=colors)
            axs[1].set_title(f'Predicted Show Distribution in Top 10 {selected_category} ({selected_country})', fontsize=16)

            plt.tight_layout()
            plt.show()
        else:
            predicted_rankings_label.config(text=f"No data available for {selected_country} - {selected_category}.")
    else:
        predicted_rankings_label.config(text="Please select both country and category.")

root = Tk()
root.title('Netflix Show Analysis')

main_frame = Frame(root, padx=20, pady=20)
main_frame.pack()

# Label and dropdown for Country selection
country_label = Label(main_frame, text="Country:", font=('Arial', 12))
country_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

countries = list(netflix_data['country_name'].unique())
country_var = StringVar(root)
country_dropdown = ttk.Combobox(main_frame, textvariable=country_var, values=countries, font=('Arial', 12), state='readonly')
country_dropdown.grid(row=0, column=1, padx=10, pady=5)
country_dropdown.current(0)

# Label and dropdown for Category selection
category_label = Label(main_frame, text="Category:", font=('Arial', 12))
category_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

categories = ["TV", "Films"]  # Fixed categories as per your requirement
category_var = StringVar(root)
category_dropdown = ttk.Combobox(main_frame, textvariable=category_var, values=categories, font=('Arial', 12), state='readonly')
category_dropdown.grid(row=1, column=1, padx=10, pady=5)
category_dropdown.current(0)

plot_button = Button(main_frame, text="Plot", command=plot_top_10, font=('Arial', 12), bg='green', fg='white')
plot_button.grid(row=2, column=0, pady=10, padx=5, columnspan=2, sticky='ew')

# Button for Predicting Rankings and Plotting
predict_button = Button(main_frame, text="Predict", command=predict_and_plot, font=('Arial', 12), bg='blue', fg='white')
predict_button.grid(row=3, column=0, pady=10, padx=5, columnspan=2, sticky='ew')

# Label to display the predicted rankings
predicted_rankings_label = Label(main_frame, text="", font=('Arial', 12))
predicted_rankings_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()

root.mainloop()
