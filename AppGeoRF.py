import tkinter as tk
from tkinter import ttk
import tkintermapview
from tkintermapview.canvas_position_marker import CanvasPositionMarker
import Data

db_string = "mongodb+srv://bdcrews:256168Apt@sandbox.xf5clle.mongodb.net/?retryWrites=true&w=majority"


class AppGeoRF(tk.Tk):
    def __init__(self):
        # Initialize the main window
        super().__init__()
           # Connection the database
        self.my_data = Data.DataSource(db_string)
        self.user_id = ""
        self.logged_in = False
        


        self.geometry("900x500")
        self.title("GeoRF")

        # App states
        self.current_marker = None
        self.current_marker_position = (0,0)
        self.search_results = list() # place to store the list buttons so they can be destroyed with subsequent searches.




     

        # Set up the menu
        self.top_menu = tk.Menu(self)
        self.config(menu=self.top_menu)

        self.file_menu = tk.Menu(self.top_menu)
        self.file_menu.add_command(label="Quit", command=self.destroy)

        self.help_menu = tk.Menu(self.top_menu)
        self.help_menu.add_command(label="About")

        self.top_menu.add_cascade(label="File", menu=self.file_menu)
        #self.top_menu.add_cascade(label="Help", menu=self.help_menu)

# Frames for layout
# Top Frame
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill="x")
      
# Middle Frame-------------      
        self.middle_frame = tk.Frame(self)


        self.middle_frame.pack(side=tk.TOP, fill="both", expand=True)
        
        self.search_frame = tk.Frame(self.middle_frame, width=200, padx=5, pady=5)
        self.search_frame.pack(side=tk.LEFT, fill="y")
        
        self.search_input = ttk.Entry(self.search_frame)
        self.search_input.pack(side = tk.TOP)

        self.marker_frame = tk.Frame(self.search_frame, height=100)
        self.marker_frame.pack(side=tk.BOTTOM)
        self.save_button = tk.Button(self.marker_frame, text="Save Marker", command = self.save_marker)
        self.save_button.pack(side=tk.BOTTOM)
        self.marker_coord_label = tk.Label(self.marker_frame)
        self.marker_coord_label.pack(side=tk.BOTTOM)



        self.search_button = ttk.Button(self.search_frame, name="search", text="Search", command = self.search_handler  )
        self.search_button.pack(side = tk.LEFT, anchor=tk.N, expand=True)

        self.map_view = tkintermapview.TkinterMapView(self.middle_frame)
        self.map_view.add_left_click_map_command(self.map_right_click)
        self.map_view.pack(fill="both", expand=True)

#Bottom Frame---------------
        self.bottom_frame = tk.Frame(self)


        #while self.logged_in != True:

        # make a login form and show it
        self.login_form = tk.Toplevel()
        self.login_form.geometry("400x300")
        self.login_form.columnconfigure(0, weight=1)
        self.login_form.columnconfigure(1, weight=1)
        tk.Label(self.login_form, text="ID:").pack(side=tk.TOP)
        self.lid = ttk.Entry(self.login_form)
        self.lid.pack(side=tk.TOP)
        tk.Label(self.login_form, text="PASSWORD:").pack(side=tk.TOP)
        self.lpw = ttk.Entry(self.login_form)
        self.lpw.pack(side=tk.TOP)
        tk.Button(self.login_form, text="Log In", command= lambda: self.login()).pack(side=tk.TOP)
        self.login_form.mainloop() # Show the login

        #Start the window
        self.mainloop()

    def map_right_click(self, coords): # The map was clicked
        self.current_marker:CanvasPositionMarker
       
        if self.current_marker != None:
            #print(self.current_marker)
            self.current_marker.delete()
            
        self.current_marker = self.map_view.set_marker(coords[0], coords[1], text=f"{coords[0]},{coords[1]}")
        self.current_marker_position = coords # save the coords for saving
        self.current_marker.click(self.marker_clicked)
        self.marker_coord_label['text'] = f"{coords[0]:.3f},{coords[1]:.3f}"


    def marker_clicked(self, coords):
         print(f"marker clicked: {coords}")

    def search_handler(self):
            search_string = self.search_input.get()
    
            
            # Clear the previous results
            for result in self.search_results:
                 result:tk.Button
                 result.destroy()
            self.search_results.clear()

            # Query the DB
            results = self.my_data.search_database("georf",f"{search_string}")
            #Iterate through the results, making a new button for each one.
            for result in results:

                button = tk.Button(self.search_frame, text= result["name"])
                self.search_results.append(button)
                button['command'] = lambda: self.result_clicked(result["name"][:]) 
                button.pack(side=tk.TOP)

                delete = tk.Button(self.search_frame, text="Delete", command= lambda: self.my_data.delete_record("georf", result["_id"] ))
                delete.pack(side=tk.TOP)
                self.search_results.append(delete)

                update = tk.Button(self.search_frame, text="Update", command= lambda: self.update_record(result["_id"])     )
                update.pack(side=tk.TOP)
                self.search_results.append(update)


    def save_marker(self):
        print(f"SAVING MARKER! {self.current_marker.position}")
        save_marker_popup = tk.Toplevel()
        save_marker_popup.geometry("400x300")
        save_marker_popup.columnconfigure(0, weight=1)
        save_marker_popup.columnconfigure(1, weight=1)
        
        #make the form
        tk.Label(save_marker_popup, text="Name").grid(column=0, row=0, sticky="w", padx=10)
        tk.Label(save_marker_popup, text="Range").grid(column=0, row=1, sticky="w", padx=10)
        tk.Label(save_marker_popup, text="Power").grid(column=0, row=2, sticky="w", padx=10)
        tk.Label(save_marker_popup, text="Upper Freq").grid(column=0, row=3, sticky="w", padx=10 )
        tk.Label(save_marker_popup, text="Lower Freq").grid(column=0, row=4, sticky="w", padx=10 )
        
        p_name = tk.Entry(save_marker_popup)
        p_name.grid(column=1,row=0)
        p_range = tk.Entry(save_marker_popup)
        p_range.grid(column=1,row=1)
        p_power = tk.Entry(save_marker_popup)
        p_power.grid(column=1,row=2)
        p_upper = tk.Entry(save_marker_popup)
        p_upper.grid(column=1,row=3)
        p_lower = tk.Entry(save_marker_popup)
        p_lower.grid(column=1,row=4)

        save_marker_popup.title("Save Station")
        tk.Button(save_marker_popup, text="Save", command=lambda: save_button_pushed()).grid(column=0, row=6)
        tk.Button(save_marker_popup, text="Cancel", command=lambda: save_marker_popup.destroy()).grid(column=1, row=6)

        def save_button_pushed():
             self.save_marker_record(p_name.get(), p_range.get(), p_power.get(), p_upper.get(), p_lower.get())
             save_marker_popup.destroy()
        
        save_marker_popup.mainloop()

    def result_clicked(self, event):
         print(f"Clicked a result! {event}")



    def save_marker_record(self, name, range, power, upper, lower): 
        new_record = {"name": name, "latitude": self.current_marker_position[0], "longitude": self.current_marker_position[1], "range": range, "power": power, "upper": upper, "lower": lower, "user": "bdcrews"}
        self.my_data.store_record("georf", new_record)

    

    def update_marker_record(self, id, name, range, power, upper, lower):
        new_record = {"$set": {"name": name, "range": range, "power": power, "upper": upper, "lower": lower, "user": "bdcrews"}}
        self.my_data.update_record("georf", id, new_record)




    def update_record(self, id):
        update_marker_popup = tk.Toplevel()
        update_marker_popup.geometry("400x300")
        update_marker_popup.columnconfigure(0, weight=1)
        update_marker_popup.columnconfigure(1, weight=1)
        
        #make the form
        tk.Label(update_marker_popup, text="Name").grid(column=0, row=0, sticky="w", padx=10)
        tk.Label(update_marker_popup, text="Range").grid(column=0, row=1, sticky="w", padx=10)
        tk.Label(update_marker_popup, text="Power").grid(column=0, row=2, sticky="w", padx=10)
        tk.Label(update_marker_popup, text="Upper Freq").grid(column=0, row=3, sticky="w", padx=10 )
        tk.Label(update_marker_popup, text="Lower Freq").grid(column=0, row=4, sticky="w", padx=10 )
        
        p_name = tk.Entry(update_marker_popup)
        p_name.grid(column=1,row=0)
        p_range = tk.Entry(update_marker_popup)
        p_range.grid(column=1,row=1)
        p_power = tk.Entry(update_marker_popup)
        p_power.grid(column=1,row=2)
        p_upper = tk.Entry(update_marker_popup)
        p_upper.grid(column=1,row=3)
        p_lower = tk.Entry(update_marker_popup)
        p_lower.grid(column=1,row=4)

        update_marker_popup.title("Update Station")
        tk.Button(update_marker_popup, text="Update", command=lambda: update_button_pushed()).grid(column=0, row=6)
        tk.Button(update_marker_popup, text="Cancel", command=lambda: update_marker_popup.destroy()).grid(column=1, row=6)

        def update_button_pushed():
             self.update_marker_record(id, p_name.get(), p_range.get(), p_power.get(), p_upper.get(), p_lower.get())
             update_marker_popup.destroy()

       

        update_marker_popup.mainloop()
         
    def login(self):
        if self.my_data.login("georf", self.lid.get(), self.lpw.get()) == True:
            self.logged_in = True # save the user
            self.user_id = self.lid.get()
            self.title(f"GeoRF - {self.user_id}")
            self.login_form.destroy()
        else:
             self.destroy()
        #self.login_form.destroy()

main_window = AppGeoRF() # Create the app window