import tkinter as tk
import requests
import threading
import time
from datetime import datetime, timezone
from io import BytesIO
from PIL import Image, ImageTk

# --- CONFIGURATION ---
API_KEY = 'YOUR_API_KEY'
COMPETITION_ID = 2021
REFRESH_RATE = 120        
ANIMATION_SPEED = 40      
SCROLL_STEP = 2           
BG_COLOR = "#202124"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#3d195b"

class GoalBubble(tk.Toplevel):
    def __init__(self, master, text, parent_x, parent_y):
        super().__init__(master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg=BG_COLOR)
        self.wm_attributes("-transparentcolor", "black") 
        self.label = tk.Label(self, text=f"⚽ {text}", bg="#fff700", fg="black", 
                              font=("Arial", 8, "bold"), padx=5, pady=2, relief="solid", borderwidth=1)
        self.label.pack()
        self.geometry(f"+{parent_x}+{parent_y}")

    def update_position(self, x, y):
        self.geometry(f"+{int(x)}+{int(y)}")

class HoverTip(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.withdraw()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg=BG_COLOR)
        self.wm_attributes("-transparentcolor", "black") 
        self.label = tk.Label(self, text="", bg="white", fg="black", 
                              font=("Arial", 8), padx=5, pady=2, relief="solid", borderwidth=1, justify="left")
        self.label.pack()

    def show(self, text, x, y):
        self.label.config(text=text)
        self.geometry(f"+{x}+{y}")
        self.deiconify()

    def hide(self):
        self.withdraw()

class SmartTicker:
    def __init__(self, root):
        self.root = root
        self.image_cache = {}
        
        self.last_scores = {}       
        self.active_alerts = {}     
        self.active_bubbles = []    
        self.current_matches = [] 
        self.match_details_cache = {} 
        self.request_timestamps = [] 

        # Store the current gameweek number
        self.current_matchday_num = None 

        self.scroll_x = 0
        self.content_width = 0
        self.running = True
        self.user_is_hovering = False 

        self.setup_window()
        self.setup_ui()
        self.hover_tip = HoverTip(self.root)

        threading.Thread(target=self.update_data_loop, daemon=True).start()
        self.animate_ticker()
        self.update_counter_ui()

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

        for btn_text, col, func in [("✕", "#ff9999", self.close_app), ("⟳", "#00ff00", self.manual_refresh), ("T", "#00ccff", self.run_test_design)]:
            lbl = tk.Label(controls, text=btn_text, bg=ACCENT_COLOR, fg=col, font=("Arial", 9, "bold"), cursor="hand2", width=3)
            lbl.pack(side=tk.LEFT, fill=tk.Y)
            lbl.bind("<Button-1>", lambda e, f=func: f())
            if btn_text == "⟳": self.btn_refresh = lbl

        self.lbl_req_count = tk.Label(controls, text="API: 0/10", bg=ACCENT_COLOR, fg="white", font=("Arial", 7))
        self.lbl_req_count.pack(side=tk.LEFT, padx=5)

        self.clip_frame = tk.Frame(self.body, bg=BG_COLOR)
        self.clip_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.clip_frame.bind("<Button-1>", self.start_move) 

        self.ticker_frame = tk.Frame(self.clip_frame, bg=BG_COLOR)
        self.ticker_frame.place(x=0, y=0, relheight=1.0)
        
        self.lbl_status = tk.Label(self.ticker_frame, text="Loading...", bg=BG_COLOR, fg="#888", font=("Arial", 8))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

    # --- API COUNTER ---
    def track_request(self):
        now = time.time()
        self.request_timestamps.append(now)
        self.update_counter_label()

    def update_counter_ui(self):
        if not self.running: return
        now = time.time()
        self.request_timestamps = [t for t in self.request_timestamps if now - t < 60]
        self.update_counter_label()
        self.root.after(1000, self.update_counter_ui)

    def update_counter_label(self):
        count = len(self.request_timestamps)
        color = "white"
        if count >= 5: color = "yellow"
        if count >= 9: color = "red"
        # Show Matchday info in label too if available
        gw_text = f" | GW{self.current_matchday_num}" if self.current_matchday_num else ""
        self.lbl_req_count.config(text=f"API: {count}/10{gw_text}", fg=color)

    # --- MOUSE ---
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        self.root.geometry(f"+{self.root.winfo_x() + (event.x - self.x)}+{self.root.winfo_y() + (event.y - self.y)}")

    def on_match_enter(self, event, match_id):
        self.user_is_hovering = True
        text = self.match_details_cache.get(match_id, "Click to fetch details")
        self.show_tooltip_at_widget(event.widget, text)

    def on_match_leave(self, event):
        self.user_is_hovering = False
        self.hover_tip.hide()

    def on_match_click(self, event, match_id, current_score_sum):
        if match_id in self.match_details_cache: del self.match_details_cache[match_id]
        self.show_tooltip_at_widget(event.widget, "Fetching goal/assist/cards...")
        threading.Thread(target=self.fetch_and_cache_details, args=(match_id, event.widget, current_score_sum), daemon=True).start()

    def fetch_and_cache_details(self, match_id, widget, score_sum):
        details = self.fetch_match_events(match_id, score_sum)
        self.match_details_cache[match_id] = details['full_history']
        if self.running:
            self.root.after(0, lambda: self.show_tooltip_at_widget(widget, details['full_history']))

    def show_tooltip_at_widget(self, widget, text):
        if not text: text = "No info"
        try:
            wx = widget.winfo_rootx()
            wy = widget.winfo_rooty()
            self.hover_tip.show(text, wx, wy - 40)
        except: pass

    # --- ANIMATION ---
    def animate_ticker(self):
        if self.running:
            if not self.user_is_hovering:
                self.scroll_x -= SCROLL_STEP
                if self.scroll_x < -self.content_width:
                    self.scroll_x = self.clip_frame.winfo_width()
                self.ticker_frame.place(x=self.scroll_x, y=0, relheight=1.0)
                self.sync_bubbles()
            self.root.after(ANIMATION_SPEED, self.animate_ticker)

    def sync_bubbles(self):
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        clip_w = self.clip_frame.winfo_width()
        ctrl_w = self.root.winfo_width() - clip_w
        for widget, bubble in self.active_bubbles:
            try:
                screen_x = root_x + ctrl_w + self.scroll_x + widget.winfo_x()
                if screen_x < root_x or screen_x > (root_x + self.root.winfo_width()):
                    bubble.withdraw()
                else:
                    bubble.deiconify()
                    bubble.update_position(screen_x + 10, root_y - 28)
            except: pass

    # --- DATA LOGIC ---
    def check_score_changes(self, matches):
        self.active_alerts = {}
        for m in matches:
            mid = m['id']
            h_s = m['score']['fullTime']['home'] or 0
            a_s = m['score']['fullTime']['away'] or 0
            curr = f"{h_s}-{a_s}"
            score_sum = h_s + a_s
            
            if mid in self.last_scores:
                if curr != self.last_scores[mid]:
                    details = self.fetch_match_events(mid, score_sum)
                    self.active_alerts[mid] = details['last_event']
                    self.match_details_cache[mid] = details['full_history']
            self.last_scores[mid] = curr

    def fetch_match_events(self, match_id, score_sum):
        self.track_request()
        url = f"https://api.football-data.org/v4/matches/{match_id}"
        headers = {'X-Auth-Token': API_KEY}
        res = {'last_event': "Goal!", 'full_history': ""}
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 429:
                res['full_history'] = "Rate Limit (Wait 60s)"
                return res
            
            data = r.json()
            goals = data.get('goals', [])
            lines = []
            last_txt = "Goal!"
            
            for g in goals:
                mn = g.get('minute', '')
                sc = "Goal"
                if g.get('scorer') and g['scorer'].get('name'):
                    sc = g['scorer']['name'].split(" ")[-1]
                ast = ""
                if g.get('assist') and g['assist'].get('name'):
                    ast = f" (a: {g['assist']['name'].split(' ')[-1]})"
                lines.append(f"⚽ {mn}' {sc}{ast}")
                last_txt = f"{sc}{ast}"
            
            bookings = data.get('bookings', [])
            for b in bookings:
                mn = b.get('minute', '')
                card = b.get('card', 'YELLOW_CARD')
                pl = "Player"
                if b.get('player') and b['player'].get('name'): pl = b['player']['name'].split(" ")[-1]
                icon = "🟨" if card == "YELLOW_CARD" else "🟥"
                lines.append(f"{icon} {mn}' {pl}")
            
            if lines:
                res['last_event'] = last_txt
                res['full_history'] = "\n".join(lines)
            else:
                if score_sum > 0: res['full_history'] = "Source delayed.\nWaiting for update..."
                else: res['full_history'] = "No events yet"
        except Exception as e:
            print(f"Err: {e}")
            res['full_history'] = "Data Error"
        return res

    def run_once(self):
        matches = self.fetch_matches()
        if self.running and matches is not None:
            self.current_matches = matches
            self.check_score_changes(matches)
            self.root.after(0, lambda: self.render_matches(matches))
            self.root.after(0, lambda: self.btn_refresh.config(fg="#00ff00"))

    def render_matches(self, matches):
        for w in self.ticker_frame.winfo_children(): w.destroy()
        for _, b in self.active_bubbles: b.destroy()
        self.active_bubbles = []

        if not matches:
            tk.Label(self.ticker_frame, text="NO MATCHES IN THIS GAMEWEEK", bg=BG_COLOR, fg="#666").pack(side=tk.LEFT, padx=10)
            self.update_ticker_width()
            return

        for m in matches:
            mid = m['id']
            cont = tk.Frame(self.ticker_frame, bg=BG_COLOR)
            cont.pack(side=tk.LEFT, padx=10, fill=tk.Y)
            
            sh = m['score']['fullTime']['home'] or 0
            sa = m['score']['fullTime']['away'] or 0
            score_sum = sh + sa

            def bind_all(w):
                w.bind("<Enter>", lambda e, i=mid: self.on_match_enter(e, i))
                w.bind("<Leave>", lambda e: self.on_match_leave(e))
                w.bind("<Button-1>", lambda e, i=mid, s=score_sum: self.on_match_click(e, i, s))

            bind_all(cont)

            min_str = self.calculate_minute(m)
            l_min = tk.Label(cont, text=min_str, bg=BG_COLOR, fg="#00ff00", font=("Arial", 7, "bold"))
            l_min.pack(side=tk.LEFT)
            bind_all(l_min)
            
            h_img = self.get_team_icon(m['homeTeam']['id'], m['homeTeam']['crest'])
            if h_img: 
                l = tk.Label(cont, image=h_img, bg=BG_COLOR)
                l.pack(side=tk.LEFT)
                bind_all(l)

            stxt = f" {m['homeTeam']['tla']} {sh}-{sa} {m['awayTeam']['tla']} "
            l_sc = tk.Label(cont, text=stxt, bg=BG_COLOR, fg=TEXT_COLOR, font=("Consolas", 9, "bold"))
            l_sc.pack(side=tk.LEFT)
            bind_all(l_sc)

            a_img = self.get_team_icon(m['awayTeam']['id'], m['awayTeam']['crest'])
            if a_img: 
                l = tk.Label(cont, image=a_img, bg=BG_COLOR)
                l.pack(side=tk.LEFT)
                bind_all(l)

            tk.Label(self.ticker_frame, text="||", bg=BG_COLOR, fg="#444").pack(side=tk.LEFT, padx=5)

            if mid in self.active_alerts:
                bubble = GoalBubble(self.root, self.active_alerts[mid], -100, -100)
                self.active_bubbles.append([l_sc, bubble])

        self.update_ticker_width()

    def update_ticker_width(self):
        self.ticker_frame.update_idletasks()
        self.content_width = self.ticker_frame.winfo_reqwidth()
        if self.content_width < 100: self.content_width = 300 

    def calculate_minute(self, match):
        try:
            s = match['status']
            if s == 'PAUSED': return "HT"
            if s == 'FINISHED': return "FT"
            if s == 'SCHEDULED': return match['utcDate'][11:16]
            if s != 'IN_PLAY': return ""
            start = datetime.fromisoformat(match['utcDate'].replace("Z", "+00:00"))
            mins = int((datetime.now(timezone.utc) - start).total_seconds() / 60)
            if mins > 45: mins = max(45, mins - 15)
            return f"{mins}'"
        except: return "LIVE"

    def get_team_icon(self, team_id, url):
        if not url: return None
        if team_id in self.image_cache: return self.image_cache[team_id]
        try:
            r = requests.get(url.replace(".svg", ".png"), timeout=1)
            if r.status_code == 200:
                im = Image.open(BytesIO(r.content)).resize((16, 16), Image.Resampling.LANCZOS)
                ph = ImageTk.PhotoImage(im)
                self.image_cache[team_id] = ph
                return ph
        except: pass
        return None

    def manual_refresh(self):
        self.btn_refresh.config(fg="yellow")
        threading.Thread(target=self.run_once, daemon=True).start()

    def run_test_design(self):
        fake_id = 999999
        fake_match = {
            'id': fake_id, 'status': 'IN_PLAY', 'utcDate': datetime.now(timezone.utc).isoformat(),
            'homeTeam': {'id': 0, 'tla': 'TEST', 'crest': ''},
            'awayTeam': {'id': 0, 'tla': 'DSGN', 'crest': ''},
            'score': {'fullTime': {'home': 5, 'away': 5}}
        }
        self.active_alerts[fake_id] = "TestGoal"
        self.match_details_cache[fake_id] = "⚽ 12' Scorer (a: Asst)\n🟨 45' Player"
        self.render_matches([fake_match] + self.current_matches)

    # --- UPDATED FETCH LOGIC FOR CURRENT GAMEWEEK ---
    def fetch_current_gameweek(self):
        """Ask API what the current matchday is."""
        self.track_request()
        url = f"https://api.football-data.org/v4/competitions/{COMPETITION_ID}"
        headers = {'X-Auth-Token': API_KEY}
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return r.json()['currentSeason']['currentMatchday']
        except: pass
        return None

    def fetch_matches(self):
        # 1. Get current matchday if we don't have it yet (or refresh occasionally)
        if self.current_matchday_num is None:
            self.current_matchday_num = self.fetch_current_gameweek()
            
        if not self.current_matchday_num:
            return None

        # 2. Fetch ALL matches for this specific Gameweek (Matchday)
        self.track_request()
        url = f"https://api.football-data.org/v4/competitions/{COMPETITION_ID}/matches"
        headers = {'X-Auth-Token': API_KEY}
        params = {'matchday': self.current_matchday_num}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            if r.status_code == 200:
                return r.json().get('matches', [])
        except: pass
        return None

    def update_data_loop(self):
        while self.running:
            self.run_once()
            time.sleep(REFRESH_RATE)

    def close_app(self):
        self.running = False
        self.hover_tip.destroy()
        for _, b in self.active_bubbles: b.destroy()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartTicker(root)
    root.mainloop()