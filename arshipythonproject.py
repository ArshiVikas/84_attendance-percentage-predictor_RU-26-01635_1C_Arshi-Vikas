import numpy as np
import pandas as pd

def get_attendance_data():
    print("Choose input method:")
    print("1. Enter attendance manually")
    print("2. Load attendance from a CSV file")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        raw_input = input("Enter weekly attendance percentages separated by commas: ")
        # Convert comma-separated text into a list of floats
        attendance = [float(x.strip()) for x in raw_input.split(",") if x.strip() != ""]
        weeks = list(range(1, len(attendance) + 1))
        return weeks, attendance

    elif choice == "2":
        file_name = input("Enter CSV file name (e.g., attendance.csv): ").strip()
        df = pd.read_csv(file_name)
        # Assumes CSV has columns 'Week' and 'Attendance'
        weeks = df["Week"].tolist()
        attendance = df["Attendance"].tolist()
        return weeks, attendance

    else:
        print("Invalid choice.")
        return None, None


def predict_attendance():
    try:
        weeks, attendance = get_attendance_data()
        if weeks is None:
            return

        # Validation 1: Check for at least 2 weeks of data
        if len(attendance) < 2:
            print("At least 2 weeks of data are required.")
            return

        # Validation 2: Check that all values are between 0 and 100
        for val in attendance:
            if val < 0 or val > 100:
                print("Attendance must be between 0 and 100.")
                return

        # Ask for the future week to predict
        target_week = int(input("Predict for week: "))

        # Convert lists to NumPy arrays and fit a straight line (degree = 1)
        x = np.array(weeks)
        y = np.array(attendance)
        slope, intercept = np.polyfit(x, y, 1)

        # Calculate predicted attendance
        predicted = (slope * target_week) + intercept

        # Cap the result between 0 and 100
        cap_note = ""
        if predicted > 100:
            predicted = 100.0
            cap_note = " (capped at 100)"
        elif predicted < 0:
            predicted = 0.0
            cap_note = " (capped at 0)"

        # Display outputs matching the required format
        print(f"\nSlope: {slope:.2f} | Intercept: {intercept:.2f}")
        print(f"Predicted attendance for week {target_week}: {predicted:.2f}%{cap_note}")

        if predicted >= 75:
            print("Safe")
        else:
            print("Warning: below 75%")

    except ValueError:
        print("Invalid input! Please enter numeric values only.")
    except FileNotFoundError:
        print("CSV file not found. Please check the file name and path.")


# Run the program
if __name__ == "__main__":
    predict_attendance()