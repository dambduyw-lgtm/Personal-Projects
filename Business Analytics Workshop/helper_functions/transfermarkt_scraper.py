"""
Transfermarkt Player Market Value History Scraper

This script allows you to search for a player by name and retrieve their
complete market value history from Transfermarkt.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Optional
import pandas as pd


class TransfermarktScraper:
    """Scraper for Transfermarkt player data and market value history."""

    SEARCH_URL = "https://www.transfermarkt.nl/schnellsuche/ergebnis/schnellsuche"
    API_URL = "https://tmapi-alpha.transfermarkt.technology/player/{player_id}/market-value-history"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    def search_player(self, name: str) -> list[dict]:
        """
        Search for a player by name and return matching results.

        Args:
            name: Player name to search for

        Returns:
            List of dictionaries containing player info (id, name, club, etc.)
        """
        params = {"query": name}
        response = requests.get(
            self.SEARCH_URL,
            params=params,
            headers=self.HEADERS
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        players = []

        # Find player rows in the search results table
        player_rows = soup.select("table.items tbody tr")

        for row in player_rows:
            # Extract player link and ID
            player_link = row.select_one("td.hauptlink a")
            if not player_link:
                continue

            href = player_link.get("href", "")
            # Extract player ID from URL like /player-name/profil/spieler/123456
            id_match = re.search(r"/spieler/(\d+)", href)
            if not id_match:
                continue

            player_id = id_match.group(1)
            player_name = player_link.get_text(strip=True)

            # Extract additional info
            club_elem = row.select_one("td:nth-child(3) a")
            club = club_elem.get_text(strip=True) if club_elem else "Unknown"

            age_elem = row.select_one("td.zentriert")
            age = age_elem.get_text(strip=True) if age_elem else "Unknown"

            market_value_elem = row.select_one("td.rechts")
            market_value = market_value_elem.get_text(strip=True) if market_value_elem else "Unknown"

            players.append({
                "id": player_id,
                "name": player_name,
                "club": club,
                "age": age,
                "market_value": market_value,
            })

        return players

    def get_player_id(self, name: str) -> Optional[str]:
        """
        Search for a player and return the first matching player ID.

        Args:
            name: Player name to search for

        Returns:
            Player ID as string, or None if not found
        """
        players = self.search_player(name)
        if players:
            return players[0]["id"]
        return None

    def get_market_value_history(self, player_id: str) -> dict:
        """
        Get the complete market value history for a player.

        Args:
            player_id: Transfermarkt player ID

        Returns:
            Dictionary containing the API response with market value history
        """
        url = self.API_URL.format(player_id=player_id)
        response = requests.get(url, headers=self.HEADERS)
        response.raise_for_status()
        return response.json()

    def get_market_value_history_df(self, player_id: str) -> pd.DataFrame:
        """
        Get the market value history as a pandas DataFrame.

        Args:
            player_id: Transfermarkt player ID

        Returns:
            DataFrame with columns: date, value, age, club_id
        """
        data = self.get_market_value_history(player_id)

        if not data.get("success") or not data.get("data", {}).get("history"):
            return pd.DataFrame()

        history = data["data"]["history"]

        records = []
        for entry in history:
            market_value = entry.get("marketValue", {})
            records.append({
                "date": market_value.get("determined"),
                "value": market_value.get("value"),
                "currency": market_value.get("currency"),
                "age": entry.get("age"),
                "club_id": entry.get("clubId"),
            })

        df = pd.DataFrame(records)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")

        return df

    def scrape_player(self, name: str) -> tuple[Optional[str], pd.DataFrame]:
        """
        Search for a player by name and get their market value history.

        Args:
            name: Player name to search for

        Returns:
            Tuple of (player_id, DataFrame with market value history)
        """
        player_id = self.get_player_id(name)
        if not player_id:
            print(f"No player found for: {name}")
            return None, pd.DataFrame()

        print(f"Found player ID: {player_id}")
        df = self.get_market_value_history_df(player_id)
        return player_id, df


def main():
    """Example usage of the scraper."""
    scraper = TransfermarktScraper()

    # Example: Search for a player
    player_name = "Erling Haaland"
    print(f"\nSearching for: {player_name}")
    print("-" * 50)

    # Get all search results
    results = scraper.search_player(player_name)
    print(f"\nFound {len(results)} result(s):")
    for player in results:
        print(f"  ID: {player['id']}, Name: {player['name']}, Club: {player['club']}")

    # Get market value history for the first result
    if results:
        player_id = results[0]["id"]
        print(f"\nFetching market value history for player ID: {player_id}")

        df = scraper.get_market_value_history_df(player_id)

        if not df.empty:
            print(f"\nMarket Value History ({len(df)} entries):")
            print(df.to_string(index=False))

            # Optionally save to CSV
            # df.to_csv(f"market_value_history_{player_id}.csv", index=False)
        else:
            print("No market value history found.")


if __name__ == "__main__":
    main()
