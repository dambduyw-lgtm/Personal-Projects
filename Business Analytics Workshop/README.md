# Excelsior Data Cleaning & Analysis

This project contains scripts for cleaning and analyzing football player data from Driblab for Excelsior Rotterdam, including market value enrichment from Transfermarkt.

## Project Structure

```
business_analytics_workshop/
├── config/
│   └── config.py                 # Position mappings and KPI definitions
├── helper_functions/
│   ├── transfermarkt_scraper.py  # Scraper for Transfermarkt market values
│   ├── append_market_values.py   # Enriches dataset with market values
│   ├── append_league_quality.py  # Adds league quality metadata
│   ├── calculate_age.py          # Calculates player age from birth year
│   └── remove_missing_rows.py    # Cleans data by removing incomplete rows
├── excel_helpers/
│   ├── league_quality.csv        # League quality reference table
│   └── KPI Weight Driblab - Excelsior updated.xlsx
├── full_datasets/
│   ├── Data Excelsior - EUR.csv                    # Original Driblab dataset
│   └── Data Excelsior - EUR_with_market_values.csv # Enriched dataset
├── dataset_per_position/         # Cleaned data split by position
├── requirements.txt
└── README.md
```

## Data Files

### Input Data
- `full_datasets/Data Excelsior - EUR.csv` - Original dataset from Driblab
- `full_datasets/Data Excelsior - EUR_with_market_values.csv` - Dataset enriched with Transfermarkt market values, league quality, and calculated age

### Reference Data
- `excel_helpers/league_quality.csv` - League quality ratings for Netherlands, Belgium, Portugal, Norway, Sweden, and Finland

### Output Data
- `dataset_per_position/` - Cleaned data split by position group

## Scripts

### Data Enrichment Pipeline

Run these scripts in order to process the raw data:

#### 1. `helper_functions/append_market_values.py`
Fetches historical market values from Transfermarkt for each player.
- Searches players by name on Transfermarkt
- Gets market value history and finds the value closest to each season end date
- Adds columns: `Transfermarkt_Value`, `Transfermarkt_Player_ID`

```bash
python helper_functions/append_market_values.py
```

#### 2. `helper_functions/append_league_quality.py`
Adds league quality metadata based on country and division.
- Parses the Season column (e.g., "NED II 2024")
- Joins with `league_quality.csv` reference table
- Adds columns: `Country`, `Division`, `League_Name`, `League_Quality`, `Player_Quality`, `Pricing`

```bash
python helper_functions/append_league_quality.py
```

#### 3. `helper_functions/calculate_age.py`
Calculates player age based on birth year and season year.
- Extracts season year from Season column
- Calculates: `Age = Season_Year - Birth_Year`
- Handles missing birth values (marked as `-`)

```bash
python helper_functions/calculate_age.py
```

#### 4. `helper_functions/remove_missing_rows.py`
Cleans data by removing rows with too many missing KPI values.
- Filters by position group using custom mapping
- Removes rows where >20% of position-relevant KPIs are missing
- Creates separate CSV files for each position group

```bash
python helper_functions/remove_missing_rows.py
```

### Supporting Scripts

#### `helper_functions/transfermarkt_scraper.py`
A reusable scraper class for Transfermarkt data.
- `TransfermarktScraper.search_player(name)` - Search for players by name
- `TransfermarktScraper.get_market_value_history_df(player_id)` - Get market value history as DataFrame

## Configuration

### Position Mapping (`config/config.py`)

| Position Group | Driblab Positions | Description |
|----------------|-------------------|-------------|
| Centre back | DC | Central defenders |
| Full back | DR, DL | Right/left backs |
| 6 | DMC, MC | Defensive/holding midfielders |
| 8 | MC, ML, MR | Box-to-box midfielders |
| 10 | AMC, MC, AML, AMR | Attacking midfielders |
| 7 | AML, AMR, FWL, FWR | Wingers |
| 9 | FW | Strikers |

Note: Some positions (like MC, AML, AMR) belong to multiple groups because players in these positions can fulfill different tactical roles.

### KPI Definitions (`config/config.py`)

Each position group has a tailored set of KPIs for evaluation:
- **Centre back**: Defensive actions, aerial duels, passing & build-up
- **Full back**: Defensive work, wide progression, crossing
- **6 (DM)**: Defensive shielding, ball circulation, progression from deep
- **8 (CM)**: Box-to-box contribution, passing, chance creation
- **7 (Winger)**: 1v1 dribbling, chance creation from wide, attacking threat
- **10 (AM)**: Creative output, ball progression, scoring support
- **9 (Striker)**: Goal scoring, penalty-box presence, aerial play

### League Quality Reference

| Country | Division | League Name | Quality |
|---------|----------|-------------|---------|
| NED | I | Eredivisie | High |
| NED | II | Keuken Kampioen Divisie | Medium-Low |
| BEL | I | Belgian Pro League | Medium |
| BEL | II | Challenger Pro League | Medium-Low |
| POR | I | Primeira Liga | Medium-High |
| POR | II | Ledman LigaPro | Low |
| SWE | I | Allsvenskan | Medium |
| SWE | II | Superettan | Low |
| NOR | I | Eliteserien | Medium |
| NOR | II | OBOS Ligaen | Low |
| FIN | I | Veikkausliiga | Low |
| FIN | II | Ykkonen | Low |

## Output Files

### Per-Position Datasets (`dataset_per_position/`)

Each position group has two output files:
- `position_[group].csv` - Players with sufficient data (<=20% missing KPIs)
- `position_[group]_removed.csv` - Players removed due to missing data

## Missing Value Handling

In the Driblab data:
- `-` means "not applicable" or "cannot be calculated" (e.g., division by zero)
- `0` means the player attempted something but the result was zero
- `null` means the data is missing

Both `-` and `null` are treated as missing values for filtering purposes.

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Requirements

- pandas
- requests
- beautifulsoup4

## Full Processing Pipeline

To process the complete dataset from scratch:

```bash
# 1. Add market values from Transfermarkt (takes time due to API calls)
python helper_functions/append_market_values.py

# 2. Add league quality metadata
python helper_functions/append_league_quality.py

# 3. Calculate player ages
python helper_functions/calculate_age.py

# 4. Clean and split by position
python helper_functions/remove_missing_rows.py
```
