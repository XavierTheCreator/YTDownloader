"""
Youtube downloader version 0.03

Plans for 0.03
- Allow for users to select the quality of the video.  DONE
- Catch exception when no URL is specified or if not a url print a message DONE


Plans for 0.04
- Make a seperate screen that monitors downloads
- Allow users to download multiple videos at once 

"""


from PySimpleGUI import FileBrowse, FolderBrowse
from pytube import YouTube
import PySimpleGUI as sg
import threading
import time
from pytube import streams

sg.theme('TanBlue')
done = False
title = ''
streams = None

def download_thread(url,filepath) :
    global done, title
    yt = YouTube(url)       

    stream = yt.streams.first()
    stream.download(filepath)
    title = yt.title

    stream.download()
    done = True

   


def get_quality(url):
    yt = YouTube(url)

    streams = yt.streams.all()

    layout = [[sg.T('Choose Streams')]]
    for i ,s in enumerate(streams):
        layout += [[sg.CB(str(s),k=i)]]

    layout += [[sg.Ok(), sg.Cancel()]]
    event, values = sg.Window('Choose Stream', layout).read(close=True)
    choices = [k for k in values if values[k]]
    if not choices:
        sg.popup_error('Must choose stream')
        exit()
    else:
        print(f'You chose {choices[0]}')
        print(streams[choices[0]])

    return streams[choices[0]]




if __name__ == '__main__':

    #add drop list to select how many videos user wants to download
    # make an if statement to refresh window based on how many videos users want to download
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
             
            try:
                stream = get_quality(values['-URL-'])

                done = False
                thread = threading.Thread(target=download_thread, args=(values['-URL-'],values['-FOLDER-']), daemon=True)
                thread.start()
                
            except:
                done = True
                print("Exception")
                sg.popup_error("PLEASE A YOUTUBE URL")
        


        while not done:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'Downloading', time_between_frames=30)
            time.sleep(.3)
            sg.popup_animated(image_source=None)
            window['-OUTPUT-'].update(title + '\nis finished downloading')
            
        window.refresh()

    # Finish up by removing from the screen
    window.close()
