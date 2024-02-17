const { app, BrowserWindow } = require("electron");
const { spawn } = require('node:child_process');
const path = require("path");

function createWindow() {
  var python = require('child_process').spawn('py', ['../../app-flask/app_files_memory.py']); 
  python.stdout.on('data', function (data) { 
    console.log("data: ", data.toString('utf8')); 
  }); 
  python.stderr.on('data', (data) => { 
    console.log(`stderr: ${data}`); // при ошибке 
  });
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
  });

  win.loadFile("dist/index.html");
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
