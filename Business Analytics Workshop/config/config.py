# Position mapping - custom mapping
POSITION_MAPPING = {
    "Centre back": ["DC"],
    "Full back": ["DR", "DL"],
    "6": ["DMC", "MC"],
    "8": ["MC", "ML", "MR"],
    "10": ["AMC", "MC", "AML", "AMR"],
    "7": ["AML", "AMR", "FWL", "FWR"],
    "9": ["FW"]
}

# KPIs per position - custom mapping
POSITION_KPIS = {
    "Centre back": [
        # Defensive actions & duels
        # "Tackles/Was Dribbled 2/3",
        "Tackles Attempted",
        "Successful Tackles",
        "Blocked Shots",
        "Defensive Actions",
        "% High Defensive Actions",
        "Individual Pressure",
        "Individual Pressure Opp. Half",
        "Aggresive Actions",
        "Recoveries",
        "Quick Recoveries",
        "% Quick Recoveries",
        "Diff. Defensive Distance Team",
        # Aerial dominance
        "Aerial Duels",
        "Aerial Wins",
        "% Aerial Wins",
        "Aerial Wins Defensive",
        "% Aerial Defensive",
        "Aerial Wins Own Box",
        # Passing & build-up (low-risk)
        "Passes",
        "% Passing",
        "Successful Short Passes",
        "Completed Long Balls",
        "% Long Balls",
        "Passes per Long Ball",
        "Average Pass Distance",
        # "Long Balls Received",
        "Passes into Final 1/3",
        "xG Build Up in Team",
        # Discipline
        # "Fouls",
        # "Yellow Cards",
        # "Red Cards",
        # 
        # Excelsior
        # Attacking
        "% Passing Contribution",
        "% Long Balls",
        "xG Build Up",
        "Ball Prog. by Passing",
        # Defensive
        "% Aerial Wins Own Box",
        "Tackles/Was Dribbled",
        "% Ground Duels",
        "Interceptions",
        "Clearances",
    ],
    "Full back": [
        # Defensive work
        "Tackles Attempted",
        "Successful Tackles",
        "Defensive Actions",
        "Recoveries",
        "Individual Pressure",
        "Individual Pressure Opp. Half",
        "Aggresive Actions",
        "Clearances",
        # Wide progression & crossing
        "Progressive Carries",
        "% Carries",
        "Average Carries Progress",
        "Deep Progression",
        "Entries Opp. Box",
        "Completed Crosses",
        "% Crossing",
        "Cross Efficiency",
        "Passes into Final 1/3",
        "OP Passes into Box",
        # Passing & ball movement
        "Passes",
        "% Passing",
        "Successful Short Passes",
        "Completed Long Balls",
        "Average Pass Distance",
        "Ball Progression",
        "Ball Prog. by Passing",
        "Ball Prog. by Carrying",
        # Chance contribution
        "Chances Created Open Play",
        "xAssists Open Play",
        "Assists",
        # 
        # Excelsior
        # Attacking
        "Chances Created",
        "Expected Assists",
        "Expected Threat (xT)",
        "xG Chain",
        # Defensive
        "Fouls",
        "Tackles/Was Dribbled",
        "% Ground Duels",
        "Aerial Efficiency",
        "Interceptions",
    ],
    "6": [
        # Defensive shielding
        "Tackles/Was Dribbled",
        "Tackles Attempted",
        "Successful Tackles",
        "Quick Recoveries",
        "% Quick Recoveries",
        "Aggresive Actions",
        # Ball circulation & retention
        "Passes",
        "% Passing Contribution",
        "Successful Short Passes",
        "% Ball Retention",
        "% Ball Retention in Opp. Half",
        "Average Pass Distance",
        # Progression from deep
        "Passes into Final 1/3",
        "Completed Long Balls",
        "% Long Balls",
        "Ball Progression",
        "Ball Prog. by Passing",
        "Progressive Carries",
        "xG Build Up in Team",
        "xG Chain",
        # Discipline
        "Fouls",
        "Yellow Cards",
        "Red Cards",
        # 
        # Excelsior
        # Attacking
        "Dispossessed",
        "% Passing",
        "xG Build Up",
        "Ball Prog. by Passing",
        # Defensive
        "% Ground Duels",
        "Individual Pressure",
        "Recoveries",
        "Defensive Actions",
        "Interceptions",
        "Aerial Efficiency",
    ],
    "8": [
        # Box-to-box contribution
        "Tackles/Was Dribbled",
        "Successful Tackles",
        "Individual Pressure Opp. Half",
        # Passing & tempo
        "Passes",
        "% Passing",
        "Passes into Final 1/3",
        "Successful Short Passes",
        "Completed Long Balls",
        "Average Pass Distance",
        # Progression & carries
        "Ball Progression",
        "Ball Prog. by Passing",
        "Ball Prog. by Carrying",
        "Progressive Carries",
        "% Carries",
        "Average Carries Progress",
        # Chance creation
        "Chances Created",
        "Chances Created Open Play",
        "Expected Assists",
        "xAssists Open Play",
        "Open Play Key Passes",
        "OP Passes into Box",
        # Goal threat (secondary)
        "Shots",
        "Expected Goals",
        "xG per Shot",
        "Non-Penalty Goals",
        # 
        # Excelsior
        # Attacking
        "% Passing Contribution",
        "Entries Opp. Box",
        "Expected Threat (xT)",
        "xG Chain",
        "xG Build Up",
        # Defensive
        "% Ground Duels",
        "Individual Pressure",
        "Recoveries",
        "Defensive Actions",
        "Interceptions",
        "Aerial Efficiency",
    ],
    "7": [
        # 1v1 & ball carrying
        "Successful Dribbles",
        "Dribbles Attempted",
        "% Successful Dribbles",
        "Dribbles Opp. Half",
        "Progressive Carries",
        "% Carries",
        "Average Carries Progress",
        # Chance creation from wide
        "Chances Created",
        "Chances Created Open Play",
        "Completed Crosses",
        "% Crossing",
        "Cross Efficiency",
        "OP Passes into Box",
        "Open Play Key Passes",
        "xAssists Open Play",
        # Attacking threat
        "Shots",
        "Non-Penalty Goals",
        "Expected Goals",
        "xG per Shot",
        "Touches In Opponent Box",
        "Goal Ending Carries",
        "Shot Ending Carries",
        # Ball progression & threat
        "Ball Prog. by Carrying",
        "xT Open Play",
        "xT Dribbling",
        "xT OP in Team",
        # 
        # Excelsior
        # Attacking
        "Progressive Passes Receive into Box",
        "Expected Threat (xT)",
        "Expected Assists",
        "xG Chain",
        "Ball Progression",
        # Defensive
        "% High Defensive Actions",
        "Individual Pressure",
        "Recoveries",
    ],
    "10": [
        # Creative output
        "Chances Created",
        "Chances Created Open Play",
        "Open Play Key Passes",
        "OP Passes into Box",
        "Expected Assists",
        "xAssists Open Play",
        "Assists",
        "xG Build Up",
        # Ball progression in final third
        "Ball Progression",
        "Ball Prog. by Passing",
        "Ball Prog. by Carrying",
        "Progressive Carries",
        "Touches In Opponent Box",
        # Dribbling & retention
        "Successful Dribbles",
        "Dribbles Attempted",
        "% Successful Dribbles",
        "% Ball Retention",
        "% Ball Retention in Opp. Half",
        # Scoring support
        "Shots",
        "Expected Goals",
        "Non-Penalty Goals",
        "xG on Target",
        "Finishing",
        # 
        # Excelsior
        # Attacking
        "Progressive Passes Receive into Box",
        "Ball Retention in Opp. Half",
        "Entries Opp. Box",
        "xG per Shot",
        "xG Chain",
        "Expected Threat (xT)",
        # Defensive
        "% High Defensive Actions",
        "Individual Pressure Opp. Half",
        "Recoveries",
    ],
    "9": [
        # Goal scoring
        "Non-Penalty Goals",
        "Goals",
        "Shots",
        "Expected Goals",
        "xG per Shot",
        "xG on Target",
        "Finishing",
        "Finishing xGOT",
        # Penalty-box presence
        "Touches In Opponent Box",
        "Shot Ending Sequence",
        "Goal Ending Sequence",
        # Aerial & physical play
        "Aerial Duels",
        "Aerial Wins",
        "% Aerial Wins",
        "Aerial Wins Offensive",
        "Aerial Wins Opp Box",
        "% Aerial Wins Opp. Box",
        "Headers",
        "Header per Shot",
        "Header per Cross",
        # Link-up & contribution
        "Assists",
        "Chances Created",
        "xG Chain",
        "xG Build Up",
        "Open Play Key Passes",
        # 
        # Excelsior
        # Attacking
        "% Ball Retention in Opp. Half",
        "Entries Opp. Box",
        "Expected Threat (xT)",
        "xG per NPG",
        "Aerial Efficiency",
        "Deep Progression"
        # Defensive
        "% High Defensive Actions",
        "Individual Pressure Opp. Half",
        "Recoveries",
    ]
}

AGE_GROUPS = ["<21", "21-23", "24-26", "27+"]

STAGE_BY_AGEGROUP = {
    "<21": "Early Talent",
    "21-23": "Developing Talent",
    "24-26": "Prime Transition",
    "27+": "Established Player"
}

STAGE_MINUTES = {
    "Early Talent": 150,
    "Developing Talent": 300,
    "Prime Transition": 600,
    "Established Player": 600
}

MINUTES_PERCENTILE_Q = 0.10
MINUTES_COLUMN = "Minutes"

PEER_GROUP_COLS = ["League_Name", "age_group"]

#Threshhold for binary indicating significant transfermarkt value increase:
TMV_DELTA_THRESHOLD = 50000

#Threshold for the proportion of data that can be missing to drop a row or KPI from the regression df
MISSING_THRESHOLD = 0.2

#Minimum minitus for the row to be included in the regresion
MIN_MINUTES_CUTOFF = 300