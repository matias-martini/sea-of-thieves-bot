import svgwrite
import cairosvg

# goal_hoarders_stats = {'Shaddy Link': {'player_tier': 'Marauder', 'next_score': 481500.0, 'next_tier': 'Captain', 'current_score': 349800.0}, 'Maestruli666': {'player_tier': 'Marauder', 'next_score': 481500.0, 'next_tier': 'Captain', 'current_score': 349800.0}, 'Lesterlarata69': {'player_tier': 'Marauder', 'next_score': 481500.0, 'next_tier': 'Captain', 'current_score': 349800.0}}
# order_of_souls_stats = {'Lesterlarata69': {'player_tier': 'Captain', 'next_score': 28230837.0, 'next_tier': 'Top 1', 'current_score': 479403.0}, 'Maestruli666': {'player_tier': 'Marauder', 'next_score': 436350.0, 'next_tier': 'Captain', 'current_score': 364539.0}, 'Shaddy Link': {'player_tier': 'Marauder', 'next_score': 436350.0, 'next_tier': 'Captain', 'current_score': 276153.0}, 'ProYoloMcSwag': {'player_tier': 'Marauder', 'next_score': 436350.0, 'next_tier': 'Captain', 'current_score': 203250.0}}
# athenas_stats = {'Shaddy Link': {'player_tier': 'Captain', 'next_score': 23684580.0, 'next_tier': 'Top 1', 'current_score': 354600.0}, 'Lesterlarata69': {'player_tier': 'Captain', 'next_score': 23684580.0, 'next_tier': 'Top 1', 'current_score': 354600.0}, 'ProYoloMcSwag': {'player_tier': 'Marauder', 'next_score': 275850.0, 'next_tier': 'Captain', 'current_score': 145200.0}}
# merchant_stats = {'Lesterlarata69': {'player_tier': 'Seafarer', 'next_score': 214950.0, 'next_tier': 'Marauder', 'current_score': 144858.0}, 'Maestruli666': {'player_tier': 'Castaway', 'next_score': 78459.0, 'next_tier': 'Seafarer', 'current_score': 41550.0}}
# reaper_stats = {'ProYoloMcSwag': {'player_tier': 'Seafarer', 'next_score': 244560.0, 'next_tier': 'Marauder', 'current_score': 104529.0}, 'Shaddy Link': {'player_tier': 'Seafarer', 'next_score': 244560.0, 'next_tier': 'Marauder', 'current_score': 104529.0}, 'Lesterlarata69': {'player_tier': 'Seafarer', 'next_score': 244560.0, 'next_tier': 'Marauder', 'current_score': 104529.0}}


# # Combine all the stats
# all_stats = {
#     "Goal Hoarders": goal_hoarders_stats,
#     "Order of Souls": order_of_souls_stats,
#     "Athena's": athenas_stats,
#     "Merchant Alliance": merchant_stats,
#     "Reaper's Bones": reaper_stats
# }


def create_svg_table(all_stats, filename='table.svg'):
    # Combine all stats into one list
    data = []
    for guild_name, stats in all_stats.items():
        for character_name, character_stats in stats.items():
            data.append({
                "Guild Name": guild_name,
                "Character Name": character_name,
                "Current Tier": character_stats['player_tier'],
                "Score [Current/Next]": f"{character_stats['current_score']:.1f} / {character_stats['next_score']:.1f}"
            })
    # Table dimensions and styles
    column_widths = [150, 150, 120, 200]
    row_height = 25
    header_height = 35
    header_fill = '#333333'
    row_fill_1 = '#f2f2f2'
    row_fill_2 = '#ffffff'
    header_font_color = '#ffffff'
    row_font_color = '#000000'

    # Calculate the width and height of the table
    width = sum(column_widths)
    height = header_height + row_height * len(data)

    # Create an SVG drawing
    dwg = svgwrite.Drawing(filename.replace('.png', '.svg'), size=(width, height))

    # Add header
    headers = ["Guild Name", "Character Name", "Current Tier", "Score [Current/Next]"]
    for i, header in enumerate(headers):
        dwg.add(dwg.rect(insert=(sum(column_widths[:i]), 0), size=(column_widths[i], header_height), fill=header_fill))
        dwg.add(dwg.text(header, insert=(sum(column_widths[:i]) + 5, header_height - 10),
                         fill=header_font_color, font_size='15px', font_weight="bold"))

    # Add rows with alternating colors
    for row_idx, row in enumerate(data):
        y = header_height + row_idx * row_height
        bg_color = row_fill_1 if row_idx % 2 == 0 else row_fill_2
        dwg.add(dwg.rect(insert=(0, y), size=(width, row_height), fill=bg_color))
        for col_idx, col_name in enumerate(headers):
            value = str(row[col_name])
            x = sum(column_widths[:col_idx]) + 5
            dwg.add(dwg.text(value, insert=(x, y + row_height - 7), fill=row_font_color, font_size='12px'))

    # Save the SVG file
    dwg.save()

    # Convert SVG to PNG
    cairosvg.svg2png(url=filename.replace('.png', '.svg'), write_to=filename)