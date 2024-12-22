import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_to_picture(filepath):
    # Validate the input file
    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return
    
    # Load the CSV data
    try:
        data = pd.read_csv(filepath, skiprows=1, names=["Частота", "Канал A"])
        data["Частота"] = pd.to_numeric(data["Частота"], errors='coerce')
        data["Канал A"] = pd.to_numeric(data["Канал A"], errors='coerce')

        if data.shape[1] < 2:
            print("Error: CSV file must have at least two columns.")
            return

    except Exception as e:
        print(f"Error: Could not read CSV file. {e}")
        return
    
    data = data.dropna()
    
    # Plot the data
    plt.figure(figsize=(10, 6))

    plt.plot(data["Частота"], data["Канал A"], label="Сигнал (Канал A)")

    plt.xlabel("Частота (кГц)")

    plt.ylabel("Напряжение (В)")

    plt.grid(True)


    # Ensure the pictures directory exists
    pictures_dir = "pictures"
    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)

    # Save the plot
    filename = os.path.splitext(os.path.basename(filepath))[0] + ".pdf"
    save_path = os.path.join(pictures_dir, filename)
    plt.savefig(save_path)
    plt.close()

    print(f"Graph saved to '{save_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
    else:
        plot_csv_to_picture(sys.argv[1])


