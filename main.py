#!/usr/bin/env python3
import tkinter as tk, os
from tkinter import simpledialog as sd, filedialog as fd, messagebox as mb
from http.server import SimpleHTTPRequestHandler as Handler
from socketserver import TCPServer as serve
from threading import Thread
from webbrowser import open as c
import socket

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

display = tk.Tk()
display.title("Server")
display.geometry("400x600")
display.resizable(False, False)

root = tk.Frame(display, bg="orange")
root.pack(fill=tk.BOTH)

lbl = tk.Label(root, text="Welcome to Server - Hosts files", bg="pink", font=('TkFixedFont', 15))
lbl.pack(fill=tk.BOTH)

lbl2 = tk.Label(root, text="Configurations", bg="white", highlightthickness=6.25)
lbl2.pack(fill=tk.BOTH)

file_path = os.getcwd()
filelbl = tk.Label(root, text=f"Hosting path: {file_path}", bg="orange")
filelbl.pack()
def change_fl():
    global file_path, filelbl
    file_path = fd.askdirectory(title="Select folder to host", initialdir=file_path) or file_path
    filelbl["text"] = f"Hosting path: {file_path}"
    os.chdir(file_path)
   
btn1 = tk.Button(root, text="Choose another folder", command=change_fl, bg="yellow")
btn1.pack()

port = 8080
portlbl = tk.Label(root, text=f"Port: {port}", bg="orange")
portlbl.pack()
def change_port():
    global port, portlbl
    port = sd.askinteger("Select port", "Enter port number", minvalue=1024, maxvalue=65535, parent=root) or port
    portlbl["text"] = f"Port: {port}"
   
btn2 = tk.Button(root, text="Choose another port", command=change_port, bg="yellow")
btn2.pack()

def start():
    global btn2, btn1, btn3, btn4, btn5
    btn1["state"] = "disabled"
    btn2['state'] = 'disabled'
    btn3['state'] = 'disabled'
    btn4['state'] = 'normal'
    btn5['state'] = 'normal'
    server()

threaded = False
thread = None

def always():
    global threaded, thread
    threaded = True
    thread = Thread(target=start, daemon=True)
    thread.start()

control = tk.Frame(display, bg="blue")
lbl1 = tk.Label(display, text="Controling", bg="white", highlightthickness=6.25)
lbl1.pack(fill=tk.BOTH)

btn3 = tk.Button(control, text="Start", command=always, bg="green")
btn3.pack(fill=tk.BOTH)
btn4 = tk.Button(control, text="Stop", state='disabled', bg="red")
btn4.pack(fill=tk.BOTH)
control.pack(fill=tk.BOTH)
btn5 = tk.Button(control, state="disabled", text=f"Open in browser", bg="blue", command=lambda: c(f"http://{getIP()}:{port}"))
btn5.pack(fill=tk.BOTH)
btn6 = tk.Button(control, bg="purple", text="Get IP address", command=lambda: mb.showinfo("IP information", f"IP address: {getIP()}\nOpen to browser: http://{getIP()}:{port}/"))
btn6.pack(fill=tk.BOTH)

tk.Label(display, text="Logs", bg="white", highlightthickness=6.25).pack(fill=tk.BOTH)

def texter(obj, text, to=tk.END, end="\n"):
    obj["state"] = "normal"
    obj.insert(to, text + end)
    obj['state'] = 'disabled'
    obj.see(tk.END)

def clearme(obj):
	obj["state"] = "normal"
	obj.delete(0.0, tk.END)
	obj["state"] = "disabled"

btn7 = tk.Button(display, text="Clear log", bg="grey")
btn7.pack(fill=tk.BOTH)

log_frame = tk.Frame(display)
log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

text = tk.Text(log_frame, bg="cyan", fg="black", wrap="word")

scrollbar = tk.Scrollbar(log_frame, command=text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scrollbar.set)

btn7["command"] = lambda: clearme(text)
text.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

logdo = lambda t: texter(text, t)

class TextHandler(Handler):
    def log_message(self, format, *args):
        message = format % args
        logdo("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          message.translate(self._control_char_table)))

class Serve(serve):
    allow_reuse_address = True
    allow_reuse_port = True

def server():
    global btn4, btn3, btn2, btn1, btn5
    httpd = None
    try:
     with Serve(("", port), TextHandler) as httpd:
        def stop():
            btn1['state'] = 'normal'
            btn2['state'] = 'normal'
            btn3['state'] = 'normal'
            btn4['state'] = 'disabled'
            btn5['state'] = 'disabled'
            httpd.socket.close()
            httpd.shutdown()
            httpd.server_close()
        btn4["command"] = stop
        httpd.serve_forever()
    except OSError as e:
            btn1['state'] = 'normal'
            btn2['state'] = 'normal'
            btn3['state'] = 'normal'
            btn4['state'] = 'disabled'
            btn5['state'] = 'disabled'
            mb.showerror("Port used", f"Port alredy in use! Error detail:\nOSError: {e}")
    finally:
        if httpd:
            httpd.socket.close()
            httpd.server_close()

display.mainloop()
