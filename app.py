from flask import Flask, request, render_template
import json

app = Flask(__name__)

# Load dataset dari file JSON
with open("resep.json", encoding="utf-8") as f:
    semua_resep = json.load(f)

# Fungsi rekomendasi berdasarkan input bahan
def rekomendasi_resep(input_bahan, semua_resep, ambang_skor=0.3):
    hasil = []
    input_set = set(map(str.strip, map(str.lower, input_bahan)))

    for resep in semua_resep:
        cocok = 0
        total = len(resep['bahan'])

        for ib in input_set:
            for b in resep['bahan']:
                if ib in b.lower():
                    cocok += 1
                    break  # hindari duplikat hitung

        if total > 0:
            skor = cocok / total
            if skor >= ambang_skor:
                hasil.append((skor, resep))

    hasil.sort(reverse=True, key=lambda x: x[0])
    return [r[1] for r in hasil]


# Route utama
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_bahan = request.form["bahan"].split(",")
        hasil = rekomendasi_resep(input_bahan, semua_resep)
        return render_template("hasil.html", hasil=hasil)
    return render_template("index.html")

# Jalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)


