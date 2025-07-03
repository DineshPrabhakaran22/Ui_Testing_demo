import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("ui_testing_repos_detailed.csv")


keyword_cols = [
    "technologies", "ui_testing_tools", "patterns", 
    "paradigms", "best_practices", "principles"
]


df[keyword_cols] = df[keyword_cols].fillna("")


guideline_cols = [col for col in df.columns if col.endswith(".md")]


def count_keywords(column):
    values = df[column].astype(str).str.lower().str.split(", ")
    flattened = [kw.strip() for sublist in values for kw in sublist if kw]
    return pd.Series(flattened).value_counts()

for col in keyword_cols:
    freq = count_keywords(col)
    plt.figure(figsize=(8, 5))
    if not freq.empty:
        freq.plot(kind="bar", color="teal")
        plt.title(f"{col.replace('_', ' ').title()} Mentions")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{col}_chart.png")
        print(f"📊 Saved {col}_chart.png")
    else:
        print(f"No data for {col}")


for col in guideline_cols:
    vals = df[col].value_counts()
    if not vals.empty:
        plt.figure(figsize=(4, 4))
        vals.plot(kind="pie", autopct="%1.0f%%", startangle=90, labels=["Present", "Missing"])
        plt.title(f"{col} Presence")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(f"{col.replace('/', '_')}_pie.png")
        print(f"📄 Saved {col}_pie.png")