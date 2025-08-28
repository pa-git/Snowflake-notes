import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv("your_dataset.csv")  # Replace with your actual file name

# Optional: Convert duration_seconds to minutes or hours if values are too large
df["duration_minutes"] = df["duration_seconds"] / 60

# Set up the plot style
sns.set(style="whitegrid")

# Plot the distribution of duration per crew_name
plt.figure(figsize=(12, 6))
sns.histplot(
    data=df,
    x="duration_minutes",
    hue="crew_name",
    multiple="stack",  # Use "dodge" for side-by-side histograms
    bins=30,
    kde=True
)

plt.title("Distribution of Processing Time (in Minutes) by Crew Name")
plt.xlabel("Processing Time (Minutes)")
plt.ylabel("Count")
plt.legend(title="Crew Name")
plt.tight_layout()
plt.show()
