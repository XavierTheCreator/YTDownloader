"""
Youtube downloader version 0.02

Plans for 0.03
- Allow for users to select the quality of the video. 
- Make a seperate screen that monitors downloads
- Catch exception when no URL is specified or if not a url make a pop message 
  
"""
from PySimpleGUI import FileBrowse, FolderBrowse
from pytube import YouTube
import PySimpleGUI as sg
import threading
import time

sg.theme('TanBlue')
done = False
title = ''


def download_thread(url,filepath):
    global done, title

    yt = YouTube(url)
    stream = yt.streams.first()
    stream.download(filepath)
    title = yt.title
    done = True



if __name__ == '__main__':

    layout = [[sg.Text('URL', size=(15, 1)), sg.InputText(k='-URL-')],
            [sg.Text('Download Folder',size=(15,1)),sg.InputText(k='-FOLDER-'),FolderBrowse(button_text="Browse")],  
            [sg.Text(size=(50, 2), key='-OUTPUT-')],
            [sg.Button('Download'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('Youtube Downloader', layout)

    # Event Loop
    while True:
        event, values = window.read()

        # Waiting for quit press
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Download':
            done = False
            thread = threading.Thread(target=download_thread, args=(values['-URL-'],values['-FOLDER-']), daemon=True)
            thread.start()

        while not done:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'Downloading', time_between_frames=30)
            time.sleep(.3)

        sg.popup_animated(image_source=None)

        window['-OUTPUT-'].update(title + '\nis finished downloading')

    # Finish up by removing from the screen
    window.close()
