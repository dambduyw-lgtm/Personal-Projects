"""
Script to calculate player age based on birth year and season year.

Loops over every row and calculates Age = Season_Year - Birth_Year
"""

import pandas as pd


def calculate_age(input_path: str, output_path: str):
    """
    Calculate and append Age column to the dataset.

    Args:
        input_path: Path to input CSV
        output_path: Path for output CSV
    """
    print(f"Reading dataset from {input_path}...")
    df = pd.read_csv(input_path, low_memory=False, encoding='utf-8')
    print(f"Loaded {len(df)} rows")

    print("\nCalculating age for each row...")
    ages = []
    skipped = 0
    for index, row in df.iterrows():
        birth_value = row["Birth"]
        if pd.isna(birth_value) or str(birth_value).strip() == "-":
            ages.append(None)
            skipped += 1
        else:
            season_year = int(row["Season"].split()[-1])
            birth_year = int(birth_value)
            age = season_year - birth_year
            ages.append(age)

        if (index + 1) % 10000 == 0:
            print(f"  Processed {index + 1} rows...")

    if skipped > 0:
        print(f"  Skipped {skipped} rows with missing birth year")

    df["Age"] = ages

    print(f"\nSaving results to {output_path} with UTF-8 encoding...")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("Done!")

    # Summary
    print(f"\nSummary:")
    print(f"  Total rows: {len(df)}")
    print(f"  Age statistics:")
    print(f"    Min: {df['Age'].min()}")
    print(f"    Max: {df['Age'].max()}")
    print(f"    Mean: {df['Age'].mean():.1f}")
    print(f"    Median: {df['Age'].median()}")

    return df


def main():
    input_path = "full_datasets/Data Excelsior - EUR_with_market_values.csv"
    output_path = "full_datasets/Data Excelsior - EUR_with_market_values.csv"  # Overwrite

    calculate_age(input_path, output_path)


if __name__ == "__main__":
    main()
