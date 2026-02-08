import tkinter as tk
import requests
import threading
import time
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk

# --- CONFIGURATION ---
ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
# ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard"
REFRESH_RATE = 60         
ANIMATION_SPEED = 40      
SCROLL_STEP = 2
ALERT_DURATION = 60       # Notification stays for 60 seconds
BG_COLOR = "#202124"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#3d195b"

class GoalBubble(tk.Toplevel):
    """Yellow popup for goals."""
    def __init__(self, master, text, parent_x, parent_y):
        super().__init__(master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg=BG_COLOR)
        self.wm_attributes("-transparentcolor", "black") 
        
        self.label = tk.Label(
            self, 
            text=f"⚽ {text}", 
            bg="#fff700", fg="black", 
            font=("Arial", 8, "bold"),
            padx=5, pady=2, relief="solid", borderwidth=1
        )
        self.label.pack()
        self.update_idletasks()
        h = self.label.winfo_reqheight()
        self.geometry(f"+{parent_x}+{parent_y - h - 5}")

    def update_position(self, x, y):
        h = self.label.winfo_reqheight()
        self.geometry(f"+{int(x)}+{int(y - h - 5)}")

class HoverTip(tk.Toplevel):
    """Rich History Tooltip."""
    def __init__(self, master):
        super().__init__(master)
        self.withdraw()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg=BG_COLOR)
        self.container = tk.Frame(self, bg=BG_COLOR, highlightthickness=1, highlightbackground="#555")
        self.container.pack(fill=tk.BOTH, expand=True)

    def show(self, events_data, widget_x, widget_y):
        for w in self.container.winfo_children(): w.destroy()
        if not events_data:
            tk.Label(self.container, text="No events yet", bg=BG_COLOR, fg="#888", font=("Arial", 8)).pack(padx=5, pady=2)
        else:
            for ev in events_data:
                row = tk.Frame(self.container, bg=BG_COLOR)
                row.pack(fill=tk.X, padx=5, pady=1)
                tk.Label(row, text=ev['time'], bg=BG_COLOR, fg="#00ff00", font=("Consolas", 8, "bold"), width=4, anchor="w").pack(side=tk.LEFT)
                if ev['type'] == 'goal':
                    tk.Label(row, text="⚽", bg=BG_COLOR, fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=(0, 4))
                elif ev['type'] == 'yellow':
                    tk.Frame(row, width=8, height=10, bg="#ffcc00").pack(side=tk.LEFT, padx=(0, 4))
                elif ev['type'] == 'red':
                    tk.Frame(row, width=8, height=10, bg="#ff3333").pack(side=tk.LEFT, padx=(0, 4))
                tk.Label(row, text=ev['player'], bg=BG_COLOR, fg="white", font=("Arial", 8, "bold")).pack(side=tk.LEFT)
                if ev.get('assist'):
                    tk.Frame(row, width=8, bg=BG_COLOR).pack(side=tk.LEFT)
                    tk.Label(row, text="🅰", bg=BG_COLOR, fg="#00ccff", font=("Arial", 7, "bold")).pack(side=tk.LEFT)
                    tk.Label(row, text=ev['assist'], bg=BG_COLOR, fg="#cccccc", font=("Arial", 7)).pack(side=tk.LEFT)

        self.update_idletasks()
        tip_h = self.container.winfo_reqheight()
        pos_x = widget_x
        pos_y = widget_y - tip_h - 10
        self.geometry(f"+{pos_x}+{pos_y}")
        self.deiconify()

    def hide(self):
        self.withdraw()

class SmartTicker:
    def __init__(self, root):
        self.root = root
        self.image_cache = {}
        self.last_scores = {}       
        self.match_details_cache = {} 
        self.current_matches = [] 

        # --- LOGIC UPDATES ---
        # active_alerts format: { match_id: {'text': "Goal!", 'expires': timestamp} }
        self.active_alerts = {}     
        # active_bubbles format: [ [match_id, container_widget, bubble_window], ... ]
        self.active_bubbles = []    

        self.scroll_x = 0
        self.content_width = 0
        self.running = True
        self.user_is_hovering = False 

        self.setup_window()
        self.setup_ui()
        self.hover_tip = HoverTip(self.root)

        threading.Thread(target=self.update_data_loop, daemon=True).start()
        self.animate_ticker()

    def setup_window(self):
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg=BG_COLOR)
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"700x35+{int(screen_width/2)-350}+200")
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.body = tk.Frame(self.root, bg=BG_COLOR, highlightthickness=1, highlightbackground=ACCENT_COLOR)
        self.body.pack(fill=tk.BOTH, expand=True)

    def setup_ui(self):
        controls = tk.Frame(self.body, bg=ACCENT_COLOR, height=35)
        controls.pack(side=tk.LEFT, fill=tk.Y)
        controls.bind("<Button-1>", self.start_move)
        controls.bind("<B1-Motion>", self.do_move)

        for btn_text, col, func in [("✕", "#ff9999", self.close_app), ("⟳", "#00ff00", self.manual_refresh), ("T", "#00ccff", self.run_test_notification)]:
            lbl = tk.Label(controls, text=btn_text, bg=ACCENT_COLOR, fg=col, font=("Arial", 9, "bold"), cursor="hand2", width=3)
            lbl.pack(side=tk.LEFT, fill=tk.Y)
            lbl.bind("<Button-1>", lambda e, f=func: f())
            if btn_text == "⟳": self.btn_refresh = lbl

        self.clip_frame = tk.Frame(self.body, bg=BG_COLOR)
        self.clip_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.clip_frame.bind("<Button-1>", self.start_move) 

        self.ticker_frame = tk.Frame(self.clip_frame, bg=BG_COLOR)
        self.ticker_frame.place(x=0, y=0, relheight=1.0)
        
        self.lbl_status = tk.Label(self.ticker_frame, text="Connecting...", bg=BG_COLOR, fg="#888", font=("Arial", 8))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        self.root.geometry(f"+{self.root.winfo_x() + (event.x - self.x)}+{self.root.winfo_y() + (event.y - self.y)}")

    # --- HOVER LOGIC ---
    def on_match_enter(self, event, match_id):
        self.user_is_hovering = True
        events_data = self.match_details_cache.get(match_id, [])
        widget = event.widget
        wx = widget.winfo_rootx()
        wy = widget.winfo_rooty()
        self.hover_tip.show(events_data, wx, wy)

    def on_match_leave(self, event):
        self.user_is_hovering = False
        self.hover_tip.hide()

    def on_match_click(self, event, match_id):
        threading.Thread(target=self.run_once, daemon=True).start()

    # --- ANIMATION & TIME MANAGEMENT ---
    def animate_ticker(self):
        if self.running:
            if not self.user_is_hovering:
                self.scroll_x -= SCROLL_STEP
                if self.scroll_x < -self.content_width:
                    self.scroll_x = self.clip_frame.winfo_width()
                    # REMOVED: self.clear_all_bubbles() 
                    # Reason: We now rely on time, not rotation.
                    
                self.ticker_frame.place(x=self.scroll_x, y=0, relheight=1.0)
                self.check_expired_alerts() # Check for 60s timeout
                self.sync_bubbles()
            self.root.after(ANIMATION_SPEED, self.animate_ticker)

    def check_expired_alerts(self):
        """Checks if any alert has passed its 60s lifespan."""
        now = time.time()
        
        # 1. Identify expired IDs
        expired_ids = [mid for mid, data in self.active_alerts.items() if now > data['expires']]
        
        # 2. Remove from logic dict
        for mid in expired_ids:
            del self.active_alerts[mid]

        # 3. Visually destroy expired bubbles immediately
        # Filter active_bubbles list: Keep only those whose Match ID is still in active_alerts
        # If match ID is NOT in active_alerts, destroy the window
        new_active_bubbles = []
        for mid, cont, win in self.active_bubbles:
            if mid in self.active_alerts:
                new_active_bubbles.append([mid, cont, win])
            else:
                win.destroy() # Poof!
        
        self.active_bubbles = new_active_bubbles

    def sync_bubbles(self):
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        clip_w = self.clip_frame.winfo_width()
        ctrl_w = self.root.winfo_width() - clip_w
        
        for mid, widget, bubble in self.active_bubbles:
            try:
                widget_x = widget.winfo_x()
                screen_x = root_x + ctrl_w + self.scroll_x + widget_x
                
                # Only show if inside window bounds
                if screen_x < root_x or screen_x > (root_x + self.root.winfo_width()):
                    bubble.withdraw()
                else:
                    bubble.deiconify()
                    bubble.update_position(screen_x + 40, root_y)
            except: pass

    # --- PARSERS ---
    def get_player_name_from_detail(self, detail):
        if 'athletesInvolved' in detail and detail['athletesInvolved']:
            return detail['athletesInvolved'][0].get('shortName', detail['athletesInvolved'][0].get('displayName', "Unknown"))
        if 'participants' in detail and detail['participants']:
            return detail['participants'][0]['athlete'].get('shortName', "Unknown")
        if 'text' in detail:
            return detail['text'].replace("Goal - ", "").replace("Yellow Card - ", "").replace("Red Card - ", "").split(" ")[-1]
        return "Unknown"

    def get_assist_from_detail(self, detail):
        if 'athletesInvolved' in detail and len(detail['athletesInvolved']) > 1:
            return detail['athletesInvolved'][1].get('shortName', "")
        if 'participants' in detail and len(detail['participants']) > 1:
            return detail['participants'][1]['athlete'].get('shortName', "")
        return None

    def parse_espn_match(self, event):
        try:
            mid = event['id']
            status = event['status']
            state = status['type']['state']
            time_str = status['type']['shortDetail'] if state == 'in' else ("FT" if state == 'post' else datetime.strptime(event['date'], "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M"))
            
            competitors = event['competitions'][0]['competitors']
            home = next(c for c in competitors if c['homeAway'] == 'home')
            away = next(c for c in competitors if c['homeAway'] == 'away')
            h_score = int(home.get('score', 0))
            a_score = int(away.get('score', 0))

            events_list = []
            last_goal_text = ""
            
            if 'details' in event['competitions'][0]:
                for d in event['competitions'][0]['details']:
                    clock = d.get('clock', {}).get('displayValue', '')
                    type_txt = d.get('type', {}).get('text', '') 
                    player_short = self.get_player_name_from_detail(d)
                    evt = {'time': clock, 'player': player_short, 'assist': None, 'type': 'other'}
                    
                    if "Goal" in type_txt: 
                        evt['type'] = 'goal'
                        assist = self.get_assist_from_detail(d)
                        if assist: evt['assist'] = assist
                        if "Own Goal" in type_txt: evt['player'] += " (OG)"
                        if "Penalty" in type_txt: evt['player'] += " (P)"
                        
                        assist_str = f" (a: {assist})" if assist else ""
                        last_goal_text = f"{evt['player']}{assist_str}"
                        events_list.append(evt)
                    elif "Card" in type_txt:
                        evt['type'] = 'red' if "Red" in type_txt else 'yellow'
                        events_list.append(evt)

            return {
                'id': mid, 'time': time_str,
                'home': {'tla': home['team']['abbreviation'], 'logo': home['team']['logo'], 'score': h_score},
                'away': {'tla': away['team']['abbreviation'], 'logo': away['team']['logo'], 'score': a_score},
                'history_list': events_list, 'last_event': last_goal_text
            }
        except: return None

    def run_once(self):
        try:
            r = requests.get(ESPN_URL)
            events = r.json().get('events', [])
            parsed_matches = []
            
            for e in events:
                m = self.parse_espn_match(e)
                if m:
                    parsed_matches.append(m)
                    mid = m['id']
                    curr_score = f"{m['home']['score']}-{m['away']['score']}"
                    self.match_details_cache[mid] = m['history_list']

                    # --- NEW ALERT LOGIC ---
                    if mid in self.last_scores:
                        if curr_score != self.last_scores[mid]:
                            if m['last_event']:
                                # STORE WITH EXPIRY TIME
                                self.active_alerts[mid] = {
                                    'text': m['last_event'],
                                    'expires': time.time() + ALERT_DURATION
                                }
                    
                    self.last_scores[mid] = curr_score

            self.current_matches = parsed_matches # Update stored list for test btn
            self.root.after(0, lambda: self.render_matches(parsed_matches))
            self.root.after(0, lambda: self.btn_refresh.config(fg="#00ff00"))
        except: pass

    def render_matches(self, matches):
        # 1. Clear Widgets
        for w in self.ticker_frame.winfo_children(): w.destroy()
        
        # 2. Clear Bubble Visuals (Logic persists in active_alerts)
        for _, _, b in self.active_bubbles: b.destroy()
        self.active_bubbles = []

        if not matches:
            tk.Label(self.ticker_frame, text="NO MATCHES TODAY", bg=BG_COLOR, fg="#666").pack(side=tk.LEFT, padx=10)
            self.update_ticker_width()
            return

        for m in matches:
            mid = m['id']
            cont = tk.Frame(self.ticker_frame, bg=BG_COLOR)
            cont.pack(side=tk.LEFT, padx=10, fill=tk.Y)
            
            def bind_all(w):
                w.bind("<Enter>", lambda e, i=mid: self.on_match_enter(e, i))
                w.bind("<Leave>", lambda e: self.on_match_leave(e))
                w.bind("<Button-1>", lambda e, i=mid: self.on_match_click(e, i))

            bind_all(cont)
            tk.Label(cont, text=m['time'], bg=BG_COLOR, fg="#00ff00", font=("Arial", 7, "bold")).pack(side=tk.LEFT)
            h_img = self.get_team_icon(m['home']['tla'], m['home']['logo'])
            if h_img: tk.Label(cont, image=h_img, bg=BG_COLOR).pack(side=tk.LEFT)
            stxt = f" {m['home']['tla']} {m['home']['score']}-{m['away']['score']} {m['away']['tla']} "
            tk.Label(cont, text=stxt, bg=BG_COLOR, fg=TEXT_COLOR, font=("Consolas", 9, "bold")).pack(side=tk.LEFT)
            a_img = self.get_team_icon(m['away']['tla'], m['away']['logo'])
            if a_img: tk.Label(cont, image=a_img, bg=BG_COLOR).pack(side=tk.LEFT)
            tk.Label(self.ticker_frame, text="||", bg=BG_COLOR, fg="#444").pack(side=tk.LEFT, padx=5)

            # --- CREATE BUBBLE ONLY IF TIME HAS NOT EXPIRED ---
            if mid in self.active_alerts:
                alert_data = self.active_alerts[mid]
                # Double check time (safety)
                if time.time() < alert_data['expires']:
                    bubble = GoalBubble(self.root, alert_data['text'], -100, -100)
                    self.active_bubbles.append([mid, cont, bubble])

        self.update_ticker_width()

    def update_ticker_width(self):
        self.ticker_frame.update_idletasks()
        self.content_width = self.ticker_frame.winfo_reqwidth()
        if self.content_width < 100: self.content_width = 300 

    def get_team_icon(self, tla, url):
        if not url: return None
        if tla in self.image_cache: return self.image_cache[tla]
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                im = Image.open(BytesIO(r.content)).resize((16, 16), Image.Resampling.LANCZOS)
                ph = ImageTk.PhotoImage(im)
                self.image_cache[tla] = ph
                return ph
        except: pass
        return None

    def manual_refresh(self):
        self.btn_refresh.config(fg="yellow")
        threading.Thread(target=self.run_once, daemon=True).start()

    def run_test_notification(self):
        target_match = None
        # Try to find a real match first
        if self.current_matches:
            target_match = self.current_matches[0]
        else:
            # Fallback
            target_match = {'id': '999', 'time': "88'", 'home': {'tla': 'TES', 'logo': '', 'score': 2}, 'away': {'tla': 'DSG', 'logo': '', 'score': 1}, 'history_list': [], 'last_event': ""}
            self.render_matches([target_match])

        if target_match:
            mid = target_match['id']
            # SET EXPIRY TO NOW + 60s
            self.active_alerts[mid] = {
                'text': "TEST GOAL! (90')",
                'expires': time.time() + ALERT_DURATION
            }
            # Re-render to show the bubble immediately
            if self.current_matches:
                self.render_matches(self.current_matches)
            else:
                self.render_matches([target_match])

    def update_data_loop(self):
        while self.running:
            self.run_once()
            time.sleep(REFRESH_RATE)

    def close_app(self):
        self.running = False
        self.hover_tip.destroy()
        for _, _, b in self.active_bubbles: b.destroy()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartTicker(root)
    root.mainloop()