import cv2
import requests
from tkinter import Tk, filedialog

SERVER = "http://127.0.0.1:5000/scan"

# Hide Tkinter window
root = Tk()
root.withdraw()

# Select image
image_path = filedialog.askopenfilename(
    title="Select QR Code Image",
    filetypes=[
        ("Image Files", "*.png *.jpg *.jpeg *.bmp")
    ]
)

if image_path == "":
    print("No image selected.")
    exit()

print("Selected:", image_path)

# Read image
image = cv2.imread(image_path)

if image is None:
    print("Cannot open image.")
    exit()

# Detect QR
detector = cv2.QRCodeDetector()

data, points, _ = detector.detectAndDecode(image)

if data:

    print("\n========== QR CONTENT ==========")
    print(data)
    print("================================\n")

    # Send to Flask
    try:
        response = requests.post(
            SERVER,
            json={"qr": data},
            timeout=5
        )

        print("Server Response:")
        print(response.json())

    except Exception as e:
        print("Cannot connect to Flask server.")
        print(e)

    # Draw QR box
    if points is not None:

        points = points.astype(int)

        for i in range(len(points[0])):
            pt1 = tuple(points[0][i])
            pt2 = tuple(points[0][(i + 1) % len(points[0])])

            cv2.line(image, pt1, pt2, (0, 255, 0), 3)

        cv2.putText(
            image,
            "QR Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

else:

    cv2.putText(
        image,
        "NO QR FOUND",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    print("No QR Code detected.")

cv2.imshow("QR Scanner", image)
cv2.waitKey(0)
cv2.destroyAllWindows()