from bs4 import BeautifulSoup

TIERS = {
  5: "Top 1",
  4: "Captain",
  3: "Marauder",
  2: "Seafarer",
  1: "Castaway"
}


def get_lowest_score_by_tier(html):
    tier_lower_scores = {TIERS[5]: 1E10, TIERS[4]: 1E10, TIERS[3]: 1E10, TIERS[2]: 1E10, TIERS[1]: 0}

    soup = BeautifulSoup(html, 'html.parser')
    all_divs = soup.find_all(
        'div',
        class_='ledger-table__row ledger-table__row-enter-done'
    )

    highest_score = 0

    for div in all_divs:
        tier_int = int(div.find("img")["src"].split("tier-")[-1].split(".")[0])
        tier = TIERS[tier_int]

        if tier == "Castaway":
            continue

        score = float(div.find('div', class_="ledger-table__row-score").text.replace(",",""))
        highest_score = max(highest_score, score)
        tier_lower_scores[tier] = min(tier_lower_scores[tier], score)

        tier_lower_scores["Top 1"] = highest_score

    return tier_lower_scores


def get_player_stats(player_scores, tier_map):
    player_tiers = {}

    for player, score in player_scores.items():
        player_next_score_to_rise = score
        next_tier = "Top 1"
        for tier, threshold in tier_map.items():
            if score >= threshold:
                player_tier = tier
                break
            else:
                player_next_score_to_rise = threshold
                next_tier = tier
        player_tiers[player] = {
          "player_tier": player_tier,
          "next_score": player_next_score_to_rise,
          "next_tier": next_tier,
          "current_score": score
        }

    return player_tiers


def get_friend_scores(html):
    soup = BeautifulSoup(html, 'html.parser')
    player_sections = soup.find_all('div', class_=[
      'ledger-table__row ledger-table__row-enter-done',
      'ledger-table__row ledger-table__row-includes-user '
      'ledger-table__row-enter-done'
    ])

    player_scores = {}
    for player in player_sections:
        name_div = player.find(
            'div',
            class_='ledger-table__row-names--gamertag'
        )
        name = name_div.text

        score_div = player.find('div', class_='ledger-table__row-score')
        score = score_div.text.replace(",", "")

        player_scores[name] = float(score)

    return player_scores
