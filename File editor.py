# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 13:36:43 2024

@author: sayan
"""

#The original code can be found at: https://thepythoncode.com/code/create-rich-text-editor-with-tkinter-python

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import ctypes
from functools import partial
from json import loads, dumps



def rgbToHex(rgb):
    
    """
    Convert an RGB tuple to a hexadecimal color string.

    Args:
        rgb (tuple): A tuple containing three integers (r, g, b), 
                     each ranging from 0 to 255, representing the 
                     red, green, and blue components of a color.

    Returns:
        str: A string representing the color in hexadecimal format,
             starting with a '#' followed by six hexadecimal digits.
    """
    hex="#%02x%02x%02x" % rgb 
    return hex




def fileManager(event=None, action=None):
    """
    Manage file operations such as opening and saving files.

    Args:
        event (tkinter.Event, optional): The event that triggered the file manager.
        action (str, optional): The action to be performed, either 'open' or 'save'.

    Returns:
        None

    Description:
        - 'open': Opens a file dialog to select a file to open, reads its content, and loads it into the text area. It also resets and re-applies any tags found in the file.
        - 'save': Saves the current content of the text area to a file. If the file path is not specified, it prompts the user to choose a save location and file name.

    Notes:
        - This function uses global variables `document` and `filePath`.
        - It assumes the existence of other global variables and functions such as `validFileTypes`, `initialdir`, `textArea`, `root`, `applicationName`, `resetTags`, and `defaultContent`.
    """
    
    global document, filePath

    match action:
    
        case 'open':
        
            filePath = askopenfilename(filetypes=validFileTypes, initialdir=initialdir)

            f= open(filePath, 'r')
            document = loads(f.read())
            textArea.delete('1.0', END)
            textArea.insert('1.0', document['content'])
            root.title('{} - {}'.format(applicationName,filePath))
    
            # Reset all tags
            resetTags()
            for tagName in document['tags']:
                for tagStart, tagEnd in document['tags'][tagName]:
                    textArea.tag_add(tagName, tagStart, tagEnd)

        case 'save':
            document = defaultContent
            document['content'] = textArea.get('1.0', END)

            for tagName in textArea.tag_names():
                if tagName == 'sel': 
                    continue
    
                document['tags'][tagName] = []
                ranges = textArea.tag_ranges(tagName)
                for i, tagRange in enumerate(ranges[::2]):
                    document['tags'][tagName].append([str(tagRange), str(ranges[i+1])])

            if not filepath:
                # ask the user for a filename with the native file explorer.
                newfilePath = asksaveasfilename(filetypes=validFileTypes, initialdir=initialdir)
        
                if newfilePath is None: 
                    return
    
                filePath = newfilePath
    
            if not filePath.endswith('.rte'):
                filePath += '.rte'
    
            f=open(filePath, 'w')
            print('Saving at: ', filePath)  
            f.write(dumps(document))
    
            root.title('{} - {}'.format(applicationName,filePath))


def resetTags():
    """
    Reset and reconfigure text tags in the text area.

    This function performs two main tasks:
    1. Removes all existing tags from the text area.
    2. Reconfigures the text area with a predefined set of tags.

    Args:
        None

    Returns:
        None

    Notes:
        - This function assumes the existence of a global `textArea` widget.
        - It also assumes the presence of a global `tagTypes` dictionary, where keys are tag names and values are their configurations.
    """
    for tag in textArea.tag_names():
        textArea.tag_remove(tag, "1.0", "end")

    for tagType in tagTypes:
        textArea.tag_configure(tagType.lower(), tagTypes[tagType])


def keyDown(event=None):
    """
    Update the window title to indicate unsaved changes.

    Args:
        event (tkinter.Event, optional): The event that triggered this function.

    Returns:
        None

    Description:
        This function updates the title of the root window to indicate that the current document has unsaved changes by adding an asterisk (*) before the file path.

    Notes:
        - This function assumes the existence of global variables `root`, `applicationName`, and `filePath`.
    """
    root.title('{} - *{}'.format(applicationName,filePath))


def tagToggle(tagName):
    """
    Toggle a text tag on the currently selected text.

    Args:
        tagName (str): The name of the tag to toggle.

    Returns:
        None

    Description:
        This function toggles a tag on the text currently selected in the text area. If the selected text already has the specified tag, the tag is removed. Otherwise, the tag is added to the selected text.

    Notes:
        - This function assumes the existence of a global `textArea` widget.
        - The selection range is determined by the text widget's "sel.first" and "sel.last" indices.
        - This function requires that there is a text selection; otherwise, it may raise an error.
    """
    start, end = "sel.first", "sel.last"

    if tagName in textArea.tag_names('sel.first'):
        textArea.tag_remove(tagName, start, end)
    else:
        textArea.tag_add(tagName, start, end)




if __name__ == '__main__':
   
    """
    Initialize the application when the script is executed directly.

    This block of code sets up the application window, defines global variables, and creates the main menu and text area.

    Notes:
        - This block is executed only when the script is run directly, not when it's imported as a module.
        - It ensures that the application is properly initialized and ready to use.
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    
    # Setup
    root = Tk()
    applicationName = 'Rich Text Editor'
    root.title(applicationName)
    
    #Initialize required variables
    filePath = None
    initialdir = '.'
    validFileTypes = (
        ("Rich Text File","*.rte"),
        ("all files","*.*")
    )
    
    fontName = 'Bahnschrift'
    padding = 60
    
    document = None
    
    # Default content of the File
    defaultContent = {
        "content": "",
        "tags": {
            'bold': [(), ()]
        },
    }
    #Pre-defined font options
    tagTypes = {
        
        'Bold': {'font': '{} 15 bold'.format(fontName)},
        'Italic': {'font': '{} 15 italic'.format(fontName)},
        'Code': {'font': 'Consolas 15', 'background': rgbToHex((200, 200, 200))},
    
        
        'Normal Size': {'font': '{} 15'.format(fontName)},
        'Larger Size': {'font': '{} 25'.format(fontName)},
        'Largest Size': {'font': '{} 35'.format(fontName)},
    
        
        'Highlight': {'background': rgbToHex((255, 255, 0))},
        'Highlight Red': {'background': rgbToHex((255, 0, 0))},
        'Highlight Green': {'background': rgbToHex((0, 255, 0))},
        'Highlight Black': {'background': rgbToHex((0, 0, 0))},
    
    
        'Text White': {'foreground': rgbToHex((255, 255, 255))},
        'Text Grey': {'foreground': rgbToHex((200, 200, 200))},
        'Text Blue': {'foreground': rgbToHex((0, 0, 255))},
        'Text green': {'foreground': rgbToHex((0, 255, 0))},
        'Text Red': {'foreground': rgbToHex((255, 0, 0))},
    }
    
    textArea = Text(root, font='{} 15'.format(fontName), relief=FLAT)
    textArea.pack(fill=BOTH, expand=TRUE, padx=padding, pady=padding)
    textArea.bind("<Key>", keyDown)
    
    resetTags()
    
    
    menu = Menu(root)
    root.config(menu=menu)
    
    fileMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=fileMenu)
    
    fileMenu.add_command(label="Open", command=partial(fileManager, action='open'), accelerator='Ctrl+O')
    root.bind_all('<Control-o>', partial(fileManager, action='open'))
    
    fileMenu.add_command(label="Save", command=partial(fileManager, action='save'), accelerator='Ctrl+S')
    root.bind_all('<Control-s>', partial(fileManager, action='save'))
    
    fileMenu.add_command(label="Exit", command=root.quit)
    
    
    formatMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Format", menu=formatMenu)
    
    for tagType in tagTypes:
        formatMenu.add_command(label=tagType, command=partial(tagToggle, tagName=tagType.lower()))
    
    
    root.mainloop()