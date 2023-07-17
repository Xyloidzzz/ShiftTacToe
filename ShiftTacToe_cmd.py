###########################################################################
# File: ShiftTacToe_cmd.py
# Author: Tim Wylie
# Date: 7/2023
# Description: A cmd line interface to play the game. Allows for saving and 
#   loading games. Clean, but a bit tedious to use.
###########################################################################



import ShiftTacToe as stt
import pickle




if __name__ == '__main__':
    print('Welcome to Shift-Tac-Toe')
    
    opt = input('(N)ew or (L)oad:')
    if opt=='l' or opt=='L':
        f = input('File:')
        with open(f, 'rb') as pf:
            data = pickle.load(pf)
        
        b = data['board']
        rows = data['rows']
        cols = data['cols']
        shift = data['shift']
    else:
    
        rows = input('Rows:')
        cols = input('Columns:')
        shift = input('Shift:')
        inshift = input('Initial Shift:')
        
        b  = stt.ShiftTacToeE(int(rows),int(cols),int(shift), int(inshift))

    run = True
    while(run):
        b.ToString()
        print("Commands: (A)dd, (S)hift, (F)ile, (E)xit")
        cmd = input('>')
        
        if cmd == 'A' or cmd == 'a':
            c = input('Column:')
            v = input('Piece:')
            b.Add(int(c),v[0])
        elif cmd == 'S' or cmd == 's':
            r = input('Row:')
            d = input('Direction (1 is left, -1 is right):')
            b.Shift(int(r),int(d))
        elif cmd == 'F' or cmd == 'f':
            fn = input('Filename:')
            data = {}
            data['board'] = b
            data['rows'] = rows 
            data['cols'] = cols
            data['shift'] = shift
            with open(fn, 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            
        elif cmd == 'E' or cmd == 'e' or cmd == 'q':
            run = False
        else:
            pass