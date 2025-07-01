import cv2
import pandas as pd

# Load color dataset from GitHub
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(
    'https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv',
    names=index,
    header=None
)

# Load your image (update the path)
img = cv2.imread(r'C:\Users\Sreeja\OneDrive\Desktop\image2.jpg')

# Check if image is loaded
if img is None:
    print("❌ Error: Image not found.")
    exit()
else:
    print("✅ Image loaded successfully.")

# Resize image
img = cv2.resize(img, (800, 600))

clicked = False
r = g = b = xpos = ypos = 0

# Function to get color name from RGB
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse click event
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)
        print(f"Clicked at ({x}, {y}) - R={r}, G={g}, B={b}")

# Setup OpenCV window
cv2.namedWindow('Color Detection')
cv2.setMouseCallback('Color Detection', draw_function)

while True:
    cv2.imshow("Color Detection", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = f"{get_color_name(r, g, b)} R={r} G={g} B={b}"
        text_color = (255, 255, 255) if r + g + b < 400 else (0, 0, 0)
        cv2.putText(img, text, (50, 50), 2, 0.8, text_color, 2, cv2.LINE_AA)
        clicked = False
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
