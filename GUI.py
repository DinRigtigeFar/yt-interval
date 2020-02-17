#!/usr/local/bin/python

#import PySimpleGUI as sg
import ParseInput

def gui_popup():
    """
    Create a GUI window to input path and text
    """
    # The layout
    layout = [[sg.Text('I will download the videos to this folder:')],
                [sg.Input(), sg.FolderBrowse()],
                [sg.Text('Paste your copied text here:')],
                [sg.Multiline(size=(45, 20))],
                [sg.Checkbox('Download pictures too', default=True), sg.Checkbox('Save interval file', default=False)],
                [sg.OK(), sg.Quit()],
                [sg.Text('Created by Christian Hviid Friis')]]

    # The window: Title and look
    window = sg.Window('PTP', layout, resizable=False)

    # Read window and save to two variables. Values contains path to download
    event, values = window.read()
    window.close()

    list_of_input = values[1].split("\n")

    # Apply my script to the paths
    try:
        # Parse the input. Contains two return values: YT and Pics
        parser_out = ParseInput.parser(list_of_input)
        # Input for the yt download functions
        input_for_funcs = ParseInput.make_time(parser_out[0])
        ParseInput.download_interval(input_for_funcs[0], values[0])
        ParseInput.download_whole(input_for_funcs[1], values[0])
        # If you want to download jpg's
        if values[2]:
            ParseInput.download_pics(parser_out[1], values[0])
        # If you want to save the interval list made by make_time
        if values[3]:
            ParseInput.save_link_time(input_for_funcs[0], values[0])
    except FileNotFoundError as FNFE:
        print(f"{FNFE}")


def done_cya():
    """
    Create a window to say the program is done
    """
    # Layout
    layout = [[sg.Text('All done')],
              [sg.Quit()]]

    # Make window
    window = sg.Window('Program finished').Layout(layout)

    # Open window
    window.Read()
    # Close window
    window.close()


# Call the functions
if __name__ == "__main__":
    try:
        gui_popup()
        done_cya()
    except Exception as E:
        with open('/Users/christian/Desktop/log.txt', 'a') as f:
            f.write(f'Error: {E}\n')

