from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

last_scan = "No QR scanned yet"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bus QR Scanner</title>
    <meta http-equiv="refresh" content="2">
</head>
<body style="font-family:Arial">

<h1>🚍 Smart Bus QR Scanner</h1>

<h2>Latest Scan</h2>

<div style="padding:20px;background:#f4f4f4;border-radius:10px;width:500px;">
{{data}}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, data=last_scan)


@app.route("/scan", methods=["POST"])
def scan():

    global last_scan

    data = request.get_json()

    last_scan = data.get("qr", "")

    print("QR Received:", last_scan)

    return jsonify({
        "success": True,
        "message": "QR received successfully."
    })


if __name__ == "__main__":
    app.run(debug=True)