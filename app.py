from flask import Flask, render_template, request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None

    if request.method == "POST":
        try:
            interarrival = float(request.form["interarrival"])
            service_time = float(request.form["service"])

            if interarrival <= 0 or service_time <= 0:
                raise ValueError

            lamda = 1 / interarrival
            mu = 1 / service_time

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

            plt.figure()
            plt.bar(["Wq", "W"], [Wq, W])
            plt.title("Perbandingan Wq dan W")
            plt.savefig("static/grafik.png")
            plt.close()

        except Exception as e:
            print(e)
            hasil = "error"

    return render_template("index.html", hasil=hasil)
