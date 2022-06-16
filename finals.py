from sqlite3.dbapi2 import Time
from tkinter import *
from PIL import Image, ImageTk
from random import randint
import random
from tkinter import messagebox
import sqlite3
from tkinter import font
import time
import datetime as dt
# ---DRE---

root = Tk()
root.title('Guess the country flags!')
root.geometry('700x700')
root.config(bg='light gray')

# DATABASE

# CREATE A DATABASE O KAYA KOKONEK SA ISA
conn = sqlite3.connect('finals_db.db')

# CREATE CURSOR
c = conn.cursor()

# CREATE TABLE
'''
c.execute("""
    CREATE TABLE users
    (uname text,
    pword text)
    """)
'''
# LOADING
def loading1():
    global fr
    fr = Frame(root, width=700, height=700, padx=228, pady=108)
    fr.pack(side=TOP, expand=YES)
    frameCnt = 12
    frames = [PhotoImage(file='loading.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    def update(ind):
        frame = frames[ind]
        ind += 1
        label.configure(image=frame)
        if ind == 12:
            fr.destroy()
            signup_function()
        loop = 0
        if ind <= 11:
            fr.after(50, update, ind)
            loop += 1
    label = Label(fr)
    label.pack()
    fr.after(0, update, 0)

# LOADING
def loading2():
    global fr
    fr = Frame(root, width=700, height=700, padx=228, pady=108)
    fr.pack(side=TOP, expand=YES)
    frameCnt = 12
    frames = [PhotoImage(file='loading.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    def update(ind):
        frame = frames[ind]
        ind += 1
        label.configure(image=frame)
        if ind == 12:
            fr.destroy()
            login()
        loop = 0
        if ind <= 11:
            fr.after(50, update, ind)
            loop += 1
    label = Label(fr)
    label.pack()
    fr.after(0, update, 0)

def signup_function():
    # CREATE SIGNUP FRAME
    signup_frame = Frame(root, height=700, width=700, padx=50, pady=50)
    signup_frame.pack(side=TOP, expand=YES)

    # SIGNUP CONTENTS
    def signup_command(event=None):
        c.execute("SELECT * FROM users WHERE uname = '" + signup_username_entry.get() + "'")
        existing_uname_fetched = c.fetchone()
        print('This is existing_uname_fetched')
        print(existing_uname_fetched)
        if signup_username_entry.get() == '' or signup_password_entry.get() == '':
            signup_spacing.config(text='Please enter value', fg='red')
            messagebox.showinfo('Notice', 'Please enter value')
        elif signup_password_entry.get() != signup_password_verify_entry.get():
            signup_spacing.config(text='Password does not match', fg='red')
            messagebox.showinfo('Notice', 'Password does not match')
        elif existing_uname_fetched == None and signup_password_entry.get() == signup_password_verify_entry.get():
            c.execute("INSERT INTO users (uname, pword) VALUES (:uname, :pword)",
                {
                    'uname': signup_username_entry.get(),
                    'pword': signup_password_entry.get()
                })
            
            # COMMIT CHANGES
            conn.commit()

            # SHOW MESSAGEBOX
            messagebox.showinfo('Notice', 'Sign up successfully')

            # BACK TO LOGIN
            signup_frame.pack_forget()
            login()

        elif signup_username_entry.get() == existing_uname_fetched[1]:

            signup_spacing.config(text='Username exists. Please use another username.', fg='red')
            
            # SHOW MESSAGEBOX
            messagebox.showinfo('Notice', 'Username Exists')
        
        else:
            pass

    def signup_username_checking(event=None):
        global check_signup_username_fetched
        c.execute("SELECT * FROM users WHERE uname = '" + signup_username_entry.get() + "'")
        check_signup_username_fetched = c.fetchone()
        if signup_username_entry.get() == '':
            signup_spacing.config(text='Please enter a username', fg='red')
            signup_btn.config(state=DISABLED)
        elif check_signup_username_fetched == None:
            signup_spacing.config(text='Username available', fg='green')
            signup_btn.config(state=NORMAL)
        elif check_signup_username_fetched != None:
            signup_spacing.config(text='Username not available', fg='red')
            signup_btn.config(state=DISABLED)

    global logo
    img = Image.open('flag_logo.png')
    logo = ImageTk.PhotoImage(img)
    logo_lbl = Label(signup_frame, image=logo, pady=5)
    logo_lbl.grid(row=0, column=0, columnspan=2)
    signup_label = Label(signup_frame, text='SIGN UP', font=('', 35))
    signup_label.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    signup_spacing = Label(signup_frame, text='')
    signup_spacing.grid(row=2, column=0, columnspan=2, sticky=NSEW)
    signup_username_label = Label(signup_frame, text='Username', anchor='w')
    signup_username_label.grid(row=3, column=0, sticky=W, columnspan=2)
    signup_username_entry = Entry(signup_frame, width=50)
    signup_username_entry.grid(row=4, column=0, sticky=W, columnspan=2)
    signup_password_label = Label(signup_frame, text='Password', anchor='w')
    signup_password_label.grid(row=5, column=0, sticky=W, columnspan=2)
    signup_password_entry = Entry(signup_frame, width=50)
    signup_password_entry.grid(row=6, column=0, sticky=W, columnspan=2)
    signup_password_entry.config(show='●')
    signup_password_verify_label = Label(signup_frame, text='Verify Password', anchor='w')
    signup_password_verify_label.grid(row=8, column=0, sticky=W, columnspan=2)
    signup_password_verify_entry = Entry(signup_frame, width=50)
    signup_password_verify_entry.grid(row=9, column=0, sticky=W, columnspan=2)
    signup_password_verify_entry.config(show='●')
    signup_password_entry.config(show='●')
    signup_btn = Button(signup_frame, text='Signup', padx=5, pady=5, command=signup_command, bd=3, relief=RAISED)
    signup_btn.grid(row=11, column=0, sticky=W, pady=(5, 0), columnspan=2)

    signup_username_entry.bind('<Tab>', signup_username_checking)
    signup_username_entry.bind('<FocusOut>', signup_username_checking)

    signup_username_entry.bind('<Return>', signup_command)
    signup_password_entry.bind('<Return>', signup_command)
    signup_password_verify_entry.bind('<Return>', signup_command)
    signup_btn.bind('<Return>', signup_command)

    def show_pass():
        if var.get() == 1:
            signup_password_entry.config(show='')
        if var.get() == 0:
            signup_password_entry.config(show='●')

    # Creating a checkbox
    var = IntVar()
    var.set('0')
    check = Checkbutton(signup_frame, text='Show Password', onvalue=1, offvalue=0, variable=var, command=show_pass, anchor=CENTER)
    check.grid(row=7, column=1, sticky=E)
    
    # Creating a checkbox for verify
    def show_pass_verify():
        if var_verify.get() == 1:
            signup_password_verify_entry.config(show='')
        if var_verify.get() == 0:
            signup_password_verify_entry.config(show='●')

    # Creating a checkbox
    var_verify = IntVar()
    var_verify.set('0')
    check_verify = Checkbutton(signup_frame, text='Show Password', onvalue=1, offvalue=0, variable=var_verify, command=show_pass_verify, anchor=CENTER)
    check_verify.grid(row=10, column=1, sticky=E)

    # ALREADY SIGNED UP? LOG IN HERE
    asu_label = Label(signup_frame, text="Already signed up? Login", anchor='w')
    asu_label.grid(row=12, column=0, sticky=W, pady=(5, 0))
    def here_signup_not_underlined(event=None):
        f = font.Font(here_signup_label, here_signup_label.cget("font"))
        f.configure(underline = False)
        here_signup_label.configure(font=f)
    def here_signup_underlined(event=None):
        f = font.Font(here_signup_label, here_signup_label.cget("font"))
        f.configure(underline = True)
        here_signup_label.configure(font=f)
    def back_to_login(event=None):
        signup_frame.pack_forget()
        loading2()
    here_signup_label = Label(signup_frame, text="here.", fg='#007AFF', anchor='w')
    here_signup_label.grid(row=12, column=0, pady=(5, 0), sticky=W, padx=(157, 0))
    here_signup_label.bind('<Button-1>', back_to_login)
    here_signup_label.bind('<Leave>', here_signup_not_underlined)
    here_signup_label.bind('<Enter>', here_signup_underlined)

def login():
    # LOG IN FORM
    login_frame = Frame(root, width=700, height=700, padx=50, pady=50)
    login_frame.pack(side=TOP, expand=YES)

    # LOGIN CONTENTS
    def login_command(event=None):
        c.execute("SELECT * FROM users WHERE uname = '" + username_entry.get() + "' AND pword = '" + password_entry.get() + "'")
        result = c.fetchone()
        print('This is result')
        print(result)
        if password_entry.get() == '' or username_entry.get() == '':
            notice_label.config(text='Please enter a value')
            messagebox.showwarning('Notice', 'Please enter a value')
        elif result == None:
            notice_label.config(text='Wrong username or password', fg='red')
            messagebox.showinfo('Notice', 'Wrong username or password')
        else:
            # LOGIN FRAME FORGET
            login_frame.pack_forget()

            c.execute("SELECT * FROM users WHERE users_id = " + str(result[0]))
            name_display = c.fetchone()
            # HOME
            messagebox.showinfo('Notice', 'Welcome ' + name_display[1])
            def home():
                # HOME FRAME
                home_frame = Frame(root, width=700, height=300, padx=50, pady=50)
                home_frame.pack(side=TOP)

                # HOME CONTENT
                print('this is name_display')
                print(name_display)
                name_logged_in = Label(home_frame, text=name_display[1], font=('', 50))
                name_logged_in.grid(row=0, column=0, sticky=W, columnspan=2)
                
                # CLOCK
                class ElapsedTimeClock(Label):
                    def __init__(self, parent, *args, **kwargs):
                        Label.__init__(self, parent, *args, **kwargs)
                        self.lastTime = ""
                        t = time.localtime()
                        self.zeroTime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])
                        self.tick()
                
                    def tick(self):
                        # get the current local time from the PC
                        now = dt.datetime(1, 1, 1).now()
                        time2 = now.strftime('%H:%M:%S\n%D')
                        # if time string has changed, update it
                        if time2 != self.lastTime:
                            self.lastTime = time2
                            self.config(text=time2)
                        # calls itself every 200 milliseconds
                        # to update the time display as needed
                        # could use >200 ms, but display gets jerky
                        self.after(200, self.tick)
                
                if __name__ == "__main__":
                    clock = ElapsedTimeClock(home_frame, anchor=CENTER)
                    clock.grid(row=0, column=2, columnspan=2, sticky=E)

                # DEFINES
                def logout_command():
                    Msgbx = messagebox.askquestion('NOTICE', 'Are you sure you want to logout?')
                    if Msgbx == 'yes':
                        home_frame.pack_forget()
                        app_frame.pack_forget()
                        loading2()
                    else:
                        pass

                def change_password_command():
                    change_password_window = Toplevel(root, height=300, width=400, bg='light gray')
                    change_password_window.title('Change Password')
                    change_password_window.grab_set()
                    
                    # FRAMES FOR CHANGING PASSWORDS
                    change_password_frame = Frame(change_password_window, height=300, width=400, pady=50, padx=50)
                    change_password_frame.pack(side=TOP, expand=YES)

                    class change_password_class:
                        def __init__(self, current_password, new_password, new_password_verify):
                            self.current_password = current_password
                            self.new_password = new_password
                            self.new_password_verify = new_password_verify

                    def confirm_password_btn_command():
                        c.execute("SELECT * FROM users WHERE users_id = " + str(result[0]))
                        cpf = c.fetchone()
                        passwords = change_password_class(current_password_entry.get(), new_password_entry.get(), new_password_verify_entry.get())
                        if passwords.current_password == None or passwords.new_password == None or passwords.new_password_verify == None:
                            notif_on_change_password_label.config(text='Please fill the blanks')
                            messagebox.showwarning('NOTICE', 'Please fill the blanks')
                        elif cpf[2] != passwords.current_password:
                            notif_on_change_password_label.config(text='Wrong current password')
                            messagebox.showwarning('NOTICE', 'Wrong current password')
                        elif passwords.new_password != passwords.new_password_verify:
                            notif_on_change_password_label.config(text="New password don't match")
                            cpMsgbx = messagebox.showwarning('NOTICE', "New password don't match")
                        elif passwords.new_password == passwords.new_password_verify:
                            c.execute("UPDATE users SET pword ='" + passwords.new_password + "' WHERE users_id = " + str(result[0]))
                            conn.commit()
                            cpMsgbx = messagebox.showinfo('NOTICE', 'Password changed successfully')
                            if cpMsgbx == 'ok':
                                change_password_window.grab_release()
                                change_password_window.destroy()
                        else:
                            pass

                    change_password_label = Label(change_password_frame, text='Change Password', font=('', 25))
                    notif_on_change_password_label = Label(change_password_frame, text='', fg='red')
                    current_password_label = Label(change_password_frame, text='Current Password')
                    new_password_label = Label(change_password_frame, text='New Password')
                    new_password_verify_label = Label(change_password_frame, text='Verify New Password')
                    current_password_entry = Entry(change_password_frame, width=20)
                    new_password_entry = Entry(change_password_frame, width=20)
                    new_password_verify_entry = Entry(change_password_frame, width=20)
                    confirm_password_btn = Button(change_password_frame, text='Change Password', pady=5, padx=5, bd=3, relief=SUNKEN, command=confirm_password_btn_command)

                    change_password_label.grid(row=0, column=0, columnspan=2)
                    notif_on_change_password_label.grid(row=1, column=0, columnspan=2)
                    current_password_label.grid(row=2, column=0, sticky=W)
                    current_password_entry.grid(row=3, column=0, sticky=W)
                    current_password_entry.config(show='●')
                    new_password_label.grid(row=5, column=0, sticky=W)
                    new_password_entry.grid(row=6, column=0, sticky=W)
                    new_password_entry.config(show='●')
                    new_password_verify_label.grid(row=8, column=0, sticky=W)
                    new_password_verify_entry.grid(row=9, column=0, sticky=W)
                    new_password_verify_entry.config(show='●')
                    confirm_password_btn.grid(row=11, column=0, sticky=W)

                    # CREATING CHECKBOX FOR CHANGE PASSWORDS
                    # Creating a checkbox for current
                    def cp_show_pass_current():
                        if cp_var_current.get() == 1:
                            current_password_entry.config(show='')
                        if cp_var_current.get() == 0:
                            current_password_entry.config(show='●')
                    # Creating a checkbox
                    cp_var_current = IntVar()
                    cp_var_current.set('0')
                    cp_check_current = Checkbutton(change_password_frame, text='Show Password', onvalue=1, offvalue=0, variable=cp_var_current, command=cp_show_pass_current, anchor=CENTER)
                    cp_check_current.grid(row=4, column=0, sticky=E)

                    # Creating a checkbox for new
                    def cp_show_pass_new():
                        if cp_var_new.get() == 1:
                            new_password_entry.config(show='')
                        if cp_var_new.get() == 0:
                            new_password_entry.config(show='●')
                    # Creating a checkbox
                    cp_var_new = IntVar()
                    cp_var_new.set('0')
                    cp_check_new = Checkbutton(change_password_frame, text='Show Password', onvalue=1, offvalue=0, variable=cp_var_new, command=cp_show_pass_new, anchor=CENTER)
                    cp_check_new.grid(row=7, column=0, sticky=E)

                    # Creating a checkbox for verify new
                    def cp_show_pass_verify_new():
                        if cp_var_verify_new.get() == 1:
                            new_password_verify_entry.config(show='')
                        if cp_var_verify_new.get() == 0:
                            new_password_verify_entry.config(show='●')
                    # Creating a checkbox
                    cp_var_verify_new = IntVar()
                    cp_var_verify_new.set('0')
                    cp_check_verify_new = Checkbutton(change_password_frame, text='Show Password', onvalue=1, offvalue=0, variable=cp_var_verify_new, command=cp_show_pass_verify_new, anchor=CENTER)
                    cp_check_verify_new.grid(row=10, column=0, sticky=E)

                def change_username_command():
                    # CHANGE_USERNAME WINDOW
                    change_username_window = Toplevel(root, height=300, width=400, bg='light gray')
                    change_username_window.title('Change Username')
                    change_username_window.grab_set()

                    # CHANGE_USERNAME FRAME
                    change_username_frame = Frame(change_username_window, height=300, width=400, pady=50, padx=50)
                    change_username_frame.pack(side=TOP, expand=YES)

                    def check_username(event=None):
                        global check_username_fetched
                        c.execute("SELECT * FROM users WHERE uname = '" + cu_new_username_entry.get() + "'")
                        check_username_fetched = c.fetchone()
                        if cu_new_username_entry.get() == '':
                            cu_notice.config(text='Please enter a value', fg='red')
                            cu_btn.config(state=DISABLED)
                        elif check_username_fetched == None:
                            cu_notice.config(text='Username available', fg='green')
                            cu_btn.config(state=ACTIVE)
                        elif check_username_fetched != None:
                            cu_notice.config(text='Username not available', fg='red')
                            cu_btn.config(state=DISABLED)

                    def cu_btn_command():
                        c.execute("SELECT * FROM users WHERE users_id = " + str(result[0]))
                        cu_validate_current = c.fetchone()
                        if cu_new_username_entry.get() == '' or cu_verify_new_username_entry.get() == '' or cu_current_password_entry.get() == '':
                            messagebox.showwarning('NOTICE', 'Please enter a value')
                            cu_notice.config(text='Please enter a value', fg='red')
                        elif cu_new_username_entry.get() != cu_verify_new_username_entry.get():
                            messagebox.showwarning('NOTICE', "Username don't match")
                            cu_notice.config(text="Username don't match", fg='red')
                        elif cu_current_password_entry.get() != cu_validate_current[2]:
                            messagebox.showwarning('NOTICE', 'Wrong Password')
                            cu_notice.config(text='Wrong Password', fg='red')
                        elif cu_new_username_entry.get() == cu_verify_new_username_entry.get():
                            print('This is name display in change username')
                            print(name_display)
                            c.execute("UPDATE users SET uname = '" + cu_new_username_entry.get() + "' WHERE users_id = " + str(name_display[0]))
                            conn.commit()
                            c.execute("SELECT * FROM users WHERE users_id = " + str(result[0]))
                            cu_name = c.fetchone()
                            print(cu_name)
                            messagebox.showinfo('NOTICE', 'Username changed successfully')
                            name_logged_in.config(text=cu_name[1])
                            change_username_window.grab_release()
                            change_username_window.destroy()
                        else:
                            print('this is else')

                    # CHANGE_USERNAME_CONTENT
                    global cu_notice
                    cu_label = Label(change_username_frame, text='Change Username', font=('', 25))
                    cu_notice = Label(change_username_frame, text='')
                    cu_new_username = Label(change_username_frame, text='New Username')
                    cu_new_username_entry = Entry(change_username_frame, width=20)
                    cu_verify_new_username = Label(change_username_frame, text='Verify New Username')
                    cu_verify_new_username_entry = Entry(change_username_frame, width=20)
                    cu_current_password = Label(change_username_frame, text='Enter Current Password')
                    cu_current_password_entry = Entry(change_username_frame, width=20)
                    cu_btn = Button(change_username_frame, text='Change Username', pady=5, padx=5, command=cu_btn_command)

                    cu_label.grid(row=0, column=0, columnspan=2)
                    cu_notice.grid(row=1, column=0, columnspan=2)
                    cu_new_username.grid(row=2, column=0, sticky=W)
                    cu_new_username_entry.grid(row=3, column=0, sticky=W)
                    cu_verify_new_username.grid(row=4, column=0, sticky=W)
                    cu_verify_new_username_entry.grid(row=5, column=0, sticky=W)
                    cu_current_password.grid(row=6, column=0, sticky=W)
                    cu_current_password_entry.grid(row=7, column=0, sticky=W)
                    cu_current_password_entry.config(show='●')
                    cu_btn.grid(row=9, column=0, sticky=W)

                    cu_verify_new_username_entry.bind('<Button-1>', check_username)
                    cu_new_username_entry.bind('<Tab>', check_username)

                    # Creating a checkbox for verify cu_current_password
                    def cu_show_pass_current():
                        if cu_var_current.get() == 1:
                            cu_current_password_entry.config(show='')
                        if cu_var_current.get() == 0:
                            cu_current_password_entry.config(show='●')
                    # Creating a checkbox
                    cu_var_current = IntVar()
                    cu_var_current.set('0')
                    cu_check_current = Checkbutton(change_username_frame, text='Show Password', onvalue=1, offvalue=0, variable=cu_var_current, command=cu_show_pass_current, anchor=CENTER)
                    cu_check_current.grid(row=8, column=0, sticky=E)

                def restart_command():
                    msgbox = messagebox.askquestion("NOTICE", "Are you sure you want to restart?")
                    if msgbox == 'yes':
                        hide_frames_commands()
                        play_command()
                    else:
                        pass

                def play_command():
                    hide_frames_commands()
                    play_frame.pack(side=TOP, expand=YES)

                    play_restart_btn.grid_forget()
                    play_restart_btn.grid(row=2, column=0, columnspan=4, pady=(5, 0))
                    play_restart_btn.config(text='RESTART', command=restart_command)

                    scores_btn.config(command=scores_with_ask_command)

                    global countries
                    global score
                    global number
                    global countries_index
                    # Create a list of countries
                    countries = ['canada', 'china', 'hong_kong', 'indonesia', 'japan', 'philippines', 'singapore', 'south_korea', 'united_kingdom', 'united_states_of_america']

                    # Shuffling the list
                    random.shuffle(countries)

                    # Score
                    score = 0

                    # Number
                    number = 1

                    # Countries index
                    countries_index = 0

                    def start():
                        # Creating start frame
                        global start_frame
                        start_frame = Frame(play_frame, height=500, width=500, padx=50, pady=50)
                        start_frame.pack(side=TOP, expand=YES)

                        if number <= 10:
                            # Creating your score
                            your_score = Label(start_frame, text='Your score = ' + str(score), font=('', 25))
                            your_score.grid(row=1, column=0, columnspan=2)

                            # Number
                            item_number = Label(start_frame, text=str(number) + '. ', anchor=N)
                            item_number.grid(row=2, column=0, sticky=N)

                            # Images
                            directory = './png country/' + countries[countries_index] + '.png'
                            global country_image
                            image_holder = Image.open(directory)
                            # resizing
                            country_img_resizing = image_holder.resize((200, 200), Image.ANTIALIAS)
                            # Putting it into variable
                            country_image = ImageTk.PhotoImage(country_img_resizing)
                            show_country_image = Label(start_frame, image=country_image, bg='#d3e6e8')
                            show_country_image.grid(row=2, column=1)

                            choices=[]
                            counter = 1
                            local_countries=[]
                            local_countries.extend(countries)
                            choices.append(local_countries[countries_index])
                            local_countries.remove(local_countries[countries_index])
                            while counter < 3:
                                random.shuffle(local_countries)
                                rand = randint(0, len(local_countries)-1)
                                choices.append(local_countries[rand])
                                local_countries.remove(local_countries[rand])
                                counter += 1
                            random.shuffle(choices)
                            
                            # Creating radio button
                            var = StringVar()
                            r1 = Radiobutton(start_frame, text=choices[0], variable=var, value=choices[0])
                            r1.grid(row=3, column=1, sticky=W, columnspan=2)
                            r2 = Radiobutton(start_frame, text=choices[1], variable=var, value=choices[1])
                            r2.grid(row=4, column=1, sticky=W, columnspan=2)
                            r3 = Radiobutton(start_frame, text=choices[2], variable=var, value=choices[2])
                            r3.grid(row=5, column=1, sticky=W, columnspan=2)

                            # Answer button
                            ans_btn = Button(start_frame, text='Answer', command=lambda: answer_process(var.get()), padx=5, pady=5)
                            ans_btn.grid(row=6, column=0, columnspan=2)

                            def answer_process(value):
                                print(value)
                                global score
                                global number
                                global countries_index
                                if value == countries[countries_index]:
                                    messagebox.showinfo('', 'You are correct!')
                                    hide_frames()
                                    score += 1
                                    number += 1
                                    countries_index += 1
                                    show_next_frame()
                                else:
                                    messagebox.showwarning('', 'You are wrong!')
                                    hide_frames()
                                    number += 1
                                    countries_index += 1
                                    show_next_frame()
                                
                                if number == 11:
                                    if score <= 3:
                                        messagebox.showinfo('Results', 'Your score: ' + str(score) + '/10\nBetter luck next time!')
                                    if 4 <= score and score <=6:
                                        messagebox.showinfo('Results', 'Your score: ' + str(score) + '/10\nNice!')
                                    if 7 <= score and score <=9:
                                        messagebox.showinfo('Results', 'Your score: ' + str(score) + '/10\nGood Job!')
                                    if score == 10:
                                        messagebox.showinfo('Results', 'PERFECT!')
                                    print(score)

                                    c.execute("INSERT INTO scores_tbl (scores, users_id, scores_time, scores_date) VALUES (" + str(score) + ", " + str(result[0]) + ", time('now', 'localtime'), date('now', 'localtime'))")
                                    conn.commit()
                                    scores_command()

                    def show_next_frame():
                        global start_frame
                        start()

                    def hide_frames():
                        global start_frame

                        for widget in start_frame.winfo_children():
                            widget.destroy()

                        start_frame.pack_forget()
                    start()

                def scores_with_ask_command():
                    askmsgbox = messagebox.askquestion("NOTICE", "Are you sure you want to leave?")
                    if askmsgbox == 'yes':
                        scores_command()
                    else:
                        pass

                def scores_command():
                    hide_frames_commands()
                    scores_frame.pack(side=TOP, expand=YES, padx=50, pady=50)

                    play_restart_btn.grid_forget()
                    play_restart_btn.grid(row=2, column=0, columnspan=4, pady=(5, 0))
                    play_restart_btn.config(text='PLAY', command=play_command)

                    scores_btn.config(command=scores_command)

                    c.execute("SELECT users.uname, scores_tbl.scores, scores_tbl.scores_time, scores_tbl.scores_date FROM scores_tbl INNER JOIN users ON scores_tbl.users_id = users.users_id WHERE scores_tbl.users_id = " + str(result[0]))
                    scores_table_fetched = c.fetchall()
                    print(scores_table_fetched)

                    # CREATING A HEADER AS RADIOBUTTON
                    scores_var = IntVar()
                    scores_tbl_username = Radiobutton(scores_frame, text='Username', pady=5, padx=5, bd=3, relief=GROOVE, variable=scores_var, value=1, command=lambda: scores_sort(scores_var.get()))
                    scores_tbl_scores = Radiobutton(scores_frame, text='Scores', padx=5, pady=5, bd=3, relief=GROOVE, variable=scores_var, value=2, command=lambda: scores_sort(scores_var.get()))
                    scores_tbl_time = Radiobutton(scores_frame, text='Time', padx=5, pady=5, bd=3, relief=GROOVE, variable=scores_var, value=3, command=lambda: scores_sort(scores_var.get()))
                    scores_tbl_date = Radiobutton(scores_frame, text='Date', padx=5, pady=5, bd=3, relief=GROOVE, variable=scores_var, value=4, command=lambda: scores_sort(scores_var.get()))

                    def scores_sort(value):
                        if value == 1:
                            forget_data()
                            data_frame.grid(columnspan=4, sticky=NSEW)
                            data_frame.grid_columnconfigure(0, weight=1)
                            c.execute("SELECT users.uname, scores_tbl.scores, scores_tbl.scores_time, scores_tbl.scores_date FROM scores_tbl INNER JOIN users ON scores_tbl.users_id = users.users_id WHERE scores_tbl.users_id = " + str(result[0]) + " ORDER BY users.uname DESC")
                            scores_table_fetched1 = c.fetchall()
                            for i in range (len(scores_table_fetched1)):
                                scores_data_username = Label(data_frame, text=scores_table_fetched1[i][0], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_scores = Label(data_frame, text=scores_table_fetched1[i][1], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_time = Label(data_frame, text=scores_table_fetched1[i][2], padx=5, pady=5, bd=3, relief=GROOVE)
                                scores_data_date = Label(data_frame, text=scores_table_fetched1[i][3], padx=5, pady=5, bd=3, relief=GROOVE)

                                scores_data_username.grid(row=i+1, column=0, sticky=NSEW)
                                scores_data_scores.grid(row=i+1, column=1, sticky=NSEW)
                                scores_data_time.grid(row=i+1, column=2, sticky=NSEW)
                                scores_data_date.grid(row=i+1, column=3, sticky=NSEW)
                        elif value == 2:
                            forget_data()
                            data_frame.grid(columnspan=4, sticky=NSEW)
                            data_frame.grid_columnconfigure(0, weight=1)
                            c.execute("SELECT users.uname, scores_tbl.scores, scores_tbl.scores_time, scores_tbl.scores_date FROM scores_tbl INNER JOIN users ON scores_tbl.users_id = users.users_id WHERE scores_tbl.users_id = " + str(result[0]) + " ORDER BY scores_tbl.scores DESC")
                            scores_table_fetched2 = c.fetchall()
                            for i in range (len(scores_table_fetched2)):
                                scores_data_username = Label(data_frame, text=scores_table_fetched2[i][0], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_scores = Label(data_frame, text=scores_table_fetched2[i][1], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_time = Label(data_frame, text=scores_table_fetched2[i][2], padx=5, pady=5, bd=3, relief=GROOVE)
                                scores_data_date = Label(data_frame, text=scores_table_fetched2[i][3], padx=5, pady=5, bd=3, relief=GROOVE)

                                scores_data_username.grid(row=i+1, column=0, sticky=NSEW)
                                scores_data_scores.grid(row=i+1, column=1, sticky=NSEW)
                                scores_data_time.grid(row=i+1, column=2, sticky=NSEW)
                                scores_data_date.grid(row=i+1, column=3, sticky=NSEW)
                        elif value == 3:
                            forget_data()
                            data_frame.grid(columnspan=4, sticky=NSEW)
                            data_frame.grid_columnconfigure(0, weight=1)
                            c.execute("SELECT users.uname, scores_tbl.scores, scores_tbl.scores_time, scores_tbl.scores_date FROM scores_tbl INNER JOIN users ON scores_tbl.users_id = users.users_id WHERE scores_tbl.users_id = " + str(result[0]) + " ORDER BY scores_tbl.scores_time DESC")
                            scores_table_fetched3 = c.fetchall()
                            for i in range (len(scores_table_fetched3)):
                                scores_data_username = Label(data_frame, text=scores_table_fetched3[i][0], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_scores = Label(data_frame, text=scores_table_fetched3[i][1], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_time = Label(data_frame, text=scores_table_fetched3[i][2], padx=5, pady=5, bd=3, relief=GROOVE)
                                scores_data_date = Label(data_frame, text=scores_table_fetched3[i][3], padx=5, pady=5, bd=3, relief=GROOVE)

                                scores_data_username.grid(row=i+1, column=0, sticky=NSEW)
                                scores_data_scores.grid(row=i+1, column=1, sticky=NSEW)
                                scores_data_time.grid(row=i+1, column=2, sticky=NSEW)
                                scores_data_date.grid(row=i+1, column=3, sticky=NSEW)
                        elif value == 4:
                            forget_data()
                            data_frame.grid(columnspan=4, sticky=NSEW)
                            data_frame.grid_columnconfigure(0, weight=1)
                            c.execute("SELECT users.uname, scores_tbl.scores, scores_tbl.scores_time, scores_tbl.scores_date FROM scores_tbl INNER JOIN users ON scores_tbl.users_id = users.users_id WHERE scores_tbl.users_id = " + str(result[0]) + " ORDER BY scores_tbl.scores_date DESC")
                            scores_table_fetched4 = c.fetchall()
                            for i in range (len(scores_table_fetched4)):
                                scores_data_username = Label(data_frame, text=scores_table_fetched4[i][0], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_scores = Label(data_frame, text=scores_table_fetched4[i][1], padx=50, pady=5, bd=3, relief=GROOVE)
                                scores_data_time = Label(data_frame, text=scores_table_fetched4[i][2], padx=5, pady=5, bd=3, relief=GROOVE)
                                scores_data_date = Label(data_frame, text=scores_table_fetched4[i][3], padx=5, pady=5, bd=3, relief=GROOVE)

                                scores_data_username.grid(row=i+1, column=0, sticky=NSEW)
                                scores_data_scores.grid(row=i+1, column=1, sticky=NSEW)
                                scores_data_time.grid(row=i+1, column=2, sticky=NSEW)
                                scores_data_date.grid(row=i+1, column=3, sticky=NSEW)

                    def forget_data():
                        data_frame.grid_forget()

                    scores_tbl_username.grid(row=0, column=0, sticky=NSEW)
                    scores_tbl_scores.grid(row=0, column=1, sticky=NSEW)
                    scores_tbl_time.grid(row=0, column=2, sticky=NSEW)
                    scores_tbl_date.grid(row=0, column=3, sticky=NSEW)

                    data_frame = Frame(scores_frame)
                    data_frame.grid(columnspan=4, sticky=NSEW)
                    data_frame.grid_columnconfigure(0, weight=1)
                    for i in range (len(scores_table_fetched)):
                        scores_data_username = Label(data_frame, text=scores_table_fetched[i][0], padx=50, pady=5, bd=3, relief=GROOVE)
                        scores_data_scores = Label(data_frame, text=scores_table_fetched[i][1], padx=50, pady=5, bd=3, relief=GROOVE)
                        scores_data_time = Label(data_frame, text=scores_table_fetched[i][2], padx=5, pady=5, bd=3, relief=GROOVE)
                        scores_data_date = Label(data_frame, text=scores_table_fetched[i][3], padx=5, pady=5, bd=3, relief=GROOVE)

                        scores_data_username.grid(row=i+1, column=0, sticky=NSEW)
                        scores_data_scores.grid(row=i+1, column=1, sticky=NSEW)
                        scores_data_time.grid(row=i+1, column=2, sticky=NSEW)
                        scores_data_date.grid(row=i+1, column=3, sticky=NSEW)

                def hide_frames_commands():
                    play_btn.destroy()

                    for widget in scores_frame.winfo_children():
                        widget.destroy()
                    scores_frame.pack_forget()

                    for widget in play_frame.winfo_children():
                        widget.destroy()
                    play_frame.pack_forget()

                # BUTTONS
                # CHOICES
                scores_btn = Button(home_frame, text='Scores', bd=3, relief=SUNKEN, padx=5, pady=5, command=scores_command)
                scores_btn.grid(row=1, column=0, pady=5, padx=(0, 10))
                change_password_btn = Button(home_frame, text='Change Password', bd=3, relief=RAISED, padx=5, pady=5, command=change_password_command)
                change_password_btn.grid(row=1, column=1, pady=5, padx=(0, 10))
                change_username_btn = Button(home_frame, text='Change Username', bd=3, relief=RAISED, padx=5, pady=5, command=change_username_command)
                change_username_btn.grid(row=1, column=2, pady=5, padx=(0, 10))
                logout_btn = Button(home_frame, text='Logout', bd=3, relief=SUNKEN, padx=5, pady=5, command=logout_command)
                logout_btn.grid(row=1, column=3, pady=5)

                play_restart_btn = Button(home_frame, text='', padx=5, pady=5, command='')

                # NEW FRAME FOR APP
                app_frame = Frame(root, bg='#007AFF', width=500, height=700)
                app_frame.pack()
    
                play_btn = Button(app_frame, text='PLAY', bd=3, relief=SUNKEN, padx=5, pady=5, bg='red', command=play_command, font=('', 70))
                play_btn.pack(padx=100, pady=100)

                play_frame = Frame(app_frame, height=500, width=500)
                scores_frame = Frame(app_frame, height=500, width=500)

            home()

    global logo
    img = Image.open('flag_logo.png')
    logo = ImageTk.PhotoImage(img)
    logo_lbl = Label(login_frame, image=logo, pady=5)
    logo_lbl.grid(row=0, column=0, columnspan=2)
    login_label = Label(login_frame, text='LOGIN', font=('', 35))
    login_label.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    notice_label = Label(login_frame, text='', fg='red')
    notice_label.grid(row=2, column=0, columnspan=2, sticky=NSEW)
    username_label = Label(login_frame, text='Username', anchor=W)
    username_label.grid(row=3, column=0, columnspan=2, sticky=W)
    username_entry = Entry(login_frame, width=50)
    username_entry.grid(row=4, column=0, columnspan=2, sticky=W)
    password_label = Label(login_frame, text='Password', anchor=W)
    password_label.grid(row=5, column=0, sticky=W, columnspan=2)
    password_entry = Entry(login_frame, width=50)
    password_entry.grid(row=6, column=0, columnspan=2, sticky=W)
    password_entry.config(show='●')
    login_btn = Button(login_frame, text='Login', padx=5, pady=5, bd=3, relief=RAISED, command=login_command)
    login_btn.grid(row=7, column=0, sticky=W, pady=(5, 0), columnspan=2)

    username_entry.bind('<Return>', login_command)
    password_entry.bind('<Return>', login_command)
    login_btn.bind('<Return>', login_command)

    def show_pass():
        if var.get() == 1:
            password_entry.config(show='')
        if var.get() == 0:
            password_entry.config(show='●')

    # Creating a checkbox
    var = IntVar()
    var.set('0')
    check = Checkbutton(login_frame, text='Show Password', onvalue=1, offvalue=0, variable=var, command=show_pass, anchor=CENTER)
    check.grid(row=7, column=1, sticky=E)

    # DONT HAVE AN ACCOUNT YET? SIGN UP HERE
    dhaay_label = Label(login_frame, text="Don't have an account yet? Sign up ", anchor=W)
    dhaay_label.grid(row=8, column=0, sticky=W, pady=(5, 0))
    def here_not_underlined(event=None):
        f = font.Font(here_label, here_label.cget("font"))
        f.configure(underline = False)
        here_label.configure(font=f)
    def here_underlined(event=None):
        f = font.Font(here_label, here_label.cget("font"))
        f.configure(underline = True)
        here_label.configure(font=f)
    def signup(event=None):
        login_frame.pack_forget()

        loading1()

    here_label = Label(login_frame, text="here.", fg='#007AFF', anchor=W)
    here_label.grid(row=8, column=0, pady=(5, 0), sticky=W, padx=(217, 0))
    here_label.bind('<Button-1>', signup)
    here_label.bind('<Leave>', here_not_underlined)
    here_label.bind('<Enter>', here_underlined)

login()

root.mainloop()
