import tkinter as tk
from functools import partial
import logging, sys
from time import time,sleep,localtime
import argparse
parser= argparse.ArgumentParser(description='This script takes a formatted .txt \
and feeds into a tkinter display, push one button to advance the test. Usage: \
python3 script_name.py quiz_01.txt')
parser.add_argument('dirPath', help='A formatted .txt file directory path')
args= parser.parse_args()
                                
logging.basicConfig(level= logging.DEBUG)
#logging.disable(logging.CRITICAL)

class First_Multiple_Guess(tk.Frame):
    """Simple trivia game: a question with 4 buttons as answers, pick any
       one to advance to the next question.
       Usage: python3 script.py trivia01.txt
       the text file needs to be formatted:
       1. Question line?
       A. answer one
       B. answer 2
       C. answer 3
       D. None of the above
       D
       """
       
    def __init__(self, file_path, parent=None):
        # create widgets and base attributes
        self.filePath= file_path
        self.parent= parent
        self.parent.title('My trivia game')
        tk.Frame.__init__(self, self.parent)
        self.pack(expand='yes',fill='both')       
        self.canvas= tk.Canvas(self)
        self.canvas.config(width= 1500, height= 700, bg='skyblue',
                           scrollregion=(0,0,3000,3000))
        xbar= tk.Scrollbar(self, orient='horizontal',)        
        xbar.config(command= self.canvas.xview)        
        self.canvas.config(yscrollcommand= xbar.set)                           
        xbar.pack(side='bottom',fill='x',padx=2,pady=2)
        self.canvas.pack(expand=True, fill=tk.BOTH)        
        self.font= ('monospace',18,'bold')
        self.questions= []
        self.answers= []
        self.solutions= []        
        self.count =0
        self.question_var= tk.StringVar()
        self.solution_var= tk.StringVar()
        self.win_var= tk.IntVar()
        self.loss_var= tk.IntVar()
        self.win_static= tk.Label(self.canvas, text='Wins')
        self.win_static.place(x=1300,y=130)
        self.loss_static= tk.Label(self.canvas, text='Loss')
        self.loss_static.place(x=1400,y=130)
        self.quest_label= tk.Label(self.canvas, textvariable= self.question_var,
                                font=self.font)
        self.quest_label.place(x=25,y=15)
        self.sol_label= tk.Label(self.canvas, textvariable= self.solution_var,
                              font=self.font)
        self.sol_label.place(x=50,y=420)       
        self.win_label= tk.Label(self.canvas, textvariable= self.win_var,
                                 font= self.font)
        self.win_label.place(x=1300,y=200)
        self.loss_label= tk.Label(self.canvas, textvariable= self.loss_var,
                                  font= self.font)
        self.loss_label.place(x=1400,y=200)        
        self.g_count=0
        self.a_count= 0
        self.win_count= 0
        self.loss_count=0
        self.total_count=0
        self.open_file()
    def open_file(self):
        """Pulling out the information from the file and
        store it in 3 lists"""
        count =0
        with open(self.filePath, 'r') as file:
            line= file.readline()
            while line:
                if count == 0:
                    self.questions.append(line)
                    count +=1                   
                    line= file.readline()
                elif count == 5:
                    self.solutions.append(line)
                    count = 0                    
                    line= file.readline()
                else:                    
                    self.answers.append(line)
                    count +=1
                    line= file.readline()
        self.length_quest= len(self.questions)
        self.build_puzzle()

    def build_puzzle(self):
        '''Build and place label and 4 buttons use for loop to
           step through a list answers. Partial funtion to assign the solution
           to each button.''' 
        #main loop 
        self.solution_var.set('')
        picks= ['A','B','C','D']
        y2= 60
        quest= self.questions[self.count]
        self.question_var.set(quest)
        self.frame= tk.Frame(self.parent,width=1200,height=360,
                             bg='skyblue')
        self.frame.place(x=50,y=50)
        
        for i in picks:
            answer= self.answers[self.a_count]
            self.btn= tk.Button(self.frame, text=answer,
                                command=partial(self.check_ans, i),
                                 font=self.font)
            self.btn.place(x=40,y=y2)
            y2 += 80
            self.a_count +=1
    def check_ans(self, letter):
        """Comparing the solution to the answer,
           and keep track of wins and losses,
           check for last question."""
        sol= self.solutions[self.count]        
        if sol.strip() == letter:
            self.total_count +=1
            self.win_count +=1
            self.win_var.set(self.win_count)
            if self.total_count == self.length_quest:
                text= 'Correct answers: {:.2%}'.format(self.win_count/self.total_count)
                self.frame.place_forget()
                self.solution_var.set(text)
                self.question_var.set(' ')
            else:
            
                self.frame.place_forget()
                self.solution_var.set(f'Winning answer: {letter}')
                self.question_var.set(' ')
                self.count +=1
                self.canvas.after(2000, self.build_puzzle)
            
        else:
            self.total_count +=1
            self.loss_count +=1
            self.loss_var.set(self.loss_count)
            if self.total_count == self.length_quest:
                text= 'Correct answer: {:.2%}'.format(self.win_count/self.total_count)
                self.frame.place_forget()
                self.solution_var.set(text)
                self.question_var.set(' ')
            else:
                text= f'You picked {letter} and that is incorrect'
                self.frame.place_forget()
                self.solution_var.set(text)
                self.question_var.set(' ')
                self.count +=1
                self.canvas.after(2000, self.build_puzzle)

if __name__ == '__main__':
    dirPath= args.dirPath
    root= tk.Tk()
    First_Multiple_Guess(dirPath, root)
    root.mainloop()
