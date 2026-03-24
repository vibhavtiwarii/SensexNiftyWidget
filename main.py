import sys, requests, ctypes, datetime
from PySide6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QIcon

STOCKS = {
    "NIFTY": "^NSEI",
    "SENSEX": "^BSESN"
}

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        # ---------- WINDOW ----------
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(360, 280)

        # ---------- DATA ----------
        self.data = {k: [] for k in STOCKS}
        self.display_data = {k: [] for k in STOCKS}

        # ---------- LIVE STATE ----------
        self.prev_price = {}
        self.flash = {}
        self.pulse = 0

        # ---------- INTERACTION ----------
        self.zoom = 1.0
        self.offset = 0
        self.hover_pos = None
        self.drag = None
        self.is_panning = False

        self.setMouseTracking(True)

        # ---------- UI ----------
        self.init_tray()

        # ---------- TIMERS ----------
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update)
        self.anim_timer.start(33)

        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_all)
        self.timer.start(10000)  # 🔥 10 seconds

        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.animate_pulse)
        self.pulse_timer.start(100)

        self.fetch_all()

        self.show()
        self.snap_to_corner()

    # ---------- TRAY ----------
    def init_tray(self):
        self.tray = QSystemTrayIcon(QIcon(), self)
        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addAction("Hide", self.hide)
        menu.addSeparator()
        menu.addAction("Exit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.show()

    # ---------- PULSE ----------
    def animate_pulse(self):
        self.pulse = (self.pulse + 1) % 20
        self.update()

    # ---------- POSITION ----------
    def snap_to_corner(self):
        screen = QApplication.primaryScreen().geometry()
        margin = 10
        self.move(screen.width() - self.width() - margin, margin)

    # ---------- DATA ----------
    def fetch(self, ticker):
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5).json()

            result = res['chart']['result'][0]
            q = result['indicators']['quote'][0]
            timestamps = result['timestamp']

            candles = []
            for t, o, h, l, c in zip(timestamps, q['open'], q['high'], q['low'], q['close']):
                if o and h and l and c:
                    candles.append((t, o, h, l, c))

            return candles[-100:]
        except:
            return []

    def fetch_all(self):
        for name, ticker in STOCKS.items():
            new = self.fetch(ticker)

            if new:
                self.data[name] = new

                if not self.display_data[name]:
                    self.display_data[name] = new
                else:
                    for i in range(min(len(new), len(self.display_data[name]))):
                        t,o,h,l,c = self.display_data[name][i]
                        nt,no,nh,nl,nc = new[i]
                        self.display_data[name][i] = (
                            nt,
                            o + (no-o)*0.05,
                            h + (nh-h)*0.05,
                            l + (nl-l)*0.05,
                            c + (nc-c)*0.05
                        )

                # 🔥 detect price change
                last_price = new[-1][4]

                if name in self.prev_price:
                    if last_price > self.prev_price[name]:
                        self.flash[name] = "up"
                    elif last_price < self.prev_price[name]:
                        self.flash[name] = "down"
                    else:
                        self.flash[name] = None
                else:
                    self.flash[name] = None

                self.prev_price[name] = last_price

    # ---------- DRAW ----------
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # 🔥 FIX BLUE EDGE
        rect = self.rect().adjusted(1,1,-1,-1)
        p.setBrush(QColor(20,20,30,220))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(rect, 20, 20)

        # 🔥 LIVE DOT
        radius = 4 + (self.pulse % 4)
        p.setBrush(QColor(0,255,120))
        p.drawEllipse(self.width()-20, 10, radius, radius)

        y_offset = 30

        for name, candles in self.display_data.items():
            if not candles:
                continue

            closes = [c[4] for c in candles]
            min_p, max_p = min(closes), max(closes)

            w = self.width() - 20
            h = 90

            last = closes[-1]
            first = closes[0]
            pct = (last-first)/first*100
            base_color = QColor(0,255,120) if pct>=0 else QColor(255,80,80)

            flash = self.flash.get(name)

            # TEXT
            p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
            p.setPen(QColor(220,220,220))
            p.drawText(12, y_offset, name)

            # FLASH COLOR
            if flash == "up":
                p.setPen(QColor(0,255,120))
            elif flash == "down":
                p.setPen(QColor(255,80,80))
            else:
                p.setPen(base_color)

            p.setFont(QFont("Segoe UI", 11, QFont.Bold))
            p.drawText(220, y_offset, f"{last:.2f}")

            # % TEXT
            p.setFont(QFont("Segoe UI", 8))
            p.setPen(QColor(180,180,180))
            p.drawText(220, y_offset+15, f"{pct:+.2f}%")

            # GLOW LINE
            if flash == "up":
                p.setPen(QPen(QColor(0,255,120,120),2))
                p.drawLine(200, y_offset+5, 270, y_offset+5)
            elif flash == "down":
                p.setPen(QPen(QColor(255,80,80,120),2))
                p.drawLine(200, y_offset+5, 270, y_offset+5)

            # GRID
            p.setPen(QPen(QColor(255,255,255,20),1))
            for i in range(4):
                y = y_offset + i*(h//4)
                p.drawLine(10, y, 10+w, y)

            # CANDLES
            bar_w = max(2, int(w/len(candles))-1)

            def nx(i): return 10 + int(i*w/len(candles))
            def ny(val): return y_offset+10 + int(h - (val-min_p)/(max_p-min_p+1e-6)*h)

            for i,(t,o,hg,lg,c) in enumerate(candles):
                x = nx(i)
                col = QColor(0,255,120) if c>=o else QColor(255,80,80)

                p.setPen(QPen(col,1))
                p.drawLine(x, ny(hg), x, ny(lg))

                p.setPen(QPen(col, bar_w))
                p.drawLine(x, ny(o), x, ny(c))

            y_offset += 120


# ---------- RUN ----------
app = QApplication(sys.argv)
w = Widget()
sys.exit(app.exec())
