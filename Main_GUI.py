from tkinter import *
# from tkinter import ttk
import PRs_Extractor as prEx
import time

win = Tk()
win.title('CARTESIAN')
win.geometry('500x400+150+150')
win.resizable(False, False)


def start_prioritization(event):
    repo_name = str_repo.get()
    access_token = str_token.get()
    num_prs = int_num_prs.get()
    if not repo_name and not access_token:
        lbl_name_error.configure(text='*')
        lbl_token_error.configure(text='*')
    elif not access_token:
        lbl_name_error.configure(text='')
        lbl_token_error.configure(text='*')
    elif not repo_name:
        lbl_name_error.configure(text='*')
        lbl_token_error.configure(text='')
    else:
        lbl_name_error.configure(text='')
        lbl_token_error.configure(text='')
        lbl_show_message.configure(text='Pull request extraction in progress..')
        prEx.write_features_to_file(repo_name, num_prs, access_token)
        lbl_show_message.configure(text='Pull request extraction completed')
        time.sleep(3)
        lbl_show_message.configure(text='Features extraction in progress..')
        prEx.extract_features()
        lbl_show_message.configure(text='Features extraction completed')
        # print('done')


def clear_textboxes(event):
    str_repo.set('')
    str_token.set('')
    lbl_name_error.configure(text='')
    lbl_token_error.configure(text='')
    # print('done')


## Create labels
Label(win, text='Enter repo full name').grid(row=0, column=0, sticky=W)
Label(win, text='Enter your access token').grid(row=2, column=0, sticky=W)
Label(win, text='Number of you want to extract').grid(row=3, column=0, sticky=W)

## Create text boxex
str_repo = StringVar()
str_token = StringVar()
int_num_prs = IntVar()
int_num_prs.set(20)
repo_entry = Entry(win, width=30, textvariable=str_repo)
repo_entry.grid(row=0, column=1)
Label(win, text='E.g. PyGithub/PyGithub', foreground='gray').grid(row=1, column=1, sticky=W)
repo_entry.focus()
access_token_entry = Entry(win, width=30, textvariable=str_token)
access_token_entry.grid(row=2, column=1)
num_prs_entry = Entry(win, width=10, textvariable=int_num_prs)
num_prs_entry.grid(row=3, column=1, sticky=W)
Label(win, text='Default value is 20', foreground='gray').grid(row=4, column=1, sticky=W)

lbl_name_error = Label(win, text='', foreground='red')
lbl_name_error.grid(row=0, column=3)

lbl_token_error = Label(win, text='', foreground='red')
lbl_token_error.grid(row=2, column=3)

lbl_show_message = Label(win, text='', foreground='green')
lbl_show_message.grid(row=6, columnspan=2)

## Create a button

start_button = Button(win, text='Start')
start_button.grid(row=5, column=1, sticky=W)
start_button.bind('<Button-1>', start_prioritization)

clear_button = Button(win, text='Clear')
clear_button.grid(row=5, column=1)
clear_button.bind('<Button-1>', clear_textboxes)



mainloop()



