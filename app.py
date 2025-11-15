from flask import Flask
from flask import render_template, request
import pandas as pd
import folium

app = Flask(__name__)

df = pd.read_csv("static/data_populasi.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    # Default filters
    min_pop = request.form.get("min_pop", 0, type=int)
    keyword = request.form.get("keyword", "", type=str)

    filtered = df[
        (df["populasi"] >= min_pop) &
        (df["nama"].str.contains(keyword, case=False, na=False))
    ]

    m = folium.Map(location=[-6.5, 107.0], zoom_start=8)
    for _, row in filtered.iterrows():
        popup = f"{row['nama']}<br>Populasi: {row['populasi']:,}"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup,
            tooltip=row["nama"]
        ).add_to(m)

    # Save map to HTML string
    map_html = m._repr_html_()

    return render_template("home.html", map_html=map_html, min_pop=min_pop, keyword=keyword)

if __name__ == '__main__':
    # debug=True untuk development (auto-reload + debugger)
    app.run(debug=True)