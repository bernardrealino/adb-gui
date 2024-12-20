import flet as ft
import subprocess

def run_adb_command(command):
    """Run an ADB command and return its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def main(page: ft.Page):
    page.title = "Android Remote Control"
    page.window_width = 1920
    page.window_height = 1080
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # ADB Status
    adb_status = ft.Text(value="ADB Status: Disconnected", color="red", size=18)
    connected_ip = ft.Text(value="Connected IP: None", size=16)

    def check_adb_connection():
        output = run_adb_command("adb devices")
        if "device" in output:
            adb_status.value = "ADB Status: Connected"
            adb_status.color = "green"
            lines = output.split("\n")
            for line in lines:
                if "device" in line and not line.startswith("List"):
                    connected_ip.value = f"Connected IP: {line.split()[0]}"
                    break
        else:
            adb_status.value = "ADB Status: Disconnected"
            adb_status.color = "red"
            connected_ip.value = "Connected IP: None"
        page.update()

    # IP Connection
    ip_input = ft.TextField(label="Device IP Address", width=300, autofocus=True)

    def connect_to_device(event):
        if ip_input.value:
            output = run_adb_command(f"adb connect {ip_input.value}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Connection Output: {output}"))
            page.snack_bar.open = True
            check_adb_connection()

    # Key Event Handler
    def handle_button_click(event):
        key_event = event.control.data
        output = run_adb_command(f"adb shell input keyevent {key_event}")
        log_area.value += f"Sent Key Event: {key_event}\n"
        page.update()

    # File Transfer
    file_path_input = ft.TextField(label="File Path (PC)", width=400)
    remote_path_input = ft.TextField(label="Remote Path (Device)", width=400)

    def upload_file(event):
        output = run_adb_command(f"adb push {file_path_input.value} {remote_path_input.value}")
        log_area.value += f"Upload Output: {output}\n"
        page.update()

    def download_file(event):
        output = run_adb_command(f"adb pull {remote_path_input.value} {file_path_input.value}")
        log_area.value += f"Download Output: {output}\n"
        page.update()

    # Custom Command Input
    custom_command = ft.TextField(label="Custom ADB Command", width=600)

    def send_custom_command(event):
        output = run_adb_command(custom_command.value)
        log_area.value += f"Custom Command Output: {output}\n"
        page.update()

    # Log Area
    log_area = ft.TextField(value="", multiline=True, read_only=True, expand=True)

    # Layout
    page.add(
        ft.Column([
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("ADB Connection", size=20, weight="bold"),
                            adb_status,
                            connected_ip,
                            ft.ElevatedButton("Check ADB Connection", on_click=lambda _: check_adb_connection()),
                            ft.Divider(),
                            ft.Text("Connect via IP", size=18),
                            ip_input,
                            ft.ElevatedButton("Connect", on_click=connect_to_device),
                        ], spacing=10),
                        padding=20,
                    ),
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Remote Navigation Controls", size=20, weight="bold"),
                            # ft.ElevatedButton("Up", data="19", on_click=handle_button_click),
                            ft.IconButton(icon = ft.icons.ARROW_UPWARD, data="19", on_click=handle_button_click),
                            ft.Row([
                                # ft.ElevatedButton("Left", data="21", on_click=handle_button_click),
                                ft.IconButton(icon = ft.icons.ARROW_BACK, data="21", on_click=handle_button_click),
                                ft.ElevatedButton("OK", data="23", on_click=handle_button_click),
                                # ft.ElevatedButton("Right", data="22", on_click=handle_button_click),
                                ft.IconButton(icon = ft.icons.ARROW_FORWARD, data="22", on_click=handle_button_click),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            # ft.ElevatedButton("Down", data="20", on_click=handle_button_click),
                                ft.IconButton(icon = ft.icons.ARROW_DOWNWARD, data="20", on_click=handle_button_click),
                            ft.Row([
                                # ft.ElevatedButton("Menu", data="82", on_click=handle_button_click),
                                ft.IconButton(icon = ft.icons.MENU, data="82", on_click=handle_button_click),
                                # ft.ElevatedButton("Home", data="3", on_click=handle_button_click),
                                ft.IconButton(icon = ft.icons.HOME, data="3", on_click=handle_button_click),
                                # ft.ElevatedButton(icon=ft.icons.ARROW_BACK, data="4", on_click=handle_button_click),
                                ft.IconButton(icon = ft.icons.ARROW_BACK, data="4", on_click=handle_button_click)
                            ], spacing=10),
                            ft.Row([], spacing=10),
                        ], spacing=10, horizontal_alignment= ft.CrossAxisAlignment.CENTER),
                        padding=20,
                    ),
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),

            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("File Transfer", size=20, weight="bold"),
                            file_path_input,
                            remote_path_input,
                            ft.Row([
                                ft.ElevatedButton("Upload to Device", on_click=upload_file),
                                ft.ElevatedButton("Download from Device", on_click=download_file),
                            ], spacing=10),
                        ], spacing=10),
                        padding=20,
                    ),
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Custom ADB Command", size=20, weight="bold"),
                            custom_command,
                            ft.ElevatedButton("Execute Command", on_click=send_custom_command),
                        ], spacing=10),
                        padding=20,
                    ),
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),

            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Logs", size=20, weight="bold"),
                        log_area,
                    ], spacing=10),
                    padding=20,
                    expand=True,
                ),
            ),
        ], spacing=20)
    )

# Run the Flet app
ft.app(target=main)
