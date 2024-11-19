import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import pymongo
from PIL import Image, ImageTk
from pathlib import Path
import tkinter.messagebox
import datetime


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

            if 50 < conf < 100:
                profile = get_profile(student_id)
                print("Confidence:",conf)
                if profile:
                    if profile.get('status', '') == 'YES':
                        tkinter.messagebox.showinfo("Information", "You have already voted.")
                        return
                    name = profile.get('Name', 'Unknown')
                    id = profile.get('Id', 'Unknown')
                    age = profile.get('age', 'Unknown')
                    object_id = profile.get('_id', 'Unknown')
                    district = profile.get('district', 'Unknown')  # Fetch district
                    status = profile.get('status', 'Unknown')

                    print(f"Detected Profile - Name: {name}, ID: {student_id}, Age: {age}, ObjectID: {object_id}, District: {district}, Status: {status}")

                    # Release camera and destroy OpenCV window
                    cam.release()
                    cv2.destroyAllWindows()

                    # Open new dashboard window
                    show_dashboard(name, age, profile, district,id)
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



def get_parties():
    try:
        collection = db['parties']
        parties = list(collection.find({}))
        return parties
    except Exception as e:
        print(f"Error fetching parties: {e}")
        return []

def get_candidates_by_party(party_name, voter_district):
    try:
        collection = db['candidates']
        candidates = list(collection.find({
            'partyname': party_name,
            'district': voter_district,
            'ElectionName': 'Parliament'
        }))
        return candidates
    except Exception as e:
        print(f"Error fetching candidates: {e}")
        return []

def show_candidates_window(party_name, district,  dashboard_window,profile):
    candidates = get_candidates_by_party(party_name, district)
    if not candidates:
        messagebox.showerror("Error",
                             f"No candidates found for the party '{party_name}' in your district '{district}'.")
        return

    candidates_window = tk.Toplevel()
    candidates_window.title(f"Candidates for {party_name}")
    candidates_window.geometry("1366x720")

    style = ttk.Style()
    style.configure('Candidates.TLabel', font=('Helvetica', 12), padding=10)

    candidates_label = ttk.Label(candidates_window, text=f"Candidates for {party_name}", style='Candidates.TLabel')
    candidates_label.pack(padx=10)

    selected_options = [tk.IntVar(value=0) for _ in range(len(candidates))]
    max_selections = 3
    min_selections = 1

    def on_checkbox_change(var, current_candidate_index, selected_options):
        if var.get() == 1:
            selected_count = sum(option.get() == 1 for option in selected_options)
            if selected_count > max_selections:
                messagebox.showwarning("Selection Limit", f"You can select a maximum of {max_selections} candidates.")
                var.set(0)
        elif var.get() == 0:
            selected_count = sum(option.get() == 1 for option in selected_options)
            if selected_count < min_selections:
                messagebox.showwarning("Selection Limit", f"You must select at least {min_selections} candidate(s).")
                var.set(1)

    for idx, candidate in enumerate(candidates):
        candidate_name = candidate.get('Cname', 'Unknown')
        Number = candidate.get('Number', 'Unknown')

        candidate_frame = ttk.Frame(candidates_window)
        candidate_frame.pack(pady=10, padx=10, fill='x')

        candidate_info_label = ttk.Label(candidate_frame, text=f" {candidate_name} ", style='Candidates.TLabel')
        candidate_info_label.pack(side='left', padx=10)

        candidate_num_label = ttk.Label(candidate_frame, text=f"{Number}", style='Candidates.TLabel')
        candidate_num_label.place(x=300)

        checkbox = ttk.Checkbutton(candidate_frame, text="Select", variable=selected_options[idx], onvalue=1,offvalue=0,command=lambda var=selected_options[idx], idx=idx: on_checkbox_change(var, idx,selected_options))
        checkbox.place(x=500)

    def submit_selections(profile):
        confirmed = messagebox.askyesno("Confirm Submission", "Are you sure you want to submit your vote?")
        if confirmed:
            selected_candidates = [candidates[idx] for idx, var in enumerate(selected_options) if var.get() == 1]

            if selected_candidates:
                try:
                    # Increment the vote count for each selected candidate
                    for candidate in selected_candidates:
                        candidate_id = candidate['_id']
                        db['candidates'].update_one({'_id': candidate_id}, {'$inc': {'vote_count_option_1': 1}})

                    # Update the vote count for the party
                    party_id = get_parties()[0]['_id']  # Assuming you only vote for one party at a time
                    db['parties'].update_one({'_id': party_id}, {'$inc': {'votes': 1}})

                    # Update the profile status
                    profile['status'] = 'YES'
                    collection.update_one({'_id': profile['_id']}, {'$set': {'status': 'YES'}})

                    # Create the ballot
                    candidate_nics = [candidate['nicNumber'] for candidate in selected_candidates]
                    if len(candidate_nics) == 1:
                        create_ballot(party_name, candidate_nics[0], None, None)
                    elif len(candidate_nics) == 2:
                        create_ballot(party_name, candidate_nics[0], candidate_nics[1], None)
                    elif len(candidate_nics) == 3:
                        create_ballot(party_name, candidate_nics[0], candidate_nics[1], candidate_nics[2])


                    messagebox.showinfo("Success", "Votes submitted successfully!")
                    candidates_window.destroy()
                    if dashboard_window:
                        dashboard_window.destroy()


                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update vote counts: {e}")
            else:
                messagebox.showwarning("Warning", "No candidates selected.")

    def reset_votes(selected_options):
        for var in selected_options:
            var.set(0)

    reset_button = ttk.Button(candidates_window, text="Reset Votes", command=lambda: reset_votes(selected_options))
    reset_button.pack(pady=10)

    submit_button = ttk.Button(candidates_window, text="Submit", command=lambda:submit_selections(profile))
    submit_button.pack(pady=10)


def show_dashboard(name, age, profile, district,id):
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("1366x720")

    image_path = r"D:\SE\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0\GUIBG2.jpg"
    image = Image.open(image_path)
    resized_image = image.resize((1366, 768), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(dashboard_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    style = ttk.Style()
    style.configure('Dashboard.TLabel', font=('Helvetica', 14), padding=10)

    # welcome_label = ttk.Label(dashboard_window, text=f"Welcome, {name}!", style='Dashboard.TLabel')
    # welcome_label.pack()

    profile_label = ttk.Label(dashboard_window, text=f"Profile Details:\nName: {name}\nNIC: {id}", style='Dashboard.TLabel')
    profile_label.pack(pady=10)

    canvas = tk.Canvas(dashboard_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(dashboard_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    parties = get_parties()
    if not parties:
        messagebox.showerror("Error", "Unable to fetch parties.")
        return

    selected_options = [tk.IntVar(value=0) for _ in range(len(parties))]
    view_candidate_buttons = []

    def on_checkbox_change(var, current_idx, selected_options):
        if var.get() == 1:
            for idx, option in enumerate(selected_options):
                if idx != current_idx:
                    option.set(0)
            for idx, button in enumerate(view_candidate_buttons):
                if idx == current_idx:
                    button.config(state='normal')
                else:
                    button.config(state='disabled')
        else:
            for button in view_candidate_buttons:
                button.config(state='disabled')

    if parties and len(parties) > 0:
        parties_label = ttk.Label(frame, text="List of parties", style='Dashboard.TLabel')
        parties_label.pack(pady=20)

        for idx, party in enumerate(parties):
            party_name = party.get('party_name', 'Unknown')
            logo_path = party.get('logo', '')

            party_frame = ttk.Frame(frame)
            party_frame.pack(pady=10, padx=10, fill='x')

            if logo_path:
                try:
                    logo_image = Image.open(f"E:/SE/SE_dashboard/uploads/{logo_path}")
                    resized_logo_image = logo_image.resize((100, 100), Image.LANCZOS)
                    party_logo = ImageTk.PhotoImage(resized_logo_image)
                    logo_label = tk.Label(party_frame, image=party_logo)
                    logo_label.image = party_logo
                    logo_label.pack(side='left', padx=10)
                except Exception as e:
                    print(f"Error loading logo: {e}")

            party_info_label = ttk.Label(party_frame, text=f"Party Name: {party_name}", style='Dashboard.TLabel')
            party_info_label.pack(side='left', padx=10)

            checkbox = ttk.Checkbutton(party_frame, text="Vote", variable=selected_options[idx], onvalue=1, offvalue=0, command=lambda var=selected_options[idx], idx=idx: on_checkbox_change(var, idx, selected_options))
            checkbox.pack(side='left', padx=5)

            view_candidates_button = ttk.Button(party_frame, text="View Candidates", command=lambda party_name=party_name: show_candidates_window(party_name, district, dashboard_window,profile), state='disabled')

            view_candidates_button.pack(side='left', padx=5)
            view_candidate_buttons.append(view_candidates_button)

    else:
        no_parties_label = ttk.Label(frame, text="No parties found.", style='Dashboard.TLabel')
        no_parties_label.pack(pady=10)

    reset_button = ttk.Button(frame, text="Reset Votes", command=lambda: reset_votes(selected_options, view_candidate_buttons))
    reset_button.pack(pady=10)

    submit_button = ttk.Button(frame, text="Submit", command=lambda: submit_votes(selected_options, profile, dashboard_window, parties))
    submit_button.pack(pady=20)
def reset_votes(selected_options, view_candidate_buttons):
    for var in selected_options:
        var.set(0)
    for button in view_candidate_buttons:
        button.config(state='disabled')

def submit_votes(selected_options, profile, dashboard_window, parties):
    selected_party_index = None
    for idx, option in enumerate(selected_options):
        if option.get() == 1:
            selected_party_index = idx
            break

    if selected_party_index is None:
        tk.messagebox.showwarning("Warning", "Please select exactly one party before submitting your vote.")
        return

    confirmed = tk.messagebox.askyesno("Confirm Submission", "Are you sure you want to submit your vote?")
    if confirmed:
        selected_party = parties[selected_party_index]
        party_id = selected_party['_id']

        try:
            result = db['parties'].update_one({'_id': party_id}, {'$inc': {'votes': 1}})

            if result.modified_count == 1:
                profile['status'] = 'YES'
                collection.update_one({'_id': profile['_id']}, {'$set': {'status': 'YES'}})

                create_ballot(selected_party['party_name'], None, None, None)
                tk.messagebox.showinfo("Success", "Vote submitted successfully!")
                dashboard_window.destroy()
            else:
                tk.messagebox.showerror("Error", "Failed to update the vote count.")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to submit vote: {e}")


def create_ballot(party_name,candidate_nic1, candidate_nic2, candidate_nic3):
    try:
        ballots_collection = db['ballotsP']
        ballot = {
            'party': party_name,
            'candidate_nic1': candidate_nic1,
            'candidate_nic2': candidate_nic2,
            'candidate_nic3': candidate_nic3,
             'created_at': datetime.datetime.utcnow()   # Assuming UTC time is desired
        }
        ballots_collection.insert_one(ballot)
        print(f"Ballot created with candidates: {candidate_nic1}, {candidate_nic2}, {candidate_nic3}")
    except Exception as e:
        print(f"Error creating ballot: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Face Recognition Login")

    # Center the window on the screen
    # Custom GUI setup using Tkinter-Designer assets
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\SE\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    root.geometry("500x350")
    root.configure(bg="#FFFFFF")

    canvas = tk.Canvas(
        root,
        bg="#FFFFFF",
        height=350,
        width=500,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = tk.PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_1 = canvas.create_image(
        250.0,
        175.0,
        image=image_image_1
    )

    image_image_2 = tk.PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_2 = canvas.create_image(
        250.0,
        175.0,
        image=image_image_2
    )

    canvas.create_text(
        116.0,
        151.0,
        anchor="nw",
        text="Parliament Election 2024",
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
