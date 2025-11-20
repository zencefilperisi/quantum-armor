from flask import Flask, request, render_template_string
from auto_migrator import LegacyToPQC_Migrator
import os

app = Flask(__name__)

HTML_FORM = """
<form method="POST">
    Proje Yolu:<br><input name="project_path" value=".." size=40><br>
    Algoritma:<br>
    <select name="pqc_algo">
        <option value="kyber">Kyber</option>
        <option value="dilithium">Dilithium</option>
    </select><br>
    <input type="submit" value="Projeyi Kuantum-Dirençli Yap">
</form>
{% if result %}
<h3>Sonuç:</h3><pre>{{ result }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        path = request.form.get("project_path", "..")
        algo = request.form.get("pqc_algo", "kyber")
        migrator = LegacyToPQC_Migrator(pqc_algo=algo)
        migrator.migrate_project(path)
        result = "Migrasyon tamamlandı! Detaylar için migration_report.json'a bakınız."
    return render_template_string(HTML_FORM, result=result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)