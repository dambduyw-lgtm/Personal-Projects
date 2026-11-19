"""
Script to append Transfermarkt market values to the Excelsior dataset.

This script:
1. Reads the CSV with player/season data
2. Maps each season to an end date
3. Searches for each player on Transfermarkt
4. Gets the market value closest to the season end date
5. Appends the market value to the dataset
"""

import pandas as pd
from datetime import datetime
from helper_functions.transfermarkt_scraper import TransfermarktScraper
import time
from typing import Optional


# Season end dates mapping
# Format: {COUNTRY} {DIVISION} {YEAR}
# - I = 1st division, II = 2nd division
# - Year = the year the season ends (e.g., 2024 = 2023/24 season)
#
# European leagues (autumn-spring): end in May
# Nordic leagues (calendar year): end in November

SEASON_END_DATES = {
    "NED": (5, 25),   # Netherlands - late May
    "POR": (5, 25),   # Portugal - late May
    "BEL": (5, 25),   # Belgium - late May
    "NOR": (11, 30),  # Norway - late November
    "SWE": (11, 30),  # Sweden - late November
    "FIN": (10, 31),  # Finland - late October
}


def parse_season(season_str: str) -> tuple[str, str, int]:
    """
    Parse a season string like 'NED II 2024' into components.

    Returns:
        Tuple of (country_code, division, year)
    """
    parts = season_str.split()
    country = parts[0]
    division = parts[1]
    year = int(parts[2])
    return country, division, year


def get_season_end_date(season_str: str) -> datetime:
    """
    Get the end date for a given season.

    Args:
        season_str: Season string like 'NED II 2024'
            - I/II = division (1st or 2nd)
            - Year = the year the season ends

    Returns:
        datetime object representing the season end date
    """
    country, division, year = parse_season(season_str)
    end_month, end_day = SEASON_END_DATES.get(country, (5, 25))
    return datetime(year, end_month, end_day)


def get_market_value_at_date(
    df_history: pd.DataFrame,
    target_date: datetime
) -> Optional[int]:
    """
    Get the market value closest to (but not after) the target date.

    Args:
        df_history: DataFrame with market value history (must have 'date' and 'value' columns)
        target_date: The date to find the value for

    Returns:
        Market value as integer, or None if no valid value found
    """
    if df_history.empty:
        return None

    # Filter to values on or before the target date
    target_date = pd.Timestamp(target_date)
    valid_values = df_history[df_history["date"] <= target_date]

    if valid_values.empty:
        return None

    # Get the most recent value before/on the target date
    closest = valid_values.loc[valid_values["date"].idxmax()]
    return int(closest["value"])


def process_dataset(
    input_path: str,
    output_path: str,
    delay: float = 1.0,
    max_players: Optional[int] = None
):
    """
    Process the dataset and append market values.

    Strategy:
    1. Get all unique player names
    2. Fetch market value history ONCE per player
    3. Use cached history to fill values for all seasons

    Args:
        input_path: Path to input CSV
        output_path: Path for output CSV
        delay: Delay between API requests (seconds)
        max_players: Maximum number of unique players to process (for testing)
    """
    print(f"Reading data from {input_path}...")
    df = pd.read_csv(input_path, low_memory=False)
    print(f"Loaded {len(df)} rows")

    # Initialize new columns
    df["Transfermarkt_Value"] = None
    df["Transfermarkt_Player_ID"] = None

    # Get unique players (not player-season combinations!)
    unique_players = df["Name"].unique()
    print(f"Found {len(unique_players)} unique players")

    scraper = TransfermarktScraper()

    # Step 1: Fetch all player histories
    print("\n=== Step 1: Fetching player data from Transfermarkt ===\n")
    player_cache = {}  # name -> (player_id, df_history)

    for i, player_name in enumerate(unique_players):
        if max_players and i >= max_players:
            break

        print(f"[{i+1}/{len(unique_players) if not max_players else max_players}] {player_name}...", end=" ")

        try:
            player_id = scraper.get_player_id(player_name)
            if player_id:
                df_history = scraper.get_market_value_history_df(player_id)
                player_cache[player_name] = (player_id, df_history)
                print(f"ID: {player_id}, {len(df_history)} value records")
            else:
                print("Not found")
                player_cache[player_name] = (None, pd.DataFrame())
            time.sleep(delay)  # Rate limiting
        except Exception as e:
            print(f"Error: {e}")
            player_cache[player_name] = (None, pd.DataFrame())

        # Progress update
        if (i + 1) % 100 == 0:
            print(f"\n--- Progress: {i+1} players fetched ---\n")

    # Step 2: Fill in market values for all rows
    print("\n=== Step 2: Filling market values for all seasons ===\n")

    filled_count = 0
    not_found_count = 0
    no_value_count = 0

    for player_name, (player_id, df_history) in player_cache.items():
        if player_id is None:
            not_found_count += df["Name"].eq(player_name).sum()
            continue

        # Get all seasons this player appears in
        player_mask = df["Name"] == player_name
        player_seasons = df.loc[player_mask, "Season"].unique()

        for season in player_seasons:
            season_end = get_season_end_date(season)
            market_value = get_market_value_at_date(df_history, season_end)

            # Update all rows for this player-season combination
            mask = (df["Name"] == player_name) & (df["Season"] == season)

            # Player was found on Transfermarkt
            # If no value for this date, fill 0 (player probably had no value back then)
            if market_value is None:
                market_value = 0
                no_value_count += mask.sum()
            else:
                filled_count += mask.sum()

            df.loc[mask, "Transfermarkt_Value"] = market_value
            df.loc[mask, "Transfermarkt_Player_ID"] = player_id

    # Save results with UTF-8 encoding
    print(f"Saving results to {output_path} (UTF-8)...")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("Done!")

    # Print summary
    print(f"\nSummary:")
    print(f"  Total rows: {len(df)}")
    print(f"  Rows with market value: {filled_count}")
    print(f"  Rows - player not found on TM: {not_found_count}")
    print(f"  Rows - no value for date: {no_value_count}")
    print(f"  Players fetched: {len(player_cache)}")
    print(f"  API calls made: {len(player_cache)} (instead of {len(df[['Name', 'Season']].drop_duplicates())} combinations)")

    return df


def main():
    """Main entry point."""
    input_path = "full_datasets/Data Excelsior - EUR.csv"
    output_path = "full_datasets/Data Excelsior - EUR_with_market_values.csv"

    # For testing, limit to first 5 players
    # Remove max_players parameter for full processing
    df = process_dataset(
        input_path=input_path,
        output_path=output_path,
        delay=0.2,  # 0.2 second delay between API calls
        max_players=None  # Remove or set to None for full processing
    )


if __name__ == "__main__":
    main()
