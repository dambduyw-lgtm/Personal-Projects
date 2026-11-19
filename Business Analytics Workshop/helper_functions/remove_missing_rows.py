"""
Remove rows with missing values ('-' or null) for position-relevant KPIs.
Creates a new CSV file without overwriting the original.
Uses custom position mapping.
"""

import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import POSITION_MAPPING
from config.config import POSITION_KPIS


def remove_missing_rows(input_path: str, output_base: str):
    """
    Remove rows with missing values for position-relevant KPIs.
    Creates separate CSV files for each position group.

    Args:
        input_path: Path to the input CSV file
        output_base: Base name for output files (will append position group name)
    """
    print(f"Reading data from {input_path}...")
    df = pd.read_csv(input_path, low_memory=False)
    total_rows = len(df)
    total_unique_players = df["Name"].nunique()
    print(f"Loaded {total_rows} rows, {total_unique_players} unique players\n")

    results = {}

    # Process each position group separately
    for position_group, kpis in POSITION_KPIS.items():
        mapped_positions = POSITION_MAPPING.get(position_group, [])
        all_kpis = list(set(kpis))
        valid_kpis = [kpi for kpi in all_kpis if kpi in df.columns]
        missing_kpis = [kpi for kpi in all_kpis if kpi not in df.columns]

        # Filter data for this position group
        df_pos = df[df["Position"].isin(mapped_positions)].copy()
        pos_total = len(df_pos)
        unique_players_total = df_pos["Name"].nunique()

        if pos_total == 0:
            print(f"{position_group} ({', '.join(mapped_positions)}): No rows found")
            continue

        # Count missing values per row for relevant KPIs
        missing_count = pd.Series([0] * len(df_pos), index=df_pos.index)
        for kpi in valid_kpis:
            missing_count = missing_count + (df_pos[kpi].isnull() | (df_pos[kpi] == '-')).astype(int)

        # Calculate percentage of missing KPIs per row
        total_kpis = len(valid_kpis)
        missing_pct = missing_count / total_kpis * 100

        # Remove rows where more than 20% of KPIs are missing
        remove_mask = missing_pct > 20

        # Keep rows with 20% or less missing
        df_clean = df_pos[~remove_mask].copy()
        rows_kept = len(df_clean)
        unique_players_kept = df_clean["Name"].nunique()

        # Removed rows (more than 20% missing)
        df_removed = df_pos[remove_mask].copy()
        rows_removed = len(df_removed)

        # Store results
        results[position_group] = {
            "df": df_clean,
            "df_removed": df_removed,
            "positions": mapped_positions,
            "total_rows": pos_total,
            "kept_rows": rows_kept,
            "removed_rows": rows_removed,
            "total_players": unique_players_total,
            "kept_players": unique_players_kept
        }

        # Print stats
        print(f"{position_group} ({', '.join(mapped_positions)}):")
        print(f"  Rows: {rows_kept}/{pos_total} kept ({round(rows_kept/pos_total*100, 1)}%)")
        print(f"  Players: {unique_players_kept}/{unique_players_total} kept ({round(unique_players_kept/unique_players_total*100, 1)}%)")
        if missing_kpis:
            print(f"  KPIs not found in data: {missing_kpis}")
        print()

    # Save each position group to separate file (kept and removed)
    print(f"\n{'='*60}")
    print("SAVING FILES")
    print(f"{'='*60}")

    for position_group, data in results.items():
        # Save kept rows
        output_path = f"{output_base}_{position_group.replace(' ', '_')}.csv"
        data["df"].to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"  {position_group}: {output_path} ({data['kept_rows']} rows)")

        # Save removed rows
        removed_path = f"{output_base}_{position_group.replace(' ', '_')}_removed.csv"
        data["df_removed"].to_csv(removed_path, index=False, encoding='utf-8-sig')
        print(f"  {position_group} (removed): {removed_path} ({data['removed_rows']} rows)")

    return results


def main():
    # Get the project root directory (parent of helper_functions)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_path = os.path.join(project_root, "full_datasets", "Data Excelsior - EUR_with_market_values.csv")
    output_base = os.path.join(project_root, "dataset_per_position", "position")
    remove_missing_rows(input_path, output_base)


if __name__ == "__main__":
    main()
