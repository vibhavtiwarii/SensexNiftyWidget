📊 Sensex Nifty Widget

A lightweight desktop stock widget for Windows that displays live charts for NIFTY and SENSEX directly on your desktop.

Built using Python + PySide6 (Qt) with custom rendering for a smooth, modern UI.

🚀 Features
📈 Real-time-like stock charts (NIFTY & SENSEX)
🕒 Auto-refresh every 10 seconds
🎯 Candlestick chart rendering (custom-built, no heavy libraries)
🖱️ Interactive UI:
Zoom (mouse wheel)
Pan (drag)
Crosshair + OHLC tooltip
🟢 Live status indicator (pulse animation)
🔴🟢 Price change highlighting
🪟 Frameless desktop widget (stays behind apps)
🔔 System tray integration (show / hide / exit)
🧠 Tech Stack
Python
PySide6 (Qt) – GUI framework
QPainter – custom graphics rendering
Requests – API calls
PyInstaller – executable packaging
Inno Setup – Windows installer
📦 Installation
Option 1 — Use Installer (Recommended)
Download from Releases:
👉 (add your GitHub release link here)
Run:
SensexNiftyWidgetSetup.exe
Install and launch
Option 2 — Run from Source
pip install PySide6 requests
python main.py
🖥️ Usage
The widget appears on your desktop (top-right corner)
Runs in background via system tray
Right-click tray icon to:
Show / Hide
Exit
⚠️ Data Disclaimer
Data is fetched from Yahoo Finance (unofficial API)
Prices are:
✅ Real market data
⚠️ Slightly delayed (~15–60 seconds)
Not intended for live trading decisions
📁 Project Structure
stock-widget/
│
├── main.py
├── icon.ico
├── dist/
│   └── main.exe
├── installer.iss
└── README.md
🔧 Build Executable
pyinstaller --onefile --noconsole --icon=icon.ico main.py

Output:

dist/main.exe
📦 Create Installer

Using Inno Setup:

Build → Compile → SensexNiftyWidgetSetup.exe
🧠 Key Concepts Implemented
Custom candlestick chart rendering
Real-time UI updates with QTimer
Desktop-layer widget behavior
Event-driven interaction (zoom, pan, hover)
Lightweight graphics pipeline
🚀 Future Improvements
📊 Indicators (EMA, RSI)
📈 Multiple stocks support
🔄 Real-time WebSocket data (Zerodha API)
⚙️ Settings panel
🌐 Cross-platform support
👤 Author

Vibhav
Publisher: thewitness


Project Description

SensexNiftyWidget is a lightweight Windows desktop application that displays real-time-like intraday charts for the NIFTY and SENSEX indices. The application is built using Python and the Qt framework (via PySide6), with a custom rendering pipeline for drawing candlestick charts instead of relying on external charting libraries.

The widget runs as a frameless desktop application that integrates with the Windows environment. It remains unobtrusive by staying behind active windows and is accessible through the system tray. The application fetches financial data from the Yahoo Finance API, processes it, and renders it in a continuously updating interface with smooth animations and interactive controls such as zoom, pan, and crosshair inspection.

The project demonstrates end-to-end desktop software development, including UI design, real-time data handling, custom graphics rendering, system-level window management, and packaging the application into a distributable Windows installer.

Step-by-Step Development Process

Below is the actual sequence followed to build the project, from scratch to a distributable application.

1. Defining the Goal
Objective: Build a lightweight desktop widget that shows stock charts.
Constraints:
Should not require browser or heavy frameworks
Must run as a standalone .exe
Should feel like a native desktop widget
Decision: Use Python for rapid development, later package into executable.
2. Choosing the Tech Stack
GUI framework: PySide6 (Qt for Python)
Data source: Yahoo Finance (unofficial API)
Rendering: Custom drawing using QPainter
Packaging: PyInstaller
Installer: Inno Setup

Reasoning:

Qt provides low-level control for custom UI
Avoided matplotlib to keep app lightweight
PyInstaller allows distributing without Python installed
3. Setting Up the Basic Window
Created a QWidget-based application
Removed window frame using:
FramelessWindowHint
Tool window flag
Positioned window manually (top-right corner)
Ensured it behaves like a widget (not a normal app window)
4. Fetching Stock Data
Used requests to call Yahoo Finance API:
Endpoint: /v8/finance/chart
Parsed JSON response:
Extracted timestamps
Extracted OHLC (Open, High, Low, Close)
Cleaned data:
Removed null values
Stored structured tuples (timestamp, open, high, low, close)
5. Designing Data Structures
Maintained:
data → raw fetched data
display_data → smoothed/interpolated data
Reason:
Avoid abrupt jumps in UI
Enable smooth animation
6. Implementing Rendering Engine
Used QPainter for custom drawing
Steps:
Normalize price values to screen coordinates
Map time index → x-axis
Draw grid lines
Draw candlestick:
wick (high to low)
body (open to close)
No external chart library used
7. Adding Real-Time Updates
Used QTimer:
Data fetch timer (every 10 seconds)
Animation timer (~30 FPS)
Implemented:
Continuous repaint loop
Smooth interpolation between old and new data
8. Implementing Interaction
Zoom
Mouse wheel adjusts visible candle count
Pan
Dragging shifts the data window (offset)
Crosshair
Mouse position tracked
Vertical and horizontal lines drawn
Displays OHLC + timestamp
9. Visual Feedback Enhancements
Price change detection:
Compared current price with previous
Added:
Color change (green/red)
Flash effect
Added pulse indicator:
Timer-based animation to show activity
10. Fixing UI Rendering Issues
Issue: Blue edges due to translucent background
Fix:
Adjusted drawing rectangle using rect().adjusted()
Ensured:
Proper anti-aliasing
Clean rounded corners
11. Desktop Integration
Used:
WindowStaysOnBottomHint to keep widget behind apps
Avoided unstable WorkerW hacks
Ensured:
Widget visible only on desktop
Does not interfere with normal window usage
12. System Tray Integration
Added QSystemTrayIcon
Created context menu:
Show
Hide
Exit
Overrode close behavior:
Close button hides instead of exiting
13. Performance Optimization
Limited number of candles rendered
Avoided heavy libraries
Used interpolation instead of re-rendering everything abruptly
Maintained smooth ~30 FPS UI updates
14. Packaging into Executable
Used PyInstaller:

Command:

pyinstaller --onefile --noconsole --icon=icon.ico main.py
Result:
Standalone main.exe
No Python installation required
15. Creating Installer
Used Inno Setup
Wrote .iss script:
Defined app name, version, publisher
Added shortcuts (desktop + start menu)
Included executable
Compiled into:
Setup.exe
16. Distribution Strategy
Packaged installer for easy installation
Recommended:
Upload via GitHub Releases
Avoided raw .exe distribution to reduce warnings
17. Validation
Compared displayed values with:
Google Finance
Trading platforms
Confirmed:
Data accuracy (with slight delay)

🧠 🧩 CORE SKILLS USED
🟢 1. Desktop Application Development
Built a native Windows desktop widget
Frameless window design
Always-on-bottom / widget-style behavior
System tray integration

👉 This is actual desktop engineering, not just scripting

🟢 2. GUI Programming (Qt)

Using:

PySide6 (Qt for Python)

Concepts:

Custom painting with QPainter
Event handling (mouse, wheel, hover)
Window flags & behavior control
Timers (QTimer) for real-time updates
🟢 3. Custom Graphics Rendering

You didn’t use a library — you built your own chart:

Candlestick chart rendering (OHLC)
Coordinate normalization
Dynamic scaling (min/max mapping)
Grid + UI layering

👉 This is basically graphics programming

🟢 4. Real-Time Data Handling
Fetching live stock data (Yahoo Finance API)
Parsing JSON
Handling missing/null values
Smoothing/interpolation for animation
🟢 5. Interactive UI Design

You implemented:

Zoom (mouse wheel)
Pan (drag)
Crosshair + tooltip
Live price updates
Hover detection

👉 These are trading-app-level interactions

🟢 6. State Management
Maintaining previous vs current data
Animation interpolation
Tracking UI states (hover, drag, zoom)
Price change detection
🟢 7. Windows-Specific Programming
Window layering (WindowStaysOnBottomHint)
System tray apps
Win32 API via ctypes (blur effects)
Understanding desktop/window hierarchy
🟢 8. Performance Optimization
30 FPS rendering loop
Lightweight drawing (no heavy libs)
Efficient updates (10s polling)
Avoiding flicker
🟢 9. Packaging & Distribution

Tools:

PyInstaller
Inno Setup

Concepts:

Bundling Python → .exe
Creating installer (Setup.exe)
Managing file paths
Application metadata (icon, version, publisher)
🟢 10. UX & Product Thinking

You handled:

Tray-based app behavior
No title bar UX
Visual feedback (pulse, flash)
Clean minimal UI
Desktop integration

👉 This is product-level thinking, not just coding

🧰 TECHNOLOGIES USED
🔧 Languages
Python
🧱 Frameworks / Libraries
PySide6 (Qt)
requests (API calls)
ctypes (Win32 API)
⚙️ Tools
PyInstaller (build .exe)
Inno Setup (installer)
GitHub (distribution)
🌐 APIs
Yahoo Finance (unofficial)
🧠 ADVANCED CONCEPTS TOUCHED
Event-driven programming
Rendering pipelines
Coordinate transformations
Real-time UI updates
OS-level window management
Software packaging
