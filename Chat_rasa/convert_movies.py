import pandas as pd
import json

# CSV dosyasının tam yolunu belirt
file_path = r"C:\Users\omerf\FilmVeriSeti\movie.csv"  # Windows için 'r' ekledim

# CSV dosyasını yükle
df = pd.read_csv(file_path)

# JSON formatına dönüştür
movies_json = df[['title', 'genres']].to_dict(orient='records')

# JSON dosyasını Rasa klasörüne kaydet
output_path = "movies.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(movies_json, f, indent=4, ensure_ascii=False)

print(f"Veri JSON formatına dönüştürüldü ve '{output_path}' olarak kaydedildi.")

