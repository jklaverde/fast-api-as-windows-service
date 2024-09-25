import uvicorn
from fastapi import FastAPI
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import threading

# Define the FastAPI app
app = FastAPI()

# Define a simple "Hello World" route
@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

class FastAPIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FastAPIService"
    _svc_display_name_ = "FastAPI Windows Service"
    _svc_description_ = "Service running FastAPI app"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        # Start the FastAPI app in a new thread to avoid blocking the service
        uvicorn_thread = threading.Thread(target=self.run_uvicorn)
        uvicorn_thread.start()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def run_uvicorn(self):
        # Run the FastAPI app using uvicorn
        uvicorn.run(app, host="0.0.0.0", port=14000)

# Run the service
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FastAPIService)
