# Sai

import cv2
import time
import google.generativeai as genai

def gemini_search():
    # ---- CONFIG ----
    with open("../secret_key.txt", "r") as s:
        API_KEY = s.read().strip()

    PROMPT = (
        "Describe what plant disease you see in this image in the format:\n"
        "Name: ...\nDescription: ...\nCause: ...\nProblem: ...\nCure: ..."
    )

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro")

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Camera not accessible")

    print("Press SPACE to capture image, ESC to quit")

    result_text = ""  # Store Gemini result
    while True:
        ret, frame = cam.read()
        if not ret:
            print("⚠️ Failed to read frame from camera.")
            break

        cv2.imshow("Press SPACE to capture", frame)
        key = cv2.waitKey(10)

        if key == 27:
            print("Exiting.")
            break
        elif key == 32:
            img_path = f"capture_{int(time.time())}.jpg"
            cv2.imwrite(img_path, frame)
            print("📸 Image captured, sending to Gemini...")

            try:
                with open(img_path, "rb") as f:
                    response = model.generate_content(
                        [PROMPT, {"mime_type": "image/jpeg", "data": f.read()}]
                    )

                result_text = response.text.strip()

                # Save and exit camera loop
                with open("gemini_results.txt", "a") as log:
                    log.write(f"{img_path}: {result_text}\n\n")
                break

            except Exception as e:
                result_text = f"⚠️ Error contacting Gemini: {e}"
                break

    cam.release()
    cv2.destroyAllWindows()
    return result_text