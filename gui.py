#!/usr/bin/env python3
"""
AugmentCode-Free GUI Application
A modern graphical user interface for VS Code maintenance tools.
"""

import tkinter as tk
import threading
import sys
from pathlib import Path
import queue
import time
import subprocess
import platform

# Import the core functionality
from augment_tools_core.common_utils import (
    get_os_specific_vscode_paths,
    print_info,
    print_success,
    print_error,
    print_warning
)
from augment_tools_core.database_manager import clean_vscode_database
from augment_tools_core.telemetry_manager import modify_vscode_telemetry_ids


class CursorProButton(tk.Frame):
    """CursorPro style rounded button widget"""
    def __init__(self, parent, text, command, style="primary", **kwargs):
        super().__init__(parent, bg='#f5f5f5', **kwargs)

        self.command = command
        self.is_hovered = False
        self.is_disabled = False
        self.style = style
        self.text = text

        # Button styles
        if style == "primary":
            self.normal_bg = '#4f46e5'
            self.normal_fg = '#ffffff'
            self.hover_bg = '#4338ca'
            self.hover_fg = '#ffffff'
        else:
            self.normal_bg = '#f3f4f6'
            self.normal_fg = '#6b7280'
            self.hover_bg = '#e5e7eb'
            self.hover_fg = '#374151'

        # Create canvas for rounded button with more height for better rounding
        self.canvas = tk.Canvas(self, height=55, highlightthickness=0,
                               bg='#f5f5f5', cursor='hand2')
        self.canvas.pack(fill='both', expand=True)

        # Bind events
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Enter>', self._on_enter)
        self.canvas.bind('<Leave>', self._on_leave)
        self.bind('<Configure>', self._on_configure)

        self._draw_button()

    def _draw_button(self):
        """Draw rounded button"""
        self.canvas.delete('all')
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Choose colors based on state
        if self.is_disabled:
            bg_color = '#d1d5db'
            text_color = '#9ca3af'
        elif self.is_hovered:
            bg_color = self.hover_bg
            text_color = self.hover_fg
        else:
            bg_color = self.normal_bg
            text_color = self.normal_fg

        # Draw rounded rectangle with more obvious corners
        radius = 15  # Increased radius for more obvious rounding
        self._create_rounded_rect(2, 2, width-2, height-2, radius,
                                 fill=bg_color, outline='')

        # Draw text
        self.canvas.create_text(width//2, height//2, text=self.text,
                               fill=text_color, font=('Microsoft YaHei', 13))

    def _create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def _on_configure(self, event=None):
        """Handle resize"""
        self.after_idle(self._draw_button)

    def _on_click(self, event=None):
        """Handle click event"""
        if not self.is_disabled and self.command:
            self.command()

    def _on_enter(self, event=None):
        """Handle mouse enter"""
        if not self.is_disabled:
            self.is_hovered = True
            self._draw_button()

    def _on_leave(self, event=None):
        """Handle mouse leave"""
        if not self.is_disabled:
            self.is_hovered = False
            self._draw_button()

    def config_state(self, state):
        """Configure button state"""
        if state == 'disabled':
            self.is_disabled = True
            self.canvas.config(cursor='')
        else:
            self.is_disabled = False
            self.canvas.config(cursor='hand2')
        self._draw_button()


class ModernDialog:
    """Modern dialog box that matches our UI style"""
    def __init__(self, parent, title, message, dialog_type="info"):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)

        # Calculate height based on message length
        lines = message.count('\n') + 1
        base_height = 200
        extra_height = max(0, (lines - 3) * 20)  # Add 20px per extra line
        dialog_height = min(400, base_height + extra_height)  # Cap at 400px

        self.dialog.geometry(f"350x{dialog_height}")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#f5f5f5')
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (dialog_height // 2)
        self.dialog.geometry(f'350x{dialog_height}+{x}+{y}')

        self._create_dialog(title, message, dialog_type)

    def _create_dialog(self, title, message, dialog_type):
        """Create the dialog content"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)

        # Icon and title in one line
        header_frame = tk.Frame(main_frame, bg='#f5f5f5')
        header_frame.pack(fill='x', pady=(0, 10))

        # Icon
        icon_text = "⚠️" if dialog_type == "warning" else "ℹ️"
        icon_label = tk.Label(header_frame, text=icon_text,
                             font=('Microsoft YaHei', 16),
                             fg='#f59e0b' if dialog_type == "warning" else '#3b82f6',
                             bg='#f5f5f5')
        icon_label.pack(side='left', padx=(0, 8))

        # Title
        title_label = tk.Label(header_frame, text=title,
                              font=('Microsoft YaHei', 14, 'bold'),
                              fg='#1f2937', bg='#f5f5f5')
        title_label.pack(side='left')

        # Message
        message_label = tk.Label(main_frame, text=message,
                                font=('Microsoft YaHei', 10),
                                fg='#4b5563', bg='#f5f5f5',
                                wraplength=310, justify='left')
        message_label.pack(pady=(0, 20), fill='x')

        # Buttons at the bottom
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(fill='x', pady=(10, 0))

        if dialog_type == "warning":
            # Yes/No buttons for warning dialogs
            # Cancel button on the left
            no_btn = tk.Button(button_frame, text="取消",
                              command=lambda: self._set_result(False),
                              font=('Microsoft YaHei', 10),
                              bg='#f3f4f6', fg='#6b7280',
                              relief='flat', bd=0, cursor='hand2',
                              activebackground='#e5e7eb',
                              activeforeground='#374151',
                              padx=20, pady=8)
            no_btn.pack(side='left')

            # Add hover effects for cancel button
            def on_cancel_enter(_):
                no_btn.config(bg='#e5e7eb', fg='#374151')
            def on_cancel_leave(_):
                no_btn.config(bg='#f3f4f6', fg='#6b7280')
            no_btn.bind('<Enter>', on_cancel_enter)
            no_btn.bind('<Leave>', on_cancel_leave)

            # Confirm button on the right
            yes_btn = tk.Button(button_frame, text="确认",
                               command=lambda: self._set_result(True),
                               font=('Microsoft YaHei', 10),
                               bg='#4f46e5', fg='#ffffff',
                               relief='flat', bd=0, cursor='hand2',
                               activebackground='#4338ca',
                               activeforeground='#ffffff',
                               padx=20, pady=8)
            yes_btn.pack(side='right')

            # Add hover effects for confirm button
            def on_confirm_enter(_):
                yes_btn.config(bg='#4338ca')
            def on_confirm_leave(_):
                yes_btn.config(bg='#4f46e5')
            yes_btn.bind('<Enter>', on_confirm_enter)
            yes_btn.bind('<Leave>', on_confirm_leave)

        else:
            # OK button for info dialogs
            ok_btn = tk.Button(button_frame, text="确定",
                              command=lambda: self._set_result(True),
                              font=('Microsoft YaHei', 10),
                              bg='#4f46e5', fg='#ffffff',
                              relief='flat', bd=0, cursor='hand2',
                              activebackground='#4338ca',
                              activeforeground='#ffffff',
                              padx=20, pady=8)
            ok_btn.pack(side='right')

            # Add hover effects for OK button
            def on_ok_enter(_):
                ok_btn.config(bg='#4338ca')
            def on_ok_leave(_):
                ok_btn.config(bg='#4f46e5')
            ok_btn.bind('<Enter>', on_ok_enter)
            ok_btn.bind('<Leave>', on_ok_leave)

    def _set_result(self, result):
        """Set result and close dialog"""
        self.result = result
        self.dialog.destroy()

    def show(self):
        """Show dialog and return result"""
        self.dialog.wait_window()
        return self.result

# Helper functions for showing dialogs
def show_warning(parent, title, message):
    """Show warning dialog"""
    dialog = ModernDialog(parent, title, message, "warning")
    return dialog.show()

def show_info(parent, title, message):
    """Show info dialog"""
    dialog = ModernDialog(parent, title, message, "info")
    return dialog.show()


class AugmentToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AugmentCode-Free")
        self.root.geometry("380x580")  # Larger for 4 buttons and complete text display
        self.root.resizable(False, False)

        # Set window style like CursorPro
        self.root.configure(bg='#f5f5f5')

        # Center the window
        self.center_window()

        # Queue for thread-safe GUI updates
        self.message_queue = queue.Queue()

        # Setup GUI components
        self.setup_gui()

        # Start the message processor
        self.process_messages()

        # Override print functions to redirect to GUI
        self.setup_print_redirection()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_gui(self):
        """Setup the CursorPro-style GUI components"""
        # Main container with CursorPro-like background
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Logo/Icon area - CursorPro style circular icon
        icon_frame = tk.Frame(main_frame, bg='#f5f5f5', height=100)
        icon_frame.pack(fill='x', pady=(0, 20))

        # Create gradient title using canvas that fills the frame width
        title_canvas = tk.Canvas(icon_frame, height=60, bg='#f5f5f5',
                                highlightthickness=0)
        title_canvas.pack(fill='x', pady=(20, 5))

        # Store canvas for animation
        self.title_canvas = title_canvas
        self.gradient_offset = 0

        # Wait for canvas to be properly sized, then start animation
        self.root.after(100, self._animate_gradient)

        # Welcome text
        welcome_label = tk.Label(icon_frame, text="欢迎使用",
                                font=('Microsoft YaHei', 12),
                                fg='#6b7280', bg='#f5f5f5')
        welcome_label.pack(pady=(0, 25))

        # Buttons container
        buttons_frame = tk.Frame(main_frame, bg='#f5f5f5')
        buttons_frame.pack(fill='x', pady=(0, 20))

        # Create uniform blue buttons with proper text

        self.run_all_btn = CursorProButton(buttons_frame, "一键修改所有VSCode配置",
                                          self.run_all_clicked, style="primary")
        self.run_all_btn.pack(fill='x', pady=(0, 12))

        self.close_vscode_btn = CursorProButton(buttons_frame, "关闭VSCode",
                                               self.close_vscode_clicked, style="primary")
        self.close_vscode_btn.pack(fill='x', pady=(0, 12))

        self.clean_db_btn = CursorProButton(buttons_frame, "清理VSCode数据库",
                                           self.clean_database_clicked, style="primary")
        self.clean_db_btn.pack(fill='x', pady=(0, 12))

        self.modify_ids_btn = CursorProButton(buttons_frame, "修改VSCode遥测ID",
                                             self.modify_ids_clicked, style="primary")
        self.modify_ids_btn.pack(fill='x', pady=(0, 12))

        self.modify_ids_btn = CursorProButton(buttons_frame, "登录新账号",
                                              self.login_aug_clicked, style="primary")
        self.modify_ids_btn.pack(fill='x', pady=(0, 12))

        # Set default keyword (no UI input needed)
        self.keyword_var = tk.StringVar(value="augment")

        # Version info at bottom (like CursorPro)
        version_frame = tk.Frame(main_frame, bg='#f5f5f5')
        version_frame.pack(fill='x', pady=(40, 20))  # More space at bottom

        version_label = tk.Label(version_frame, text="v0.0.2",
                                font=('Microsoft YaHei', 12),
                                fg='#9ca3af', bg='#f5f5f5')
        version_label.pack()

        # Status info (hidden by default, shown in status updates)
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(version_frame, textvariable=self.status_var,
                                    font=('Microsoft YaHei', 10),
                                    fg='#059669', bg='#f5f5f5')
        # Don't pack initially - will show when needed

        # Hidden log window (can be toggled)
        self.log_window = None

    def _animate_gradient(self):
        """Create animated gradient text effect"""
        if not hasattr(self, 'title_canvas') or not self.title_canvas.winfo_exists():
            return

        # Clear canvas
        self.title_canvas.delete('all')

        text = "AugmentCode-Free"

        # Get actual canvas dimensions for proper centering
        canvas_width = self.title_canvas.winfo_width()
        canvas_height = self.title_canvas.winfo_height()

        # If canvas hasn't been drawn yet, use default values
        if canvas_width <= 1:
            canvas_width = 380
        if canvas_height <= 1:
            canvas_height = 60

        # Use a simple approach - draw the full text with animated color
        import math

        # Create animated color based on time
        time_factor = self.gradient_offset * 0.1

        # Animated colors - cycling through rainbow-like effect
        r = int(127 + 127 * math.sin(time_factor))
        g = int(127 + 127 * math.sin(time_factor + 2))
        b = int(200 + 55 * math.sin(time_factor + 4))

        # Keep it in blue spectrum but animated
        r = max(70, min(150, r))
        g = max(70, min(150, g))
        b = max(200, min(255, b))

        color = f'#{r:02x}{g:02x}{b:02x}'

        # Draw the main text
        self.title_canvas.create_text(canvas_width//2, canvas_height//2,
                                     text=text, fill=color,
                                     font=('Microsoft YaHei', 18, 'bold'),
                                     anchor='center')

        # Update offset for next frame
        self.gradient_offset += 1
        if self.gradient_offset > 628:  # 2*pi*100 for smooth loop
            self.gradient_offset = 0

        # Schedule next animation frame
        self.root.after(100, self._animate_gradient)
    
    def toggle_log_window(self):
        """Toggle the log window visibility"""
        if self.log_window is None or not self.log_window.winfo_exists():
            self.create_log_window()
        else:
            self.log_window.destroy()
            self.log_window = None

    def create_log_window(self):
        """Create a separate log window"""
        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("操作日志")
        self.log_window.geometry("600x400")
        self.log_window.configure(bg='#f8f9fa')

        # Log text area
        log_frame = tk.Frame(self.log_window, bg='#f8f9fa')
        log_frame.pack(fill='both', expand=True, padx=20, pady=20)

        from tkinter import scrolledtext
        self.output_text = scrolledtext.ScrolledText(log_frame, height=20, width=70,
                                                    font=('Consolas', 9),
                                                    bg='#2c3e50', fg='#ecf0f1',
                                                    insertbackground='#ecf0f1')
        self.output_text.pack(fill='both', expand=True)

        # Clear button
        clear_btn = tk.Button(log_frame, text="清空日志", command=self.clear_output,
                             font=('Microsoft YaHei', 9), bg='#e74c3c', fg='white',
                             relief='flat', cursor='hand2', bd=0, pady=5)
        clear_btn.pack(pady=(10, 0))

    def setup_print_redirection(self):
        """Setup print function redirection to GUI"""
        # Store original print functions
        self.original_print_info = print_info
        self.original_print_success = print_success
        self.original_print_error = print_error
        self.original_print_warning = print_warning

        # Replace with GUI versions
        import augment_tools_core.common_utils as utils
        utils.print_info = self.gui_print_info
        utils.print_success = self.gui_print_success
        utils.print_error = self.gui_print_error
        utils.print_warning = self.gui_print_warning
    
    def gui_print_info(self, message):
        """GUI version of print_info"""
        self.message_queue.put(('info', message))
    
    def gui_print_success(self, message):
        """GUI version of print_success"""
        self.message_queue.put(('success', message))
    
    def gui_print_error(self, message):
        """GUI version of print_error"""
        self.message_queue.put(('error', message))
    
    def gui_print_warning(self, message):
        """GUI version of print_warning"""
        self.message_queue.put(('warning', message))
    
    def process_messages(self):
        """Process messages from the queue and update GUI"""
        try:
            while True:
                msg_type, message = self.message_queue.get_nowait()
                timestamp = time.strftime("%H:%M:%S")

                # Update status display (show temporarily)
                if msg_type == 'success':
                    self.show_status_message("✅ 操作完成", "#059669")
                elif msg_type == 'error':
                    self.show_status_message("❌ 操作失败", "#dc2626")
                elif msg_type == 'warning':
                    self.show_status_message("⚠️ 注意", "#d97706")
                else:
                    self.show_status_message("ℹ️ 处理中...", "#0ea5e9")

                # If log window exists, add to log
                if hasattr(self, 'output_text') and self.output_text.winfo_exists():
                    # Color coding for different message types
                    if msg_type == 'info':
                        formatted_msg = f"[{timestamp}] ℹ️ {message}\n"
                    elif msg_type == 'success':
                        formatted_msg = f"[{timestamp}] ✅ {message}\n"
                    elif msg_type == 'error':
                        formatted_msg = f"[{timestamp}] ❌ {message}\n"
                    elif msg_type == 'warning':
                        formatted_msg = f"[{timestamp}] ⚠️ {message}\n"
                    else:
                        formatted_msg = f"[{timestamp}] {message}\n"

                    self.output_text.insert(tk.END, formatted_msg)
                    self.output_text.see(tk.END)

        except queue.Empty:
            pass
        except tk.TclError:
            # Window might be destroyed
            pass

        # Schedule next check
        self.root.after(100, self.process_messages)

    def show_status_message(self, message, color):
        """Show status message temporarily"""
        self.status_var.set(message)
        self.status_label.config(fg=color)
        self.status_label.pack(pady=(10, 0))

        # Hide status after 3 seconds
        self.root.after(3000, self.hide_status_message)

    def hide_status_message(self):
        """Hide status message"""
        self.status_label.pack_forget()

    def clear_output(self):
        """Clear the output text area"""
        if hasattr(self, 'output_text') and self.output_text.winfo_exists():
            self.output_text.delete(1.0, tk.END)
    
    def set_buttons_state(self, state):
        """Enable or disable all buttons"""
        self.close_vscode_btn.config_state(state)
        self.clean_db_btn.config_state(state)
        self.modify_ids_btn.config_state(state)
        self.run_all_btn.config_state(state)

    def close_vscode_clicked(self):
        """Handle close VSCode button click"""
        # Show warning dialog
        result = show_warning(
            self.root,
            "关闭VSCode确认",
            "• 若有未保存的内容请先进行保存\n"
            "• Augment中需要备份的聊天记录请先备份\n\n"
            "确认无误后才能关闭VSCode。\n\n"
            "是否继续关闭VSCode？"
        )

        if not result:
            return

        self.set_buttons_state('disabled')
        self.status_var.set("正在关闭VSCode...")

        def close_task():
            try:
                self.gui_print_info("开始关闭VSCode进程")

                # Close VSCode processes
                if self._close_vscode_processes():
                    self.gui_print_success("VSCode已成功关闭")
                    self.root.after(0, lambda: self.show_status_message("✅ VSCode已关闭", "#059669"))
                else:
                    self.gui_print_warning("未找到运行中的VSCode进程")
                    self.root.after(0, lambda: self.show_status_message("ℹ️ VSCode未运行", "#0ea5e9"))

            except Exception as e:
                self.gui_print_error(f"关闭VSCode时发生错误: {str(e)}")
                self.root.after(0, lambda: self.show_status_message("❌ 关闭失败", "#dc2626"))
            finally:
                self.root.after(0, lambda: self.set_buttons_state('normal'))

        threading.Thread(target=close_task, daemon=True).start()

    def _close_vscode_processes(self):
        """Close all VSCode processes"""
        try:
            system = platform.system().lower()
            closed_any = False

            if system == "windows":
                # Windows: Close Code.exe processes
                result = subprocess.run(['taskkill', '/F', '/IM', 'Code.exe'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    closed_any = True
                    self.gui_print_info("已关闭VSCode主进程")

                # Also close any VSCode helper processes
                helper_processes = ['Code - Insiders.exe', 'Code - OSS.exe']
                for process in helper_processes:
                    subprocess.run(['taskkill', '/F', '/IM', process],
                                 capture_output=True, text=True)

            elif system == "darwin":  # macOS
                result = subprocess.run(['pkill', '-f', 'Visual Studio Code'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    closed_any = True
                    self.gui_print_info("已关闭VSCode进程")

            else:  # Linux
                result = subprocess.run(['pkill', '-f', 'code'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    closed_any = True
                    self.gui_print_info("已关闭VSCode进程")

            return closed_any

        except Exception as e:
            self.gui_print_error(f"关闭VSCode进程时出错: {str(e)}")
            return False

    def _is_vscode_running(self):
        """Check if VSCode is currently running"""
        try:
            system = platform.system().lower()

            if system == "windows":
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Code.exe'],
                                      capture_output=True, text=True)
                return 'Code.exe' in result.stdout

            elif system == "darwin":  # macOS
                result = subprocess.run(['pgrep', '-f', 'Visual Studio Code'],
                                      capture_output=True, text=True)
                return result.returncode == 0

            else:  # Linux
                result = subprocess.run(['pgrep', '-f', 'code'],
                                      capture_output=True, text=True)
                return result.returncode == 0

        except Exception:
            return False  # If we can't check, assume it's not running
    
    def clean_database_clicked(self):
        """Handle clean database button click"""
        # Check if VSCode is running
        if self._is_vscode_running():
            show_info(
                self.root,
                "VSCode正在运行",
                "检测到VSCode正在运行！\n\n"
                "请先关闭VSCode再进行数据库清理操作。\n"
                "您可以点击\"一键关闭VSCode\"按钮。"
            )
            return

        keyword = self.keyword_var.get().strip()  # Use default "augment"

        self.set_buttons_state('disabled')
        self.status_var.set("正在清理数据库...")

        def clean_task():
            try:
                self.gui_print_info(f"开始清理 VS Code 数据库 (关键字: '{keyword}')")
                paths = get_os_specific_vscode_paths()
                if not paths:
                    self.gui_print_error("无法确定您操作系统的 VS Code 路径。操作中止。")
                    return
                
                db_path_str = paths.get("state_db")
                if not db_path_str:
                    self.gui_print_error("在操作系统特定配置中未找到 VS Code state.vscdb 路径。操作中止。")
                    return
                
                db_path = Path(db_path_str)
                if not db_path.is_file():
                    self.gui_print_warning(f"数据库文件在预期位置不存在或不是文件: {db_path}")
                    self.gui_print_error("由于未找到数据库文件，中止数据库清理。")
                    return
                
                if clean_vscode_database(db_path, keyword):
                    self.gui_print_info("数据库清理过程完成。")
                    self.root.after(0, lambda: self.status_var.set("✅ 数据库清理已完成"))
                else:
                    self.gui_print_error("数据库清理过程报告错误。请检查之前的消息。")
                    self.root.after(0, lambda: self.status_var.set("❌ 数据库清理失败"))

            except Exception as e:
                self.gui_print_error(f"清理数据库时发生错误: {str(e)}")
                self.root.after(0, lambda: self.status_var.set("❌ 数据库清理失败"))
            finally:
                self.root.after(0, lambda: self.set_buttons_state('normal'))
        
        threading.Thread(target=clean_task, daemon=True).start()
    
    def modify_ids_clicked(self):
        """Handle modify IDs button click"""
        # Check if VSCode is running
        if self._is_vscode_running():
            show_info(
                self.root,
                "VSCode正在运行",
                "检测到VSCode正在运行！\n\n"
                "请先关闭VSCode再进行遥测ID修改操作。\n"
                "您可以点击\"一键关闭VSCode\"按钮。"
            )
            return

        self.set_buttons_state('disabled')
        self.status_var.set("正在修改遥测 ID...")

        def modify_task():
            try:
                self.gui_print_info("开始修改 VS Code 遥测 ID")
                paths = get_os_specific_vscode_paths()
                if not paths:
                    self.gui_print_error("无法确定您操作系统的 VS Code 路径。操作中止。")
                    return
                
                storage_path_str = paths.get("storage_json")
                if not storage_path_str:
                    self.gui_print_error("在操作系统特定配置中未找到 VS Code storage.json 路径。操作中止。")
                    return
                
                storage_path = Path(storage_path_str)
                if not storage_path.is_file():
                    self.gui_print_warning(f"存储文件在预期位置不存在或不是文件: {storage_path}")
                    self.gui_print_error("由于未找到存储文件，中止遥测 ID 修改。")
                    return
                
                if modify_vscode_telemetry_ids(storage_path):
                    self.gui_print_info("遥测 ID 修改过程完成。")
                    self.root.after(0, lambda: self.status_var.set("✅ 遥测 ID 修改已完成"))
                else:
                    self.gui_print_error("遥测 ID 修改过程报告错误。请检查之前的消息。")
                    self.root.after(0, lambda: self.status_var.set("❌ 遥测 ID 修改失败"))

            except Exception as e:
                self.gui_print_error(f"修改遥测 ID 时发生错误: {str(e)}")
                self.root.after(0, lambda: self.status_var.set("❌ 遥测 ID 修改失败"))
            finally:
                self.root.after(0, lambda: self.set_buttons_state('normal'))
        
        threading.Thread(target=modify_task, daemon=True).start()

    def login_aug_clicked(self):
        """Handle login button click"""
        import base64
        import uuid
        import hashlib
        import webbrowser
        from urllib.parse import urlencode
        code_verifier = base64.urlsafe_b64encode(hashlib.sha256(uuid.uuid4().bytes).digest()).decode('utf-8').replace('=', '')
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode('utf-8').replace('=', '')
        state = str(uuid.uuid4())
        # 构造授权 URL
        params = {
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "client_id": "augment-vscode-extension",
            "redirect_uri": "vscode://augment.vscode-augment/auth/result",
            "state": state,
            "scope": "email",
            "prompt": "login"
        }
        auth_url = f"https://auth.augmentcode.com/authorize?{urlencode(params)}"
        webbrowser.open(auth_url)


    def run_all_clicked(self):
        """Handle run all tools button click - 一键修改"""
        # Show special warning for this operation
        result = show_warning(
            self.root,
            "一键修改确认",
            "此按钮会关闭VSCode并清除Augment聊天数据！\n\n"
            "请确保：\n"
            "• 文件已保存\n"
            "• Augment中的重要聊天记录已备份\n\n"
            "是否继续执行一键修改？"
        )

        if not result:
            return

        keyword = self.keyword_var.get().strip()  # Use default "augment"

        self.set_buttons_state('disabled')
        self.status_var.set("正在执行一键修改...")

        def run_all_task():
            try:
                self.gui_print_info("开始执行一键修改操作")

                # Step 0: Close VSCode first
                self.gui_print_info("--- 步骤 0: 关闭VSCode ---")
                if self._is_vscode_running():
                    if self._close_vscode_processes():
                        self.gui_print_success("VSCode已关闭")
                    else:
                        self.gui_print_warning("关闭VSCode时出现问题，继续执行后续步骤")
                else:
                    self.gui_print_info("VSCode未运行，跳过关闭步骤")
                
                # Step 1: Clean database
                self.gui_print_info("--- 步骤 1: 数据库清理 ---")
                try:
                    paths = get_os_specific_vscode_paths()
                    if paths:
                        db_path_str = paths.get("state_db")
                        if db_path_str:
                            db_path = Path(db_path_str)
                            if db_path.is_file():
                                clean_vscode_database(db_path, keyword)
                            else:
                                self.gui_print_warning("数据库文件未找到，跳过数据库清理")
                        else:
                            self.gui_print_warning("数据库路径未找到，跳过数据库清理")
                    else:
                        self.gui_print_warning("无法确定 VS Code 路径，跳过数据库清理")
                except Exception as e:
                    self.gui_print_error(f"数据库清理步骤中发生错误: {e}")
                    self.gui_print_warning("尽管出现错误，仍继续下一步。")
                
                # Step 2: Modify telemetry IDs
                self.gui_print_info("--- 步骤 2: 遥测 ID 修改 ---")
                try:
                    paths = get_os_specific_vscode_paths()
                    if paths:
                        storage_path_str = paths.get("storage_json")
                        if storage_path_str:
                            storage_path = Path(storage_path_str)
                            if storage_path.is_file():
                                modify_vscode_telemetry_ids(storage_path)
                            else:
                                self.gui_print_warning("存储文件未找到，跳过遥测 ID 修改")
                        else:
                            self.gui_print_warning("存储文件路径未找到，跳过遥测 ID 修改")
                    else:
                        self.gui_print_warning("无法确定 VS Code 路径，跳过遥测 ID 修改")
                except Exception as e:
                    self.gui_print_error(f"遥测 ID 修改步骤中发生错误: {e}")
                
                self.gui_print_success("所有工具已完成执行序列。")
                self.root.after(0, lambda: self.status_var.set("✅ 所有工具执行已完成"))

            except Exception as e:
                self.gui_print_error(f"运行所有工具时发生错误: {str(e)}")
                self.root.after(0, lambda: self.status_var.set("❌ 工具执行失败"))
            finally:
                self.root.after(0, lambda: self.set_buttons_state('normal'))
        
        threading.Thread(target=run_all_task, daemon=True).start()


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    AugmentToolsGUI(root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("应用程序被用户中断")
        sys.exit(0)


if __name__ == "__main__":
    main()
