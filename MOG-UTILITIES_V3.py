import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import subprocess
import os
import threading
import shutil
import sys
import platform
import winreg
import ctypes
import requests
from pathlib import Path
import json
import socket
from datetime import datetime

class MOGUtilitiesV3:
    def __init__(self):
        if not self.check_admin():
            self.restart_as_admin()
            sys.exit()

        self.root = tk.Tk()
        self.root.title("MOG-UTILITIES V3")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")
        
        self.sidebar = tk.Frame(self.root, bg="#1f1f1f", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.main_content = tk.Frame(self.root, bg="#1a1a1a")
        self.main_content.pack(side="left", fill="both", expand=True)

        self.apps = {
            'Browsers': {
                'Google Chrome': 'https://dl.google.com/chrome/install/latest/chrome_installer.exe',
                'Mozilla Firefox': 'https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US',
                'Opera GX': 'https://download.opera.com/download/get/?partner=www&opsys=Windows',
                'Brave': 'https://laptop-updates.brave.com/latest/winx64',
                'Microsoft Edge': 'https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx',
                'Vivaldi': 'https://downloads.vivaldi.com/stable/Vivaldi.5.0.2497.48.x64.exe',
                'Tor Browser': 'https://www.torproject.org/dist/torbrowser/11.0.14/torbrowser-install-win64-11.0.14_en-US.exe'
            },
            'Gaming': {
                'Steam': 'https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe',
                'Epic Games': 'https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi',
                'Discord': 'https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x86',
                'GOG Galaxy': 'https://content-system.gog.com/open_link/download?path=/open/galaxy/client/2.0.51.86/setup_galaxy_2.0.51.86.exe',
                'Origin': 'https://origin-a.akamaihd.net/Origin-Client-Download/origin/live/OriginThinSetup.exe',
                'Uplay': 'https://ubi.li/4vxt9',
                'Battle.net': 'https://www.battle.net/download/getInstallerForGame?os=win&locale=enUS&version=LIVE&gameProgram=BATTLENET_APP'
            },
            'Development': {
                'Visual Studio Code': 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user',
                'Git': 'https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe',
                'Python': 'https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe',
                'Node.js': 'https://nodejs.org/dist/v16.14.0/node-v16.14.0-x64.msi',
                'Sublime Text': 'https://download.sublimetext.com/sublime_text_build_4126_x64_setup.exe'
            },
            'Utilities': {
                '7-Zip': 'https://www.7-zip.org/a/7z2107-x64.exe',
                'WinRAR': 'https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-611.exe',
                'VLC Media Player': 'https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe',
                'qBittorrent': 'https://downloads.sourceforge.net/project/qbittorrent/qbittorrent-win32/qbittorrent-4.4.0/qbittorrent_4.4.0_x64_setup.exe',
                'Everything Search': 'https://www.voidtools.com/Everything-1.4.1.1009.x64-Setup.exe'
            }
        }

        self.optimization_vars = {
            "System Optimization": {
                "Clear Temp Files": tk.BooleanVar(value=True),
                "Disk Cleanup": tk.BooleanVar(value=True),
                "Registry Cleanup": tk.BooleanVar(value=True),
                "Windows Services": tk.BooleanVar(value=True),
                "System File Check": tk.BooleanVar(value=True),
                "DISM Health Restore": tk.BooleanVar(value=True),
                "Clear Event Logs": tk.BooleanVar(value=True),
                "Defrag Drives": tk.BooleanVar(value=True),
                "Power Settings": tk.BooleanVar(value=True),
                "Visual Effects": tk.BooleanVar(value=True)
            },
            "Gaming Optimization": {
                "Game Mode": tk.BooleanVar(value=True),
                "High Performance": tk.BooleanVar(value=True),
                "Network Optimization": tk.BooleanVar(value=True),
                "Memory Optimization": tk.BooleanVar(value=True),
                "GPU Performance": tk.BooleanVar(value=True),
                "CPU Priority": tk.BooleanVar(value=True),
                "DirectX Cleanup": tk.BooleanVar(value=True),
                "Steam Cleanup": tk.BooleanVar(value=True),
                "Game DVR": tk.BooleanVar(value=True),
                "Fullscreen Optimization": tk.BooleanVar(value=True)
            }
        }

        self.create_sidebar()
        self.create_monitoring()
        self.show_home()

    def check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def restart_as_admin(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except:
            messagebox.showerror("Error", "This application requires administrator privileges.")

    def create_sidebar(self):
        title = tk.Label(
            self.sidebar,
            text="MOG-UTILITIES V3",
            bg="#1f1f1f",
            fg="#3391ff",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=30)

        buttons = [
            ("🏠 Home", self.show_home),
            ("⚡ Optimizer", self.show_optimizer),
            ("⚙️ Processes", self.show_processes),
            ("🎮 Gaming Mode", self.show_gaming),
            ("🗑️ Bloatware", self.remove_bloatware),
            ("📥 Install Apps", self.show_apps)
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#1f1f1f",
                fg="#3391ff", 
                font=("Segoe UI", 12),
                bd=0,
                activebackground="#2d2d2d",
                activeforeground="#3391ff",
                width=25,
                anchor="w",
                padx=30,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=5)

        self.optimize_all_btn = tk.Button(
            self.sidebar,
            text="OPTIMIZE ALL",
            command=self.optimize_all,
            bg="#00b300",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            bd=0,
            activebackground="#00cc00",
            activeforeground="white",
            height=3,
            cursor="hand2"
        )
        self.optimize_all_btn.pack(side="bottom", fill="x")

    def create_monitoring(self):
        self.cpu_label = tk.Label(
            self.sidebar,
            text="CPU: 0%",
            bg="#1f1f1f",
            fg="white",
            font=("Segoe UI", 10)
        )
        self.cpu_label.pack(side="bottom", pady=5)

        self.ram_label = tk.Label(
            self.sidebar,
            text="RAM: 0%",
            bg="#1f1f1f",
            fg="white",
            font=("Segoe UI", 10)
        )
        self.ram_label.pack(side="bottom", pady=5)

    def show_apps(self):
        self.clear_main_content()
        apps_frame = tk.Frame(self.main_content, bg="#1a1a1a")
        apps_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i in range(4):
            apps_frame.grid_columnconfigure(i, weight=1)

        current_row = 0
        
        for category, apps in self.apps.items():
            tk.Label(
                apps_frame,
                text=category,
                bg="#1a1a1a",
                fg="#3391ff",
                font=("Segoe UI", 14, "bold")
            ).grid(row=current_row, column=0, columnspan=4, sticky="w", pady=(10,5))
            
            current_row += 1
            col = 0
            
            for app_name, url in apps.items():
                btn = tk.Button(
                    apps_frame,
                    text=app_name,
                    command=lambda u=url, a=app_name: self.install_app(u, a),
                    bg="#2d2d2d",
                    fg="white",
                    font=("Segoe UI", 10),
                    width=25,
                    height=1,
                    bd=0,
                    cursor="hand2",
                    activebackground="#3d3d3d",
                    activeforeground="white"
                )
                btn.grid(row=current_row, column=col, padx=5, pady=2, sticky="ew")
                
                col += 1
                if col >= 4:
                    col = 0
                    current_row += 1
            
            current_row += 1

    def show_home(self):
        self.clear_main_content()
        
        welcome = tk.Label(
            self.main_content,
            text="Welcome to MOG-UTILITIES V3",
            bg="#1a1a1a",
            fg="#3391ff",
            font=("Segoe UI", 32, "bold")
        )
        welcome.pack(pady=50)

        actions = [
            ("⚡ Quick Optimize", self.quick_optimize),
            ("🎮 Gaming Mode", self.gaming_mode),
            ("📥 Install Apps", self.show_apps),
            ("🗑️ Remove Bloatware", self.remove_bloatware)
        ]

        for text, command in actions:
            btn = tk.Button(
                self.main_content,
                text=text,
                command=command,
                bg="#3391ff",
                fg="white",
                font=("Segoe UI", 14),
                width=30,
                height=2,
                bd=0,
                cursor="hand2"
            )
            btn.pack(pady=10)

    def show_optimizer(self):
        self.clear_main_content()
        
        notebook = ttk.Notebook(self.main_content)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)

        for category, options in self.optimization_vars.items():
            frame = tk.Frame(notebook, bg="#1a1a1a")
            notebook.add(frame, text=category)
            
            for i, (option, var) in enumerate(options.items()):
                row = i // 2
                column = i % 2
                
                cb = tk.Checkbutton(
                    frame,
                    text=option,
                    variable=var,
                    bg="#1a1a1a",
                    fg="white",
                    selectcolor="#1a1a1a",
                    activebackground="#1a1a1a",
                    activeforeground="white",
                    font=("Segoe UI", 10)
                )
                cb.grid(row=row, column=column, padx=20, pady=5, sticky="w")

        optimize_btn = tk.Button(
            self.main_content,
            text="Run Selected Optimizations",
            command=self.run_optimizations,
            bg="#3391ff",
            fg="white",
            font=("Segoe UI", 12),
            width=25,
            height=2,
            bd=0,
            cursor="hand2"
        )
        optimize_btn.pack(pady=20)

    def show_processes(self):
        self.clear_main_content()
        
        processes_frame = tk.Frame(self.main_content, bg="#1a1a1a")
        processes_frame.pack(fill="both", expand=True, padx=20, pady=20)

        headers = ["Process", "CPU %", "Memory %", "PID", "Status"]
        for i, header in enumerate(headers):
            tk.Label(
                processes_frame,
                text=header,
                bg="#1a1a1a",
                fg="#3391ff",
                font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=10, pady=5, sticky="w")

        row = 1
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'pid', 'status']):
            try:
                info = proc.info
                tk.Label(
                    processes_frame,
                    text=info['name'],
                    bg="#1a1a1a",
                    fg="white",
                    font=("Segoe UI", 9)
                ).grid(row=row, column=0, padx=10, pady=2, sticky="w")
                
                tk.Label(
                    processes_frame,
                    text=f"{info['cpu_percent']:.1f}%",
                    bg="#1a1a1a",
                    fg="white",
                    font=("Segoe UI", 9)
                ).grid(row=row, column=1, padx=10, pady=2, sticky="w")
                
                tk.Label(
                    processes_frame,
                    text=f"{info['memory_percent']:.1f}%",
                    bg="#1a1a1a",
                    fg="white",
                    font=("Segoe UI", 9)
                ).grid(row=row, column=2, padx=10, pady=2, sticky="w")
                
                tk.Label(
                    processes_frame,
                    text=str(info['pid']),
                    bg="#1a1a1a",
                    fg="white",
                    font=("Segoe UI", 9)
                ).grid(row=row, column=3, padx=10, pady=2, sticky="w")
                
                tk.Label(
                    processes_frame,
                    text=info['status'],
                    bg="#1a1a1a",
                    fg="white",
                    font=("Segoe UI", 9)
                ).grid(row=row, column=4, padx=10, pady=2, sticky="w")
                
                row += 1
            except:
                continue

    def show_gaming(self):
        self.clear_main_content()
        
        gaming_frame = tk.Frame(self.main_content, bg="#1a1a1a")
        gaming_frame.pack(fill="both", expand=True, padx=20, pady=20)

        options = [
            "Enable Game Mode",
            "Set High Performance Power Plan",
            "Optimize Network Settings",
            "Clear Standby Memory",
            "Set GPU High Performance",
            "Disable Background Apps",
            "Optimize Mouse Settings",
            "Disable Windows Updates",
            "Set CPU Priority",
            "Disable Visual Effects"
        ]

        for i, option in enumerate(options):
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(
                gaming_frame,
                text=option,
                variable=var,
                bg="#1a1a1a",
                fg="white",
                selectcolor="#1a1a1a",
                activebackground="#1a1a1a",
                activeforeground="white",
                font=("Segoe UI", 10)
            )
            cb.grid(row=i//2, column=i%2, padx=20, pady=5, sticky="w")

        tk.Button(
            gaming_frame,
            text="Apply Gaming Optimizations",
            command=self.apply_gaming_optimizations,
            bg="#3391ff",
            fg="white",
            font=("Segoe UI", 12),
            width=25,
            height=2,
            bd=0,
            cursor="hand2"
        ).grid(row=len(options)//2 + 1, column=0, columnspan=2, pady=20)

    def apply_gaming_optimizations(self):
        try:
            subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True, check=True)
            subprocess.run('reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f', shell=True, check=True)
            subprocess.run('reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 6 /f', shell=True, check=True)
            subprocess.run('reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f', shell=True, check=True)
            messagebox.showinfo("Success", "Gaming optimizations applied!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to apply gaming optimizations. Please run as administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def remove_bloatware(self):
        self.clear_main_content()
        
        bloatware_frame = tk.Frame(self.main_content, bg="#1a1a1a")
        bloatware_frame.pack(fill="both", expand=True, padx=20, pady=20)

        bloatware_list = [
            "Microsoft.3DBuilder",
            "Microsoft.WindowsAlarms",
            "Microsoft.WindowsCalculator",
            "Microsoft.WindowsCamera",
            "Microsoft.GetHelp",
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo",
            "Microsoft.MicrosoftOfficeHub",
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.WindowsMaps",
            "Microsoft.BingNews",
            "Microsoft.Office.OneNote",
            "Microsoft.People",
            "Microsoft.Windows.Photos",
            "Microsoft.SkypeApp",
            "Microsoft.WindowsSoundRecorder",
            "Microsoft.BingSports",
            "Microsoft.MicrosoftStickyNotes",
            "Microsoft.WindowsStore",
            "Microsoft.WindowsPhone",
            "Microsoft.XboxApp"
        ]

        for i, app in enumerate(bloatware_list):
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(
                bloatware_frame,
                text=app,
                variable=var,
                bg="#1a1a1a",
                fg="white",
                selectcolor="#1a1a1a",
                activebackground="#1a1a1a",
                activeforeground="white",
                font=("Segoe UI", 9)
            )
            cb.grid(row=i//4, column=i%4, padx=10, pady=2, sticky="w")

        tk.Button(
            bloatware_frame,
            text="Remove Selected Bloatware",
            command=lambda: self.remove_selected_bloatware(bloatware_list),
            bg="#3391ff",
            fg="white",
            font=("Segoe UI", 11),
            width=25,
            height=2,
            bd=0,
            cursor="hand2"
        ).grid(row=(len(bloatware_list)//4)+1, column=0, columnspan=4, pady=20)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def update_monitoring(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.cpu_label.config(text=f"CPU: {cpu}%")
            self.ram_label.config(text=f"RAM: {ram}%")
        except:
            pass
        self.root.after(1000, self.update_monitoring)

    def install_app(self, url, app_name):
        try:
            download_path = os.path.join(os.getenv('TEMP'), f"{app_name.lower().replace(' ', '_')}_installer.exe")
            
            def download_and_install():
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    with open(download_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    subprocess.Popen(download_path, shell=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to download {app_name}: {str(e)}")
                
            threading.Thread(target=download_and_install).start()
            messagebox.showinfo("Installing", f"Starting download of {app_name}...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install {app_name}: {str(e)}")

    def run_optimizations(self):
        selected = []
        for category, options in self.optimization_vars.items():
            for option, var in options.items():
                if var.get():
                    selected.append(option)

        if not selected:
            messagebox.showwarning("Warning", "No optimizations selected!")
            return

        try:
            for optimization in selected:
                if optimization == "Clear Temp Files":
                    self.clear_temp_files()
                elif optimization == "Disk Cleanup":
                    self.disk_cleanup()
                elif optimization == "Registry Cleanup":
                    self.registry_cleanup()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run optimizations: {str(e)}")
            return

        messagebox.showinfo("Success", "Selected optimizations completed!")

    def remove_selected_bloatware(self, apps):
        try:
            for app in apps:
                subprocess.run(f'powershell "Get-AppxPackage *{app}* | Remove-AppxPackage"', shell=True, check=True)
            messagebox.showinfo("Success", "Selected bloatware removed!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to remove bloatware. Please run as administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def optimize_all(self):
        for category in self.optimization_vars.values():
            for var in category.values():
                var.set(True)
        self.run_optimizations()

    def quick_optimize(self):
        try:
            self.clear_temp_files()
            self.disk_cleanup()
            messagebox.showinfo("Success", "Quick optimization completed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run quick optimization: {str(e)}")

    def gaming_mode(self):
        try:
            subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True, check=True)
            messagebox.showinfo("Success", "Gaming Mode enabled!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to enable Gaming Mode. Please run as administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_temp_files(self):
        temp_paths = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            os.path.join(os.environ.get('WINDIR'), 'Temp')
        ]
        
        for path in temp_paths:
            if path and os.path.exists(path):
                try:
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        try:
                            if os.path.isfile(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                        except:
                            continue
                except:
                    continue

    def disk_cleanup(self):
        try:
            subprocess.run('cleanmgr /sagerun:1', shell=True, check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to run Disk Cleanup. Please run as administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def registry_cleanup(self):
        try:
            subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU" /va /f', shell=True, check=True)
            subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths" /va /f', shell=True, check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to clean registry. Please run as administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.update_monitoring()
        self.root.mainloop()

if __name__ == "__main__":
    app = MOGUtilitiesV3()
    app.run()
