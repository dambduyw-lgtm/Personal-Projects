"""
Script to append league quality information to the dataset.

Joins the league quality table (league_quality.csv) with the main dataset
based on the country and division extracted from the Season column.
"""

import pandas as pd


def parse_season(season_str: str) -> tuple[str, str, int]:
    """Parse 'NED II 2024' into (country, division, year)."""
    parts = season_str.split()
    return parts[0], parts[1], int(parts[2])


def append_league_quality(
    input_path: str,
    output_path: str,
    league_quality_path: str = "excel_helpers/league_quality.csv"
):
    """
    Append league quality columns to the dataset.

    Args:
        input_path: Path to input CSV (main dataset)
        output_path: Path for output CSV
        league_quality_path: Path to league quality reference table
    """
    print(f"Reading main dataset from {input_path}...")
    df = pd.read_csv(input_path, low_memory=False)
    print(f"Loaded {len(df)} rows")

    print(f"Reading league quality table from {league_quality_path}...")
    df_quality = pd.read_csv(league_quality_path)
    print(f"Loaded {len(df_quality)} league entries")

    # Extract country and division from Season column
    print("\nExtracting country and division from Season column...")
    df["Country"] = df["Season"].apply(lambda x: parse_season(x)[0])
    df["Division"] = df["Season"].apply(lambda x: parse_season(x)[1])

    # Merge with league quality table
    print("Joining league quality data...")
    df = df.merge(
        df_quality,
        left_on=["Country", "Division"],
        right_on=["Country", "Division"],
        how="left"
    )

    # Drop the temporary Country and Division columns (they're now duplicated)
    # Keep the ones from the quality table which include League_Name
    # Actually, let's keep Country and Division as they might be useful

    # Save with UTF-8 encoding
    print(f"\nSaving results to {output_path} (UTF-8)...")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("Done!")

    # Summary
    print(f"\nSummary:")
    print(f"  Total rows: {len(df)}")
    print(f"  New columns added: Country, Division, League_Name, League_Quality, Player_Quality, Pricing")
    print(f"\nLeague quality distribution:")
    print(df["League_Quality"].value_counts().to_string())

    return df


def main():
    input_path = "full_datasets/Data Excelsior - EUR_with_market_values.csv"
    output_path = "full_datasets/Data Excelsior - EUR_with_market_values.csv"  # Overwrite

    append_league_quality(input_path, output_path)


if __name__ == "__main__":
    main()
