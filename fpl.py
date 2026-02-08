import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import time

class FPLLiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FPL Live Points Tracker")
        self.root.geometry("500x600")
        
        # --- UI Elements ---
        # Input Frame
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Enter Team ID:").pack(side=tk.LEFT, padx=5)
        self.team_id_entry = ttk.Entry(input_frame, width=15)
        self.team_id_entry.pack(side=tk.LEFT, padx=5)
        self.track_btn = ttk.Button(input_frame, text="Start Tracking", command=self.start_tracking)
        self.track_btn.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = ttk.Label(root, text="Enter ID to start", font=("Arial", 10, "italic"))
        self.status_label.pack(pady=5)

        # Total Points Frame
        points_frame = ttk.Frame(root, padding="10")
        points_frame.pack(fill=tk.X)
        self.total_points_label = ttk.Label(points_frame, text="Live Points: --", font=("Arial", 24, "bold"))
        self.total_points_label.pack()
        
        # Player List (Treeview)
        columns = ("name", "points", "mins", "status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        self.tree.heading("name", text="Player")
        self.tree.heading("points", text="Pts")
        self.tree.heading("mins", text="Mins")
        self.tree.heading("status", text="Role")
        
        self.tree.column("name", width=180)
        self.tree.column("points", width=50, anchor="center")
        self.tree.column("mins", width=60, anchor="center")
        self.tree.column("status", width=80, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # State variables
        self.is_tracking = False
        self.team_id = None

    def start_tracking(self):
        team_id_str = self.team_id_entry.get()
        if not team_id_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Team ID")
            return
        
        self.team_id = team_id_str
        self.is_tracking = True
        self.track_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Fetching data...")
        
        # Trigger the first update immediately
        self.update_data()

    def update_data(self):
        if not self.is_tracking:
            return

        # Run API calls in a separate thread to keep GUI responsive
        threading.Thread(target=self.fetch_fpl_data, daemon=True).start()
        
        # Schedule next update in 60 seconds (60000 ms)
        self.root.after(60000, self.update_data)

    def fetch_fpl_data(self):
        try:
            # 1. Get Static Data (Player mapping & Current GW)
            static_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
            static_data = requests.get(static_url).json()
            
            # Find current gameweek
            current_event = next((e for e in static_data['events'] if e['is_current']), None)
            if not current_event:
                self.update_gui_error("No active gameweek found.")
                return
            
            gw_id = current_event['id']
            
            # Map Player ID to Name
            player_map = {p['id']: f"{p['web_name']}" for p in static_data['elements']}

            # 2. Get User Picks
            picks_url = f"https://fantasy.premierleague.com/api/entry/{self.team_id}/event/{gw_id}/picks/"
            picks_res = requests.get(picks_url)
            
            if picks_res.status_code != 200:
                self.update_gui_error(f"Error fetching team (Code {picks_res.status_code})")
                return
                
            picks_data = picks_res.json()
            picks = picks_data['picks'] # List of players in team

            # 3. Get Live Stats for Gameweek
            live_url = f"https://fantasy.premierleague.com/api/event/{gw_id}/live/"
            live_data = requests.get(live_url).json()
            
            # Convert live stats to a dictionary for fast lookup: {player_id: stats}
            live_stats = {el['id']: el['stats'] for el in live_data['elements']}

            # Calculate Points
            team_data = []
            total_gw_points = 0
            
            # Check for active chips (e.g., Bench Boost)
            active_chip = picks_data.get('active_chip')
            
            for pick in picks:
                p_id = pick['element']
                multiplier = pick['multiplier']
                is_captain = pick['is_captain']
                is_vice = pick['is_vice_captain']
                position = pick['position'] # 1-11 are main, 12-15 are bench
                
                # Get live stats
                stats = live_stats.get(p_id, {})
                raw_points = stats.get('total_points', 0)
                minutes = stats.get('minutes', 0)
                
                final_points = raw_points * multiplier
                
                # Logic for "Points to Count"
                # If multiplier > 0, it counts (Starting XI or Captain)
                # If Bench Boost is active, bench players have multiplier=1, so they count automatically
                if multiplier > 0:
                    total_gw_points += final_points

                # Role String
                role = "Bench" if multiplier == 0 else "XI"
                if is_captain: role = "Capt (x2)"
                if is_vice: role = "Vice"
                if active_chip == "bboost" and multiplier > 0 and position > 11:
                    role = "BB Active"

                player_name = player_map.get(p_id, "Unknown")
                
                team_data.append((player_name, final_points, minutes, role))

            # Update GUI on main thread
            self.root.after(0, lambda: self.refresh_tree(team_data, total_gw_points))

        except Exception as e:
            self.update_gui_error(f"Error: {str(e)}")

    def refresh_tree(self, team_data, total_points):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert new data
        for row in team_data:
            self.tree.insert("", tk.END, values=row)
            
        self.total_points_label.config(text=f"Live Points: {total_points}")
        self.status_label.config(text=f"Last Updated: {time.strftime('%H:%M:%S')}")

    def update_gui_error(self, message):
        self.root.after(0, lambda: self.status_label.config(text=message))

if __name__ == "__main__":
    root = tk.Tk()
    app = FPLLiveApp(root)
    root.mainloop()