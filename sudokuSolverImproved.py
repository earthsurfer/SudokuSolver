#!/usr/bin/python -tt
## 
## SOUDOKU Solver Project 
##  Terry Norton
##
import sys
import time

def inRow(i,j):  return ( int(i)/9 == int(j)/9 )  
def inCol(i,j):  return ( int(i) % 9 == int(j) % 9 )
def inBlk(i,j):  return (i/27 == j/27) and ( i%9/3 == j%9/3 )

def prDebug (outStr):
  """ Simple function to print debug string when global:outputDebug = True
  """
  if outputDebug: print outStr
  return
  
def prVerbose (outStr):
  """ Funtion to print status information for the solver algorithym
  """
  if outputVerbose: print outStr
  return

def readPuzzle(file):
  """ readPuzzle(file):
        function to read in puzzle file of 9 lines of 9 characters each 
        returns an 80 character string
        The return data structure will evolve over time.
  """
  try:
    f=open(file)
    prDebug('readPuzzle: Opening puzzle file: ' + file)
  except IOError:
    prDebug('readPuzzle: Failed opening puzzle file')
    print 'IOError on: '+file
    return 1
  a = []
  a=f.read()
  f.close()
  a=a.replace('\n','').replace(' ','').replace(',','')
  prDebug ('a:'+a )
  return a
  
def solvePuzzle(a):
  """ sudoku puzzle solver
        INPUT: sudoku - 80 character string
        Stores solution in global solution when found
        RETURN: nothing
  """
  ## this is a stolen algorithm rewritten for my comprehension
  global loopCntr
  global solved
  global solution
  
  # find first 0 element
  loopCntr += 1
  if '0' in a:
    i = a.index('0')
  else:
    ## Solved!
    solution = a
    return 
    
  ## collect excluded numbers for i
  excludedNums = set()
##  for j in range(len(a)):
  for j in range(81):
    if inRow(i,j) or inCol(i,j) or inBlk(i,j):
      excludedNums.add(a[j])
  
  ## Now attempt a substitution
  for t in '123456789':
    if t not in excludedNums:
     solvePuzzle( a[:i] + t + a[i+1:] )
  return

def printPuzzle ( sudoku ):
  print '-'*34
  print '|',
  for i in range( len(sudoku) ):
    if sudoku[i] != '0': print ' ' + sudoku[i],
    else: print ' ' + '*',
    if not ((i+1) % 9): print '\n',
    if not ((i+1) % 27): print '-'*34 
    if not ((i+1) % 3): print '|',
  return
  
global outputDebug
global outputVerbose
outputDebug = False
outputVerbose = False
loopCntr = 0
solved = False


# Define a main() function that prints a little greeting.
def main():
  """ Solver for basic sudoku puzzles. Input to be either space or comma
      delimited. 0 represents an unfilled / solved location. 
      All 81 locations must be present.
      Ex 1:
        0 3 0 6 2 0 0 0 0
        0 0 6 0 0 1 7 0 2
        0 0 0 9 0 0 3 1 0
        5 9 0 0 0 4 0 0 8
        7 8 2 0 0 0 9 5 4 
        4 0 0 8 0 0 0 3 7
        0 7 9 0 0 2 0 0 0
        3 0 5 4 0 0 6 0 0
        0 0 0 0 9 6 0 2 0
        
      COMMAND LINE:
      
        sudoku.vv.py [--debug][--v] puzzle.txt
      
      Options are:
        --debug   Verbose debugging output to stdout
        --v       Verbose solver information - outputs intermediate computations
  """
  global outputDebug
  global outputVerbose
  global loopCntr
  global solved
  global solution
  outputDebug = False
  outputVerbose = False
  loopCntr = 0
  solved = False
  solution = ''

  
  args = sys.argv[1:]
  for flag in args:
    if flag == '--debug':
      outputDebug = True
    if flag == '--v':
      outputVerbose = True
  if outputDebug: del (args[args.index('--debug')])
  if outputVerbose: del (args[args.index('--v')])
  prDebug('outputDebug is ON')
  prVerbose ('outputVerbose is ON')
  prDebug (str(args))
  
  sudoku = ''
  ## read in puzzle file
  sudoku = readPuzzle(args[0])
  prDebug (sudoku)
  prDebug ( 'main: len(sudoku)=' + str(len(sudoku)) )
  ## print out input puzzle
  print 'Input Puzzle:'
  printPuzzle( sudoku )
  
  startTime = time.time()
  solvePuzzle( sudoku )
  stopTime = time.time()
  
  print '\nSolved Puzzle:'
  printPuzzle( solution )
  prVerbose('Solve time: '+str(stopTime-startTime)+' sec.')
  sys.exit(0)
  
  

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
