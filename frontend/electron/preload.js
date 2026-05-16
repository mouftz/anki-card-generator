const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  onScreenshot: (callback) => {
    ipcRenderer.on('screenshot-captured', (event, base64) => callback(base64));
  },
  generateCard: (imageBase64, reason) => {
    return ipcRenderer.invoke('generate-card', { imageBase64, reason });
  },
  hidePopup: () => {
    ipcRenderer.send('hide-popup');
  }
});