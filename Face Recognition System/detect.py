import cv2
import tkinter as tk
from tkinter import ttk
import pymongo
from PIL import Image, ImageTk
from pathlib import Path
import tkinter.messagebox

# MongoDB connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['SENEW']
collection = db['students']

# Load face cascade classifier and face recognizer
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingdata.yml")

def get_profile(student_id):
    try:
        student_id_str = str(student_id)
        profile = collection.find_one({'Id': student_id_str})
        return profile
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None

def authenticate_face():
    cam = cv2.VideoCapture(0)
    while True:
        ret, img = cam.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            student_id, conf = recognizer.predict(roi_gray)
            print("Confidence: ",conf)

            if 55 < conf < 100:
                profile = get_profile(student_id)
                if profile:
                    if profile.get('status', '') == 'YES':
                        tkinter.messagebox.showinfo("Information", "You have already voted.")
                        return
                    name = profile.get('Name', 'Unknown')
                    id = profile.get('Id', 'Unknown')
                    age = profile.get('age', 'Unknown')
                    object_id = profile.get('_id', 'Unknown')
                    status = profile.get('status', 'Unknown')

                    print(f"Detected Profile - Name: {name}, ID: {student_id}, Age: {age}, ObjectID: {object_id},Status:{status}")

                    # Release camera and destroy OpenCV window
                    cam.release()
                    cv2.destroyAllWindows()

                    # Open new dashboard window
                    show_dashboard(name, age, profile,id)
                    return
            else:
                print("User Not match")

            # Draw rectangle around detected face (increase size)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)

        # Calculate screen center and display OpenCV window centered
        screen_center_x = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
        screen_center_y = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
        cv2.imshow("Face Recognition", img)
        cv2.moveWindow("Face Recognition", screen_center_x - 300, screen_center_y - 200)  # Center window

        if cv2.waitKey(1) == ord('q'):
            break

    # Release camera and destroy OpenCV window if loop breaks
    cv2.destroyAllWindows()
    cam.release()


def show_dashboard(name, age, profile,id):
    # Create a Toplevel window
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Dashboard")

    # Set the size of the window
    dashboard_window.geometry("1366x768")  # Set width and height

    # Load the background image
    image_path = r"D:\SE\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0\GUIBG.jpg"
    image = Image.open(image_path)

    # Resize the image to fit the window with antialiasing
    resized_image = image.resize((1366, 768), Image.LANCZOS)

    # Convert the resized image to ImageTk format
    background_image = ImageTk.PhotoImage(resized_image)

    # Create a label to display the background image
    background_label = tk.Label(dashboard_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Position the label to cover the entire window

    # Ensure the image persists beyond the local scope (important!)
    background_label.image = background_image

    # Apply styles to the labels and buttons
    style = ttk.Style()
    style.configure('Dashboard.TLabel', font=('Helvetica', 14), padding=10)


    # welcome_label = ttk.Label(dashboard_window, text=f"Welcome, {name}!", style='Dashboard.TLabel')
    # welcome_label.pack()

    # Display profile details
    profile_label = ttk.Label(dashboard_window, text=f"Profile Details:\nName: {name}\nNIC: {id}", style='Dashboard.TLabel')
    profile_label.pack(pady=10)

    # Retrieve parties and candidates
    parties = get_parties()
    party_logo_map = {party['party_name']: party['logo'] for party in parties}

    # Retrieve candidates
    candidates = get_candidates()

    # Variables to keep track of selected options
    selected_options = [[tk.IntVar(value=0) for _ in range(3)] for _ in range(len(candidates))]
    preference_selected = [None, None, None]  # Tracks the selected candidate for each preference

    def on_checkbox_change(var, option, current_candidate_index):
        # Ensure only one option is selected per candidate
        for i, choice in enumerate(selected_options[current_candidate_index]):
            if choice != var:
                choice.set(0)
        # Ensure only one candidate is selected per option
        if var.get() == option:
            if preference_selected[option - 1] is not None:
                selected_options[preference_selected[option - 1]][option - 1].set(0)
            preference_selected[option - 1] = current_candidate_index
        else:
            preference_selected[option - 1] = None

    if candidates is not None and len(candidates) > 0:
        candidates_label = ttk.Label(dashboard_window, text="List of Candidates", style='Dashboard.TLabel')
        candidates_label.pack(pady=20)

        # Display candidate information
        for idx, candidate in enumerate(candidates):
            candidate_name = candidate.get('nicNumber', 'Unknown')
            candidate_party = candidate.get('partyname', 'Unknown')
            candidate_Cname = candidate.get('Cname', 'Unknown')

            candidate_frame = ttk.Frame(dashboard_window)
            candidate_frame.pack(pady=10, padx=10, fill='x')

            # Load party logo
            logo_path = party_logo_map.get(candidate_party, None)
            if logo_path:
                logo_image = Image.open(f"E:/SE/SE_dashboard/uploads/{logo_path}")
                logo_image_resized = logo_image.resize((50, 50), Image.LANCZOS)
                logo_image_tk = ImageTk.PhotoImage(logo_image_resized)

                logo_label = tk.Label(candidate_frame, image=logo_image_tk)
                logo_label.image = logo_image_tk  # Keep reference to avoid garbage collection
                logo_label.pack(side='left', padx=10)

            candidate_info_label = ttk.Label(candidate_frame, text=f" {candidate_party}", style='Dashboard.TLabel')
            candidate_info_label.pack(side='left', padx=10)
            candidate_name_label = ttk.Label(candidate_frame, text=f"  {candidate_Cname}", style='Dashboard.TLabel')
            candidate_name_label.place(x=200)

            options_frame = ttk.Frame(candidate_frame)
            options_frame.pack(side='right', padx=(50, 0), pady=5)

            for i in range(1, 4):
                checkbox = ttk.Checkbutton(options_frame, text=f"Preference {i}", variable=selected_options[idx][i-1], onvalue=i, offvalue=0, command=lambda var=selected_options[idx][i-1], opt=i, idx=idx: on_checkbox_change(var, opt, idx))
                checkbox.pack(side='left', padx=5)

    else:
        # Display message if no candidates are found
        no_candidates_label = ttk.Label(dashboard_window, text="No candidates found.", style='Dashboard.TLabel')
        no_candidates_label.pack(pady=10)

    # Add a submit button at the bottom
    submit_button = ttk.Button(dashboard_window, text="Submit", command=lambda: submit_votes(selected_options, preference_selected, dashboard_window, profile))
    submit_button.pack(pady=20)


def get_candidates():
    try:
        candidates_collection = db['candidates']
        query = {
            'ElectionName': 'Presidental'
        }
        candidates = candidates_collection.find(query)
        return list(candidates)
    except Exception as e:
        print(f"Error fetching candidates: {e}")
        return None

def get_parties():
    try:
        collection = db['parties']
        parties = list(collection.find({}))
        return parties
    except Exception as e:
        print(f"Error fetching parties: {e}")
        return []
def update_status(student_id):
    try:
        result = collection.update_one({'Id': str(student_id)}, {'$set': {'status': 'YES'}})
        if result.modified_count > 0:
            print(f"Status updated to 'YES' for student ID: {student_id}")
        else:
            print(f"No document found with student ID: {student_id} or status already 'YES'")
    except Exception as e:
        print(f"Error updating status: {e}")


def submit_votes(selected_options, preference_selected, dashboard_window, profile):
    # Ensure at least one preference is selected
    if all(preference is None for preference in preference_selected):
        tk.messagebox.showwarning("Warning", "Please select at least one preference before submitting your votes.")
        return

    # Ask for confirmation
    confirmed = tk.messagebox.askyesno("Confirmation", "Are you sure you want to submit your votes?")
    if confirmed:
        # Placeholder function for submitting votes
        candidates = get_candidates()
        if candidates:
            for idx, candidate_options in enumerate(selected_options):
                for i, option in enumerate(candidate_options):
                    if option.get() != 0:
                        candidate_name = candidates[idx]['nicNumber']
                        cast_vote(candidate_name, i + 1)

        # Create ballot for the voter
        candidate_nic1 = candidates[preference_selected[0]]['nicNumber'] if preference_selected[0] is not None else None
        candidate_nic2 = candidates[preference_selected[1]]['nicNumber'] if preference_selected[1] is not None else None
        candidate_nic3 = candidates[preference_selected[2]]['nicNumber'] if preference_selected[2] is not None else None

        if candidate_nic1 or candidate_nic2 or candidate_nic3:
            create_ballot(candidate_nic1, candidate_nic2, candidate_nic3)

        # Update status to 'YES'
        student_id = profile.get('Id')
        if student_id:
            update_status(student_id)

        # Print the profile status after submission
        status = profile.get('status', 'Unknown')
        print(f"Profile Status: {status}")

    dashboard_window.destroy()


def cast_vote(candidate_name, preference):
    try:
        candidates_collection = db['candidates']
        candidate = candidates_collection.find_one({'nicNumber': candidate_name})

        if candidate:
            vote_field = f'vote_count_option_{preference}'
            updated_votes = candidate.get(vote_field, 0) + 1
            candidates_collection.update_one({'nicNumber': candidate_name}, {'$set': {vote_field: updated_votes}})
            print(f"Voted for candidate with NIC Number: {candidate_name}. {vote_field} updated.")
        else:
            print(f"Error: Candidate with NIC Number '{candidate_name}' not found.")
    except Exception as e:
        print(f"Error casting vote: {e}")

def create_ballot(candidate_nic1, candidate_nic2, candidate_nic3):
    try:
        ballots_collection = db['ballots']
        ballot = {
            'candidate_nic1': candidate_nic1,
            'candidate_nic2': candidate_nic2,
            'candidate_nic3': candidate_nic3
        }
        ballots_collection.insert_one(ballot)
        print(f"Ballot created with candidates: {candidate_nic1}, {candidate_nic2}, {candidate_nic3}")
    except Exception as e:
        print(f"Error creating ballot: {e}")


root = tk.Tk()
root.title("Face Recognition Login")


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\SE\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

root.geometry("500x350")
root.configure(bg = "#FFFFFF")

canvas = tk.Canvas(
    root,
    bg = "#FFFFFF",
    height = 350,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = tk.PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    250.0,
    175.0,
    image=image_image_1
)

image_image_2 = tk.PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    250.0,
    175.0,
    image=image_image_2
)

canvas.create_text(
    116.0,
    151.0,
    anchor="nw",
    text="Presidential Election 2024",
    fill="#000000",
    font=("Inter Bold", 24 * -1)
)

button_image_1 = tk.PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = tk.Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=authenticate_face,
    relief="flat"
)
button_1.place(
    x=161.0,
    y=247.0,
    width=177.0,
    height=44.0
)

root.resizable(False, False)
root.mainloop()


