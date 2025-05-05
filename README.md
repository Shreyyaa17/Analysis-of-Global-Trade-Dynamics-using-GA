# 🌍 Global Trade Network

An interactive Streamlit web application that allows users to explore and visualize international trade data. Upload your own CSV, select a country, and view its top 10 trading partners through a dynamic map, bar chart, and network graph.

![Global Trade Network Screenshot]
![Screenshot 2025-05-03 182355](https://github.com/user-attachments/assets/94741048-f734-4f41-80b0-a056694013d5)
![Screenshot 2025-05-03 182226](https://github.com/user-attachments/assets/a46935d6-a455-456f-abd9-12116d1f75b0)


---

## 🚀 Features

- 📂 **Upload Your Trade CSV**  
  Upload a CSV file with columns like `ReporterName`, `PartnerName`, and `TradeValue in 1000 USD`.

- 🌐 **Interactive World Map**  
  View a folium-based map showing trade connections between the selected country and its top 10 partners.

- 📊 **Bar Chart Visualization**  
  Quickly compare trade values with a Seaborn horizontal bar chart.

- 🕸️ **Trade Network Graph**  
  Visualize country-to-country connections using NetworkX with multiple layout options.

- 📈 **Summary Statistics & Table**  
  Inspect top trading data, download it as CSV, and view summary stats (mean, std, etc.).

---

## 📁 Example CSV Format

Your CSV should contain the following columns:

| ReporterName | PartnerName | TradeValue in 1000 USD |
|--------------|-------------|-------------------------|
| India        | China       | 15000                   |
| India        | USA         | 12000                   |
| ...          | ...         | ...                     |

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [NetworkX](https://networkx.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [Matplotlib](https://matplotlib.org/)

