from PIL import Image
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fullpage_screenshot(driver, filename):
    # Assuming you have already initialized the WebDriver as 'driver'
    # and navigated to the page containing the table
    driver.implicitly_wait(10)  # Wait for 10 seconds

    # Use the WebDriverWait to ensure the element is present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'tablaMaestra')))

    # Get the dimensions of the div
    div_width = driver.execute_script("return document.getElementById('tablaMaestra').offsetWidth")
    div_height = driver.execute_script("return document.getElementById('tablaMaestra').offsetHeight")

    # Add some extra space to ensure the entire div is captured
    extra_space = 100
    new_width = div_width + extra_space
    new_height = div_height + extra_space

    # Resize the browser window
    driver.set_window_size(new_width, new_height)

    div = driver.find_element(By.ID, "tablaMaestra")
    div.screenshot(filename)  # saves the screenshot in the current directory


def create_svg_table(all_stats, driver, filename='table.png'):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    html_start = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Statistics Table</title>
        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            html,
            body,
            .intro {
            height: 100%;
            }

            table td,
            table th {
            text-overflow: ellipsis;
            white-space: nowrap;
            overflow: hidden;
            }

            .card {
            border-radius: .5rem;
            }

            .progress-bar-lgreen {
                color: #000 !important;
                background-color: #f1f1f1 !important;
                text-align: center;
                line-height: 24px;
            }
            .green {
                color: #000 !important;
                background-color: #4CAF50 !important;
                line-height: 24px;
            }
        </style>
    </head>
    <body>
        <section class="intro">
            <div class="mask d-flex align-items-center h-100" style="background-color: rgba(25, 185, 234,.25);">
            <div id="tablaMaestra" class="container">
                <div class="row justify-content-center">
                <div class="col-12">
                    <div class="card">
                    <div class="card-body">
                        <div class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead>
                                <tr>
                                    <th scope="col">Guild Name</th>
                                    <th scope="col">Character Name</th>
                                    <th scope="col">Current Tier</th>
                                    <th scope="col">Score [Current/Next]</th>
                                </tr>
                            </thead>
                            <tbody>
    """

    html_end = """
                        </tbody>
                    </table>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
        </div>
    </section>
    </body>
    </html>
    """

    # Función para generar las filas de la tabla
    def generate_table_rows(all_stats):
        # Crear una lista plana de todos los registros
        all_records = []
        for guild_name, stats in all_stats.items():
            for character_name, character_stats in stats.items():
                all_records.append({
                    "Guild Name": guild_name,
                    "Character Name": character_name,
                    "Current Tier": character_stats['player_tier'],
                    "Score [Current/Next]": f"{character_stats['current_score']:.1f} / {character_stats['next_score']:.1f}"
                })

        # Ordenar los registros por Character Name
        sorted_records = sorted(all_records, key=lambda x: x["Character Name"])

        # Generar las filas HTML para la tabla
        rows = ""
        for record in sorted_records:
            current_str, next_str = record["Score [Current/Next]"].split("/")
            current = int(float(current_str))
            next = int(float(next_str))
            progress = int(current / next * 100)

            tier_image_html = {
                "Captain": f'<img src="{os.path.join(current_dir,"assets/tier1.png")}" width="30">',
                "Marauder": f'<img src="{os.path.join(current_dir,"assets/tier2.png")}" width="30">',
                "Seafarer": f'<img src="{os.path.join(current_dir,"assets/tier3.png")}" width="30">',
                "Castaway": f'<img src="{os.path.join(current_dir,"assets/tier4.png")}" width="30">',
            }[record["Current Tier"]]

            tier_html = f'<div style="text-align: center;">{tier_image_html}</div>'

            rows += f"""
                <tr>
                    <td>{record["Guild Name"]}</td>
                    <td>{record["Character Name"]}</td>
                    <td>{tier_html}</td>
                    <td style="text-align: center;">
                        <div class="progress-bar-lgreen">
                            <div class="green" style="height:24px;width:{progress}%">
                            </div>
                        </div>
                            {current:,} / {next:,}
                        <br>
                    </td>
                </tr>
            """
        return rows

    # Combina todo para formar el HTML completo
    html_table = html_start + generate_table_rows(all_stats) + html_end

    # Save the HTML to a temporary file
    temp_html_path = os.path.join(current_dir, 'temp_table.html')
    with open(temp_html_path, 'w') as file:
        file.write(html_table)

    # Assuming you have already initialized a driver elsewhere
    # For example: driver = webdriver.Chrome(options=your_options)
    # Load the temporary HTML file
    driver.get('file://' + temp_html_path)

    # Take a full page screenshot
    fullpage_screenshot(driver, filename)

    # Optionally, remove the temporary file if not needed anymore
    os.remove(temp_html_path)