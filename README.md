# Soccer Analytics Project

This is an end-to-end data analysis project using StatsBomb open data. The data processed in this project is based on soccer match "Events" including shots, passes, tackles, etc and includes information such as location of event, player, team, etc. The project was intended to be used as a learning experience and a way to be exposed to the full pipeline of tools needed in the progression below:

StatsBomb JSON → Python (pandas) → SQL Server LocalDB → SQL analysis → visualization → machine learning

## Goals
- Start with raw json data and turn it into meaningful analysis
- Visualize passing patterns
- Visualize shot patterns
- Create my own Shot xG prediction (scikit-learn regression) based on StatsBomb data

## Tools
- Python
- pandas
- NumPy
- SQL
- matplotlib / seaborn
- mplsoccer
- scikit-learn
- Power BI

## Results
Here is an example of a single analysis done from beginning (raw JSON data) to end (data plotted on pitch using matplotlib).

First, the full dataframe on the SQL Server is queried for passes (in this case) using the SQL Query shown below. The processed data is then loaded into its own csv file.
<img width="696" height="306" alt="image" src="https://github.com/user-attachments/assets/0c52c8db-104d-4777-a621-fb1759607241" />

<img width="253" height="147" alt="image" src="https://github.com/user-attachments/assets/39b64f5b-7d4a-4e68-b9ce-598fb8261942" />

Then, the csv file data of passes is used to create a visualization through matplotlib and mplsoccer.
<img width="674" height="548" alt="image" src="https://github.com/user-attachments/assets/c3b1ba1c-42f2-4b46-a942-4b410d80eb09" />

Here is the final output visualization of all passes plotted as a heatmap.
<img width="1200" height="800" alt="passheatmap_allteams" src="https://github.com/user-attachments/assets/f5f50b91-5541-49d8-a9c1-9e9bb03d3b5c" />

## Visualizations
Here are the rest of the visualizations plotted throughout the project.

