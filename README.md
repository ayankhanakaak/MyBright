# MyBright

A Python-based intelligent auto-brightness system that adjusts display
brightness based on **actual screen content**, not ambient sensors.\
It uses real-time screenshot sampling, content-light analysis, baseline
interpolation, and customizable responsiveness modes.

------------------------------------------------------------------------

## ✨ Features

-   Dynamic brightness adjustment based on screen content
-   Screenshot-based light detection (instant + smoothed modes)
-   Manual baseline calibration workflow
-   Day/Night profile switching
-   Baseline persistence using JSON
-   Linear interpolation between baselines
-   Multiple responsiveness presets (Smooth → Instant)
-   Threaded auto-adjust loop
-   Automatic module installation
-   Detailed content-light preview and analysis

------------------------------------------------------------------------

## 📂 Files Structure

    MyBright-23.11.2025-2.py     # Main program file
    day_baselines.json           # Auto-generated after calibration (optional)
    night_baselines.json         # Auto-generated after calibration (optional)

------------------------------------------------------------------------

## 🚀 How It Works

1.  The program takes periodic screenshots.
2.  Converts them to grayscale and computes mean pixel intensity.
3.  Looks for the closest baseline(s) you created.
4.  Interpolates the correct brightness.
5.  Applies brightness through `screen_brightness_control`.

Baselines allow the program to learn your preferred brightness for
different screen-light conditions.

------------------------------------------------------------------------

## 🔧 Requirements

The program automatically installs required modules:

-   `numpy`
-   `Pillow`
-   `screen_brightness_control`

But you may install them manually if needed:

    pip install numpy
    pip install Pillow
    pip install screen_brightness_control

------------------------------------------------------------------------

## ▶️ Usage

Run the program:

    python "MyBright-23.11.2025-2.py"

You'll be presented with these options after choosing the mode (Day/Night):

1.  **Start Auto Brightness**
2.  **Stop Auto Brightness**
3.  **Set Manual Baseline**
4.  **Show Current Baselines**
5.  **Preview Content Light**
6.  **Set Responsiveness**
7.  **Switch Mode (Day/Night)**
8.  **Exit**

------------------------------------------------------------------------

## 🧪 Creating Baselines

To teach the program:

1.  Set your preferred brightness system-wide.
2.  Choose "Set Manual Baseline".
3.  Capture current screen or use a timed capture.
4.  Confirm baseline.

Over time, the program becomes more accurate depending on how many
baselines you provide.

------------------------------------------------------------------------

## ⚙️ Responsiveness Modes

-   Smooth (2 sec intervals, 3% threshold)
-   Balanced (1 sec intervals, 2% threshold)
-   Fast (0.7 sec intervals, 1% threshold)
-   Instant (0.5 sec intervals, 0% threshold) (Default)

------------------------------------------------------------------------

## 🛡️ Known Limitations

-   Some systems restrict screenshot capture (ImageGrab).
-   Brightness control may require admin privileges on certain laptops.

------------------------------------------------------------------------

## 📄 License

GPL-3.0

------------------------------------------------------------------------

## 👤 Author

**Developed by:** Ayan Khan\
**Message:** I'll try to publish an EXE (executable program) for Windows systems as soon as possible.

------------------------------------------------------------------------

## 🤝 Contributions

Pull requests are welcome!\
Feel free to report issues and suggest improvements.
