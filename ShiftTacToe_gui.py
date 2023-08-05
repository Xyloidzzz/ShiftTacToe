###########################################################################
# File: ShiftTacToe_gui.py
# Author: Tim Wylie
# Date: 7/2023
# Description: A gui interface to play the game built with pysimplegui. On
#   the back end it uses tkinter, so it's a little janky. The code is not
#   clean at all, It's functional though.
#   Has a game mode allowing any number of players.
###########################################################################



import ShiftTacToe as stt
import pickle
import PySimpleGUI as sg
from pathlib import Path
import random

#default to shift-tac-toe as connect-4 with shifts
rows = 6
cols = 7
shift = 2
initshift = 1
b  = stt.ShiftTacToe(int(rows),int(cols),int(shift),int(initshift))

#drawing constants used
tilesize = 70
gridsize = 12

sg.theme('Dark Grey 15')

#game mode just auto changes colors between k people
playinggame = False
gamemode=False
numplayers = 2 #1 based
currplayer = 1 #1 based
#################### layout #############################

menu = [['&File', ['&Open', '&Save', '---', 'Game Mode', '---' ,'E&xit']],   
        #['&Game', ['Game Mode','Set']],
        ['&Help', ['Options', '&About...']],]



#graph canvas
graphpn = sg.Graph(canvas_size=(tilesize*(cols+shift*2),tilesize*rows), graph_top_right=(tilesize*(cols+shift*2),0), graph_bottom_left=(0,tilesize*rows), background_color='#333333', enable_events=True, drag_submits = True, key='graph_el', expand_y=True, expand_x=True)
    
graphcol = [
    [graphpn] 
]


#parts of the side pane
boardopts = [
[sg.Text('Rows'), sg.Input(rows, size=(3, 1), key='rowspin_el')], [sg.Text('Cols'), sg.Input(cols, size=(3, 1), key='colspin_el')],    [sg.Text('Shift'), sg.Input(shift, size=(3, 1), key='shiftspin_el')],
[sg.Text('Initial Shift'), sg.Combo(default_value=initshift, values = [i for i in range(shift+1)], key='shiftinit_el', readonly=True)],
]

initcolors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF','#000000','#777777']

pieceopts = [
    [sg.Text('Color'), sg.Combo(default_value='#FF0000',values=initcolors,enable_events=True, key='color_el',size=(10,1))],
    #sg.Input('#FF0000', size=(7, 1), key='color_el')],
    [sg.Text('Size'), sg.Input(tilesize, size=(3, 1), key='size_el')],
     [sg.Graph(canvas_size=(50,50), graph_top_right=(tilesize,0), graph_bottom_left=(0,tilesize), background_color='#FF0000',  key='colorg_el')],
     [sg.Text('Grid'), sg.Input(gridsize, size=(3, 1), key='grid_el')]
]

gameopts = [
    [sg.Text('Players'), sg.Input(2, size=(3, 1), key='numplays_el')],
    #[sg.Text('Colors'), sg.Combo(default_value='#FF0000',values=['#FF0000','#0000FF'],enable_events=True, key='player_cols',size=(10,1))],
    #sg.Input('#FF0000', size=(7, 1), key='color_el')],
]

#options side pain
side_pane = [
    [sg.Frame('Board Options', boardopts, expand_x = True)],
    [sg.Button('Update', key='update_btn')],
    [sg.Frame('Tile Options', pieceopts, expand_x = True)],
    [sg.Button('Change', key='change_btn')],
    [sg.Frame('Game Options', gameopts, expand_x = True, visible = False, key='game_frm')],
    [sg.Button('Start', key='game_btn', visible = False)],
]


#main layout with menu and two columns
layout = [[sg.Menu(menu)],
    #[sg.Text("Shift-Tac-Toe")],
    [ sg.Column(graphcol,vertical_alignment='top',expand_y=True, expand_x=True),
     sg.VerticalSeparator(),
sg.Column(side_pane,vertical_alignment='top', expand_y=True, expand_x=True, key='side_col')]

]

#################### main #############################

if __name__ == '__main__':
    #print('Welcome to Shift-Tac-Toe')
    

    # Create the window
    window = sg.Window("Shift-Tac-Toe", layout, finalize=True, resizable = True, icon="./stt_logo.png")
    #indicates when to draw the board
    refresh = True
    
    #main event loop
    while True:
        
        #################### draw board #############################
        #drawing the board when needed
        if refresh:
            window['graph_el'].erase()
            offset = tilesize*shift
            #draw board
            sm = .05*tilesize
            for rowidx, pos in enumerate(b.POSITIONS):
                for c in range(cols + shift):
                    tl = (offset - pos*tilesize + c*tilesize, rowidx*tilesize + sm)
                    br = (offset - pos*tilesize + tilesize + c*tilesize, rowidx*tilesize + tilesize - sm)
                    graphpn.draw_rectangle( tl, br, fill_color='white', line_color='black', line_width=1)
           
            #draw pieces
            for r in range(rows):
                for c in range(cols):
                    if b.BOARD[r][c] != b.EMPTYSPOT:
                        cen = (tilesize*shift + tilesize/2. + tilesize*c,
                            tilesize/2. + tilesize*r)
                        graphpn.draw_circle(cen, .9*tilesize/2., fill_color = b.BOARD[r][c], line_color = "black", line_width = 1)
            
            #draw board cols
            for i in range(cols+1):
                graphpn.draw_line((offset + i*tilesize,0), (offset + i*tilesize, tilesize*(rows)), color='#000077', width=gridsize)
            for i in range(rows+1):
                graphpn.draw_line((offset,i*tilesize), (offset + cols*tilesize, i*tilesize), color='#000077', width=gridsize)
            
            #b.ToString()
            refresh = False    
        
        #################### handle events #############################
        event, values = window.read()
        #event loop
        # End program if user closes window or
        # presses the OK button
        if event in ('EXIT', 'Exit', sg.WIN_CLOSED):
            break
        #about
        elif event == 'About...':
            layoutf = [[sg.Text("Shift-Tac-Toe Simulator \nTim Wylie \nVersion 0.6, 2023")], [sg.Button("Ok")]]
            window1 = sg.Window("About", layoutf, modal=True)
            while True:
                event, values = window1.read()
                if event == sg.WINDOW_CLOSED:
                    break
                elif event == "Ok":
                    break
            window1.close()
        #open
        elif event == 'Open':
            layoutf = [[sg.Text("Select file")], [sg.Input(key='-IN1-'),sg.FilesBrowse('Select')],[sg.Button("Ok")]]
            window1 = sg.Window("File Select", layoutf, modal=True)
            while True:
                event, values = window1.read()
                if event == sg.WINDOW_CLOSED:
                    break
                elif event == "Ok":
                    filename = values['-IN1-']
                    if Path(filename).is_file():
                        try:
                            with open(filename, "rb") as pf:
                                data = pickle.load(pf)
                                b = data['board']
                                rows = data['rows']
                                cols = data['cols']
                                shift = data['shift']
                                pf.close()
                                refresh=True
                                #window['c'].update(text)
                        except Exception as e:
                            print("Error: ", e)
                    break
            window1.close()
        #save
        elif event == 'Save':
            filename = ""
            layoutf = [[sg.Text("File name:")], [sg.Input(key='fout'),sg.Button("Ok")]]
            window1 = sg.Window("File Save", layoutf, modal=True)
            while True:
                event1, values1 = window1.read()
                if event1 == sg.WINDOW_CLOSED:
                    break
                elif event1 == "Ok":
                    filename = values1['fout']
                    break
            window1.close()
            if filename:
                data = {}
                data['board'] = b
                data['rows'] = rows 
                data['cols'] = cols
                data['shift'] = shift

                with open(filename, 'wb') as f:
                    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
                    f.close()
                    
        elif event == 'Options':
            if window['side_col'].visible:
                window['side_col'].update(visible=False)
            else:
                window['side_col'].update(visible=True)
        #mouse up events on main board    
        elif event == 'graph_el+UP':
            x,y = values['graph_el']
            #shift event
            if x < shift*tilesize:
                #determine row
                r = y/tilesize  #integer division
                if b.Shift(int(r),1):
                    refresh = True
            elif x > tilesize*(cols + shift*2) - shift*tilesize:
                r = y/tilesize
                if b.Shift(int(r),-1):
                    refresh = True
            else:
                #add event
                if x > shift*tilesize and x < cols*tilesize + shift*tilesize:
                    #determine col
                    c = (x - shift*tilesize)/tilesize #int div
                    if b.Add(int(c),values['color_el']):
                        refresh = True
            if playinggame and refresh:
                currplayer = currplayer + 1 if currplayer + 1 <= numplayers else 1
                window['color_el'].update(values = initcolors[:int(numplayers)], value=initcolors[currplayer-1])
                window['colorg_el'].update(background_color = initcolors[currplayer-1])
                
                
        #the change options button
        elif event == 'change_btn':
            if int(values['size_el']) != tilesize:
                tilesize = int(values['size_el'])
                refresh = True
                
            window['colorg_el'].update(background_color = values['color_el'])
            #add custom color
            if window['color_el'].Values.count(values['color_el']) == 0:
                newc = values['color_el']
                newl = window['color_el'].Values.copy()
                newl.append(newc)
                window['color_el'].update(values = newl, value=newc)
            #change grid
            if int(values['grid_el']) != gridsize:
                gridsize = int(values['grid_el'])
                refresh = True
        #the update board button        
        elif event == 'update_btn':
            rows = int(values['rowspin_el'])
            cols = int(values['colspin_el'])
            shift = int(values['shiftspin_el'])
            #just checking that combo box has a value
            initshift = values['shiftinit_el'] if type(values['shiftinit_el']) is int else 0
            ninit = initshift if initshift <= shift else shift
            window['shiftinit_el'].update(values = [i for i in range(shift+1)], value = ninit)
            
            #values['shiftinit_el']=0
            b  = stt.ShiftTacToe(int(rows),int(cols),int(shift), initshift)
            refresh = True
        elif event == 'color_el':
            window['colorg_el'].update(background_color = values['color_el'])
            
        elif event == 'numplays_el':
            pass
        elif event == 'game_btn':
            #reset game
            if playinggame == False:
                playinggame = True
                #set colors
                numplayers = int(values['numplays_el'])
                
                #handle more than 8 players
                if numplayers > len(initcolors):
                    r = lambda: random.randint(0,255)
                    for i in range(8, numplayers):
                        color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
                        initcolors.append(color)
                
                currplayer = 1
                window['color_el'].update(values = initcolors[:int(numplayers)], value=initcolors[currplayer-1])
                window['colorg_el'].update(background_color = '#FF0000')
                #button text
                window['game_btn'].update(text='Stop')
                window['update_btn'].update(disabled=True)
                window['change_btn'].update(disabled=True)
            else:
                playinggame = False
                #button text
                window['game_btn'].update(text='Start')
                window['update_btn'].update(disabled=False)
                window['change_btn'].update(disabled=False)
                
            refresh=True
             
        elif event == 'Game Mode':
            if gamemode == True:
                gamemode = False
                playinggame = False
                window['game_btn'].update(visible = False)
                window['game_frm'].update(visible = False)
                window['color_el'].update(values = initcolors, value=initcolors[0])
                window['colorg_el'].update(background_color = values['color_el'])
                window['color_el'].update(disabled=False)
            else:
                gamemode = True
                playinggame = False
                window['game_btn'].update(visible = True)
                window['game_frm'].update(visible = True)
                window['color_el'].update(disabled=True)
            refresh=True    
                
        window.refresh()            
                
    window.close()         
        
