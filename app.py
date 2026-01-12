from flask import Flask, render_template, request
import os

# === Matplotlib SAFE MODE ===
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None

    if request.method == "POST":
        try:
            interarrival = float(request.form.get("interarrival"))
            service_time = float(request.form.get("service"))

            if interarrival <= 0 or service_time <= 0:
                raise ValueError("Nilai harus positif")

            # Parameter M/M/2
            lamda = 1 / interarrival
            mu = 1 / service_time

            if mu <= lamda / 2:
                raise ValueError("Sistem tidak stabil")

            rho = lamda / (2 * mu)
            W = 1 / (mu - lamda / 2)
            Wq = (lamda ** 2) / (2 * mu * (mu - lamda / 2))

            hasil = {
                "lambda": round(lamda, 4),
                "mu": round(mu, 4),
                "rho": round(rho, 4),
                "W": round(W, 4),
                "Wq": round(Wq, 4),
            }

            # ===== GRAFIK (SAFE) =====
            grafik_path = os.path.join("static", "grafik.png")
            os.makedirs("static", exist_ok=True)

            plt.figure(figsize=(5, 4))
            plt.bar(
                ["Waktu Antrian (Wq)", "Waktu Sistem (W)"],
                [Wq, W]
            )
            plt.ylabel("Waktu (menit)")
            plt.title("Grafik Antrian M/M/2")
            plt.tight_layout()
            plt.savefig(grafik_path)
            plt.close()

        except Exception as e:
            hasil = "error"

    return render_template("index.html", hasil=hasil)

# === WAJIB UNTUK RAILWAY ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
