'''Imporint Modules'''
import os
import json
import time
import threading
from dataclasses import dataclass
from typing import List, Dict, Tuple
import subprocess

previous_module_imported=False
first_import=True
import_count=0
everything_imported=False
while True:
    try:
        import_count+=1
        import numpy as np
        previous_module_imported=True
        everything_imported=True
        if first_import==False:
            print("IMPORTED!\n")
        break
    except ModuleNotFoundError:
        if import_count<4:
            print("ERROR: Module 'numpy' not found.\nTrying to install from internet...")
            print("══════════════════════════════════")
            subprocess.run("pip install numpy",shell=True)
            print("══════════════════════════════════")
            print("Trying to import again...")
            first_import=False
        else:
            print("\nOOOPS!\nTried 3 times, but failed to install 'numpy'.\nYou manually try installing by running 'pip install numpy' in an elevated CMD.\nOr tell me the issue at ayankhantnp786@gmail.com.\n")
            previous_module_imported=False
            break

if previous_module_imported==True:
    first_import=True
    import_count=0
    everything_imported=False
    while True:
        try:
            import_count+=1
            from PIL import Image, ImageGrab
            previous_module_imported=True
            everything_imported=True
            if first_import==False:
                print("IMPORTED!\n")
            break
        except ModuleNotFoundError:
            if import_count<4:
                print("ERROR: Module 'PIL' not found.\nTrying to install from internet...")
                print("══════════════════════════════════")
                subprocess.run("pip install Pillow",shell=True)
                print("══════════════════════════════════")
                print("Trying to import again...")
                first_import=False
            else:
                print("\nOOOPS!\nTried 3 times, but failed to install 'PIL'.\nYou manually try installing by running 'pip install Pillow' in an elevated CMD.\nOr tell me the issue at ayankhantnp786@gmail.com.\n")
                previous_module_imported=False
                break            

if previous_module_imported==True:
    first_import=True
    import_count=0
    everything_imported=False
    while True:
        try:
            import_count+=1
            import screen_brightness_control as sbc
            everything_imported=True
            previous_module_imported=True
            if first_import==False:
                print("IMPORTED!\n")
            break
        except ModuleNotFoundError:
            if import_count<4:
                print("ERROR: Module 'screen_brightness_control' not found.\nTrying to install from internet...")
                print("══════════════════════════════════")
                subprocess.run("pip install screen_brightness_control",shell=True)
                print("══════════════════════════════════")
                print("Trying to import again...")
                first_import=False
            else:
                print("\nOOOPS!\nTried 3 times, but failed to install 'screen_brightness_control'.\nYou manually try installing by running 'pip install screen_brightness_control' in an elevated CMD.\nOr tell me the issue at ayankhantnp786@gmail.com.\n")
                previous_module_imported=False
                break 
'''Modules Imported'''

if everything_imported==True:
    @dataclass
    class Baseline:
        content_light: float
        brightness: int

    class AutoBrightnessController:
        def __init__(self):
            self.modes = {"1": "day", "2": "night"}
            self.current_mode = None
            self.baselines_file = None
            self.baselines: List[Baseline] = []
            self.running = False
            self.manual_override = False
            self.last_manual_brightness = None
            
            '''Responsiveness settings'''
            self.change_threshold = 1       #Default: 1% change threshold
            self.check_interval = 0.5       #Default: 0.5 seconds (Instant mode)
            self.verbose_logging = True     #Default: show all logs
            
            '''Content light detection settings'''
            self.content_light_history = []
            self.ignore_edges = True
            self.edge_percentage = 0.1
            
        def get_instant_content_light(self) -> float:
            '''Get instant content light without any smoothing - for auto mode'''
            try:
                '''Capture screenshot'''
                screenshot = ImageGrab.grab()
                
                '''Convert to grayscale for brightness analysis'''
                grayscale = screenshot.convert('L')
                
                '''Convert to numpy array for efficient calculation'''
                img_array = np.array(grayscale)
                
                '''Ignore edges if enabled (where UI elements often are)'''
                if self.ignore_edges and img_array.shape[0] > 20 and img_array.shape[1] > 20:
                    h, w = img_array.shape
                    edge_h = int(h * self.edge_percentage)
                    edge_w = int(w * self.edge_percentage)
                    img_array = img_array[edge_h:h-edge_h, edge_w:w-edge_w]
                
                '''Calculate mean brightness (0-255 scale)'''
                content_light = np.mean(img_array)
                
                return float(content_light)
            except Exception as e:
                print(f"Error calculating content light: {e}")
                return 50.0  #Default value
        
        def get_smoothed_content_light(self, samples=5) -> float:
            '''Get smoothed content light by averaging multiple samples - for manual baseline setting'''
            current_samples = []
            
            for i in range(samples):
                try:
                    content_light = self.get_instant_content_light()
                    current_samples.append(content_light)
                    
                    '''Small delay between samples if taking multiple'''
                    if i < samples - 1:
                        time.sleep(0.1)
                except Exception as e:
                    print(f"Error in sample {i+1}: {e}")
                    continue
            
            if not current_samples:
                return 50.0  #Default if all samples fail
            
            '''Calculate mean and remove outliers'''
            if len(current_samples) >= 3:
                mean_val = np.mean(current_samples)
                std_val = np.std(current_samples)
                
                '''Remove outliers (beyond 2 standard deviations)'''
                filtered_samples = [x for x in current_samples if abs(x - mean_val) <= 2 * std_val]
                
                if filtered_samples:
                    smoothed_light = np.mean(filtered_samples)
                else:
                    smoothed_light = mean_val
            else:
                smoothed_light = np.mean(current_samples)
            
            return float(smoothed_light)
        
        def analyze_content_distribution(self) -> Dict:
            '''Analyze the distribution of content light for debugging'''
            try:
                screenshot = ImageGrab.grab()
                grayscale = screenshot.convert('L')
                img_array = np.array(grayscale)
                
                analysis = {
                    'mean': float(np.mean(img_array)),
                    'median': float(np.median(img_array)),
                    'std': float(np.std(img_array)),
                    'min': float(np.min(img_array)),
                    'max': float(np.max(img_array)),
                    'q1': float(np.percentile(img_array, 25)),
                    'q3': float(np.percentile(img_array, 75)),
                }
                
                return analysis
            except Exception as e:
                print(f"Error in content analysis: {e}")
                return {}
        
        def load_baselines(self):
            '''Load baselines from file for current mode'''
            self.baselines = []
            try:
                if os.path.exists(self.baselines_file):
                    with open(self.baselines_file, 'r') as f:
                        data = json.load(f)
                        for baseline_data in data.get('baselines', []):
                            self.baselines.append(
                                Baseline(
                                    content_light=baseline_data['content_light'],
                                    brightness=baseline_data['brightness']
                                )
                            )
                    print(f"Loaded {len(self.baselines)} baselines for {self.current_mode} mode")
            except Exception as e:
                print(f"Error loading baselines: {e}")
        
        def save_baselines(self):
            '''Save baselines to file'''
            try:
                data = {
                    'mode': self.current_mode,
                    'baselines': [
                        {
                            'content_light': baseline.content_light,
                            'brightness': baseline.brightness
                        }
                        for baseline in self.baselines
                    ]
                }
                
                with open(self.baselines_file, 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                print(f"Error saving baselines: {e}")
        
        def add_baseline(self, content_light: float, brightness: int):
            '''Add or update a baseline point
            Check if baseline exists for this content light'''
            for baseline in self.baselines:
                if abs(baseline.content_light - content_light) < 1.0:  #Increased tolerance
                    baseline.brightness = brightness
                    print(f"Updated baseline: Content Light {content_light:.1f} -> Brightness {brightness}")
                    self.save_baselines()
                    return
            
            '''Add new baseline'''
            self.baselines.append(Baseline(content_light, brightness))
            print(f"Added new baseline: Content Light {content_light:.1f} -> Brightness {brightness}")
            self.save_baselines()
        
        def calculate_target_brightness(self, current_content_light: float) -> int:
            '''Calculate target brightness based on content light and baselines'''
            if not self.baselines:
                return 50  #Default brightness if no baselines
            
            '''Sort baselines by content light'''
            sorted_baselines = sorted(self.baselines, key=lambda x: x.content_light)
            
            '''Find the closest baselines for interpolation'''
            lower_baseline = None
            upper_baseline = None
            
            for baseline in sorted_baselines:
                if baseline.content_light <= current_content_light:
                    lower_baseline = baseline
                if baseline.content_light >= current_content_light:
                    upper_baseline = baseline
                    break
            
            '''Case 1: Exact match or very close (increased tolerance)'''
            if lower_baseline and abs(lower_baseline.content_light - current_content_light) < 1.0:
                return lower_baseline.brightness
            
            '''Case 2: Interpolation between two baselines'''
            if lower_baseline and upper_baseline:
                '''Linear interpolation'''
                content_range = upper_baseline.content_light - lower_baseline.content_light
                brightness_range = upper_baseline.brightness - lower_baseline.brightness
                
                if content_range == 0:  #Avoid division by zero
                    return lower_baseline.brightness
                
                ratio = (current_content_light - lower_baseline.content_light) / content_range
                target_brightness = lower_baseline.brightness + (brightness_range * ratio)
                return max(0, min(100, int(target_brightness)))
            
            '''Case 3: Outside range - use closest baseline'''
            if current_content_light < sorted_baselines[0].content_light:
                return sorted_baselines[0].brightness
            else:
                return sorted_baselines[-1].brightness
        
        def set_brightness(self, brightness: int):
            '''Set system brightness'''
            try:
                brightness = max(0, min(100, brightness))  #Clamp to 0-100
                sbc.set_brightness(brightness)
                return True
            except Exception as e:
                print(f"Error setting brightness: {e}")
                return False
        
        def get_current_brightness(self) -> int:
            '''Get current system brightness'''
            try:
                return sbc.get_brightness()[0]  #First monitor
            except:
                return 50
        
        def capture_content_with_delay(self, delay_seconds: int = 3) -> float:
            '''Capture content light after a delay with smoothing - for manual baseline'''
            print(f"\nYou have {delay_seconds} seconds to switch to the target window...")
            print("Make sure the content you want to baseline is visible!")
            
            for i in range(delay_seconds, 0, -1):
                print(f"Capturing in {i}...")
                time.sleep(1)
            
            print("Capturing screen content now...")
            '''Use SMOOTHED capture for manual baseline'''
            content_light = self.get_smoothed_content_light(samples=3)
            print(f"Content Light captured: {content_light:.1f}")
            
            return content_light
        
        def set_responsiveness(self):
            '''Configure how quickly the system responds to content changes'''
            print("\n=== Responsiveness Settings ===")
            print("How quickly should brightness adjust to content changes?")
            print("1. Smooth (2 sec intervals, 3% threshold)")
            print("2. Balanced (1 sec intervals, 2% threshold)") 
            print("3. Fast (0.7 sec intervals, 1% threshold)")
            print("4. Instant (0.5 sec intervals, 0% threshold)")
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":  #Smooth
                self.change_threshold = 3
                self.check_interval = 2
                print("Set to Smooth mode")
            elif choice == "2":  #Balanced
                self.change_threshold = 2
                self.check_interval = 1
                print("Set to Balanced mode")
            elif choice == "3":  #Fast
                self.change_threshold = 1
                self.check_interval = 0.7
                print("Set to Fast mode")
            elif choice == "4":  #Instant
                self.change_threshold = 0
                self.check_interval = 0.5
                print("Set to Instant mode")
            else:
                print("Invalid choice, using Instant mode")
                self.change_threshold = 0
                self.check_interval = 0.5
        
        def get_responsiveness_name(self):
            '''Get the current responsiveness mode name'''
            if self.check_interval >= 2 and self.change_threshold >= 3:
                return "Smooth"
            elif self.check_interval <= 0.5 and self.change_threshold == 0:
                return "Instant"
            elif self.check_interval <= 0.7 and self.change_threshold <= 1:
                return "Fast"
            else:
                return "Balanced"
        
        def update_auto_adjust_loop(self):
            '''Auto-adjust loop with instant content detection'''
            mode_name = self.get_responsiveness_name()
            print(f"Auto brightness started (mode: {mode_name}). Press Ctrl+C to stop.")
            
            while self.running:
                try:
                    '''Use INSTANT content light detection for auto mode (no smoothing)'''
                    content_light = self.get_instant_content_light()
                    
                    '''Calculate target brightness'''
                    target_brightness = self.calculate_target_brightness(content_light)
                    
                    '''Set brightness'''
                    current_brightness = self.get_current_brightness()
                    
                    '''Only adjust if change is significant (based on threshold)'''
                    if abs(target_brightness - current_brightness) >= self.change_threshold:
                        if self.set_brightness(target_brightness):
                            print(f"Content Light: {content_light:.1f} -> Brightness: {target_brightness}")
                    
                    time.sleep(self.check_interval)
                    
                except Exception as e:
                    print(f"Error in auto-adjust loop: {e}")
                    time.sleep(self.check_interval)
        
        def manual_brightness_set(self):
            '''Handle manual brightness setting with SMOOTHED content capture'''
            try:
                print("\n=== Manual Baseline Setting ===")
                print("1. Capture current screen (quick)")
                print("2. Capture with delay (switch to target window)")
                print("3. Use specific content light value")
                
                choice = input("Enter choice (1-3): ").strip()
                
                if choice == "1":
                    '''Use SMOOTHED capture for manual baseline setting'''
                    content_light = self.get_smoothed_content_light(samples=3)
                elif choice == "2":
                    delay = int(input("Enter delay in seconds (default 3): ") or "3")
                    content_light = self.capture_content_with_delay(delay)
                elif choice == "3":
                    content_light = float(input("Enter content light value (0-255): "))
                else:
                    print("Invalid choice, using current screen.")
                    content_light = self.get_smoothed_content_light(samples=3)
                
                current_brightness = self.get_current_brightness()
                
                print(f"\nRecording baseline:")
                print(f"Content Light: {content_light:.1f}")
                print(f"Brightness: {current_brightness}")
                
                confirm = input("Confirm this baseline? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.add_baseline(content_light, current_brightness)
                    self.last_manual_brightness = current_brightness
                    print("Baseline saved successfully!")
                else:
                    print("Baseline not saved.")
                    
            except Exception as e:
                print(f"Error in manual brightness set: {e}")
        
        def preview_content_light(self):
            '''Preview current content light with detailed analysis'''
            try:
                print("\nPreviewing content light...")
                
                '''Take multiple samples to show consistency'''
                print("Taking instant samples:")
                samples = []
                for i in range(3):
                    content_light = self.get_instant_content_light()
                    samples.append(content_light)
                    print(f"  Sample {i+1}: {content_light:.1f}")
                    if i < 2:
                        time.sleep(0.3)
                
                instant_light = self.get_instant_content_light()
                smoothed_light = self.get_smoothed_content_light(samples=3)
                
                print(f"\nInstant Reading: {instant_light:.1f}")
                print(f"Smoothed Reading: {smoothed_light:.1f}")
                
                '''Show analysis'''
                analysis = self.analyze_content_distribution()
                if analysis:
                    print(f"\nDetailed Analysis:")
                    print(f"  Mean: {analysis['mean']:.1f}")
                    print(f"  Median: {analysis['median']:.1f}")
                    print(f"  Std Dev: {analysis['std']:.1f}")
                    print(f"  Range: {analysis['min']:.1f} - {analysis['max']:.1f}")
                
                '''Show what brightness would be set automatically'''
                if self.baselines:
                    target_brightness = self.calculate_target_brightness(instant_light)
                    print(f"\nWould set brightness to: {target_brightness}")
            except Exception as e:
                print(f"Error previewing content light: {e}")
        
        def start_auto_mode(self):
            '''Start automatic brightness adjustment'''
            self.running = True
            auto_thread = threading.Thread(target=self.update_auto_adjust_loop, daemon=True)
            auto_thread.start()
        
        def stop_auto_mode(self):
            '''Stop automatic brightness adjustment'''
            self.running = False
            print("Auto brightness stopped.")
        
        def show_baselines(self):
            '''Display current baselines'''
            if not self.baselines:
                print("No baselines set yet.")
                return
            
            print(f"\nCurrent baselines for {self.current_mode} mode:")
            for baseline in sorted(self.baselines, key=lambda x: x.content_light):
                print(f"  Content Light {baseline.content_light:.1f} : Brightness {baseline.brightness}")
        
        def select_mode(self):
            '''Let user select day/night mode'''
            print("Select Mode:")
            print("1. Day Mode")
            print("2. Night Mode")
            
            while True:
                choice = input("Enter choice (1 or 2): ").strip()
                if choice in self.modes:
                    self.current_mode = self.modes[choice]
                    self.baselines_file = f"{self.current_mode}_baselines.json"
                    self.load_baselines()
                    print(f"{self.current_mode.capitalize()} mode selected.")
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
        
        def run(self):
            '''Main program loop'''
            print("=== Auto Brightness Program ===")
            print("This program adjusts brightness based on screen content.")
            print("Default mode: Instant responsiveness")
            
            '''Select mode'''
            self.select_mode()
            
            '''Main menu'''
            while True:
                print(f"\n--- {self.current_mode.capitalize()} Mode ---")
                print("1. Start Auto Brightness")
                print("2. Stop Auto Brightness")
                print("3. Set Manual Baseline")
                print("4. Show Current Baselines")
                print("5. Preview Content Light (Detailed)")
                print("6. Set Responsiveness")
                print("7. Switch Mode")
                print("8. Exit")
                
                choice = input("Enter choice (1-8): ").strip()
                
                if choice == "1":
                    self.start_auto_mode()
                elif choice == "2":
                    self.stop_auto_mode()
                elif choice == "3":
                    print("\nFirst, manually adjust your brightness using system controls.")
                    print("Set the brightness to your preferred level for the current content.")
                    input("Press Enter when you have set the desired brightness...")
                    self.manual_brightness_set()
                elif choice == "4":
                    self.show_baselines()
                elif choice == "5":
                    self.preview_content_light()
                elif choice == "6":
                    self.set_responsiveness()
                elif choice == "7":
                    self.stop_auto_mode()
                    self.select_mode()
                elif choice == "8":
                    self.stop_auto_mode()
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1-8.")

    def main():
        '''Main function'''
        try:
            controller = AutoBrightnessController()
            controller.run()
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    if __name__ == "__main__":
        main()