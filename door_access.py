import cv2
import sqlite3

def check_token(token):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visits WHERE token=?", (token,))
    data = cursor.fetchone()
    conn.close()
    return data

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(frame)

    if data:
        if check_token(data):
            print("Access Granted")
            # Code to open the door (you will need to add your hardware control code here)
        else:
            print("Invalid Token")

    cv2.imshow("QR Code Scanner", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
