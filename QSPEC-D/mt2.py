import customtkinter as ctk
import tkinter as tk
from PIL import Image
from functools import partial
import math
import numpy as np

class Quasi_GUI():

    def __init__(self):
        # System Theme Setting
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        # Setting the screen
        self.root = ctk.CTk()
        self.root.title("QSPEC-D (Materials Theory Team)")
        # self.root.iconbitmap("build/images/lab_logo.ico")
        # self.screen_width = self.root.winfo_screenwidth()
        # self.screen_height = self.root.winfo_screenheight()
        self.screen_width = 1200
        self.screen_height = 700


        self.root.geometry(f"{self.screen_width}x{self.screen_height}")




        # Parameters


        self.s_ind_list = []
        self.das = {}

        self.mode = None
        self.grid_check_var = ctk.BooleanVar(value=False)

        self.da_check_var = ctk.BooleanVar(value=False)
        self.dis_check_var = ctk.BooleanVar(value=False)
        self.Dope_check_var = ctk.BooleanVar(value=False)

        self.show_grid = False
        self.grid_type = "cubic"

        self.atom_radius = 15

        
        

        self.AUID = 1

        self.atoms = [[]]
        self.atoms_dic = {}

        self.anions = []

        self.atom_tags = []
        self.bonds = [[],[]]
        self.bond_tags = []
        self.selected_atom = None
        self.grid_items = []
        self.at_id = []
        
        self.stacking_list = ["1"]
        self.stacking_info_entry_var = ctk.StringVar()
        self.stacking_info_entry_var.set(self.stacking_list[0])







        # Frame Work

        self.header_frame = ctk.CTkFrame(self.root, fg_color="#27244d", height=40)
        self.header_frame.pack(fill="x")

        self.tools_frame = ctk.CTkFrame(self.root, fg_color="white", height=80, corner_radius=0)
        self.tools_frame.pack(fill="x")

        self.main_body_frame = ctk.CTkFrame(self.root)
        self.main_body_frame.pack(fill="both", expand=True)

        self.function_frame = ctk.CTkFrame(self.main_body_frame, fg_color="#c6c3e6", width=200, corner_radius=0)
        self.function_frame.pack(side="left", fill="y")

        self.canvas_frame = ctk.CTkFrame(self.main_body_frame, corner_radius=0)
        self.canvas_frame.pack(side = "left", fill="both", expand=True)




        

        

        # Header Space

        self.header_option_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent", width=200, height=35, corner_radius=0)
        self.header_option_frame.pack(side="left", pady=3, padx=5)

        self.header_file_btn = ctk.CTkButton(self.header_option_frame, fg_color="transparent", text="File", command=self.header_file_btn_fn, height=30, width=50, font=('Helvetica', 15, 'bold'), text_color="white")
        self.header_file_btn.pack(side="left", pady=3, padx=5)

        self.header_file_menu = tk.Menu(self.root, tearoff=0)
        self.header_file_menu.add_command(label="     New     ", command=self.new_file)
        self.header_file_menu.add_command(label="     Open    ", command=self.open_file)
        self.header_file_menu.add_command(label="     Save    ", command=self.save_file)
        self.header_file_menu.add_separator()  
        self.header_file_menu.add_command(label="     Exit    ", command=self.exit_app)


        self.header_calcu_btn = ctk.CTkButton(self.header_option_frame, fg_color="transparent", text="Calculation", command=self.header_calcu_btn_fn, height=30, width=50, font=('Helvetica', 15, 'bold'), text_color="white")
        self.header_calcu_btn.pack(side="left", pady=3, padx=5)
        



        # Tools space
        self.tool_select_text_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent", width=200, height=35, corner_radius=0)
        self.tool_select_text_frame.pack(side="right", pady=3, padx=5)

        self.tools_select_text = ctk.CTkLabel(self.tool_select_text_frame, text="Selected : ", font=('Helvetica', 15, 'bold'), text_color="white")
        self.tools_select_text.pack(side="left", padx=2, pady=2)

        self.tools_select_text_active = ctk.CTkLabel(self.tool_select_text_frame, width=100, text="", font=('Helvetica', 15, 'bold'), text_color="white")
        self.tools_select_text_active.pack(side="left", anchor="e")

        self.show_update_ind_btn = ctk.CTkButton(self.header_frame, text="Show Site Index", height=30, width=180, fg_color="#292454",
                                            hover_color="#695ecc",text_color="#ffffff", 
                                            corner_radius=10,  font=("Helvetica", 15, "bold"),
                                            command= self.show_update_ind_fn)
        self.show_update_ind_btn.pack(side="right", pady=7, padx=5)













        # Canvas Space

        self.canvas = ctk.CTkCanvas(self.canvas_frame,  bg="white", highlightthickness=5)
        # self.canvas.pack(fill="both", side="left", expand=True)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.canvas.bind("<Button-1>", self.click_on_canvas)

        # Add vertical scrollbar
        self.v_scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        # Add horizontal scrollbar
        self.h_scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure the canvas to use both scrollbars
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.canvas.configure(scrollregion=(0, 0, 2500, 2000))

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)














        # Function Space
        self.tool_grid_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent", corner_radius=0, border_color="black", border_width=2)
        self.tool_grid_frame.pack(side="left", padx=5, pady=5, fill="y")



        self.photo_add_atom =  ctk.CTkImage(dark_image=Image.open("build/images/add_atom.png"), size=(20,20))
        self.photo_clear_atom =  ctk.CTkImage(dark_image=Image.open("build/images/clear_atom.png"), size=(20,20))
        self.photo_add_bond =  ctk.CTkImage(dark_image=Image.open("build/images/add_bond.png"), size=(20,20))
        self.photo_add_nbbond =  ctk.CTkImage(dark_image=Image.open("build/images/add_nbbond.png"), size=(20,20))
        self.photo_remove_bond = ctk.CTkImage(dark_image=Image.open("build/images/remove_bond.png"), size=(20,20))
        self.photo_clear_canvas = ctk.CTkImage(dark_image=Image.open("build/images/clear_canvas.png"), size=(20,20))
        self.photo_donor = ctk.CTkImage(dark_image=Image.open("build/images/donor.png"), size=(20,20))
        self.photo_acceptor = ctk.CTkImage(dark_image=Image.open("build/images/acceptor.png"), size=(20,20))
        self.photo_arrow = ctk.CTkImage(dark_image=Image.open("build/images/arrow.png"), size=(20,20))

        self.clear_atom_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_add_atom, text="", fg_color="transparent", width=20, command=self.add_atom_fn).grid(row=0, column=0, padx=2, pady=2)
        self.add_atom_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_clear_atom, text="", fg_color="transparent", width=20, command=self.clear_atom_fn).grid(row=0, column=1, padx=2, pady=2)
        self.add_bond_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_add_bond, text="", fg_color="transparent", width=20, command=self.add_bond_fn).grid(row=0, column=2, padx=2, pady=2)
        self.add_nbbond_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_add_nbbond, text="", fg_color="transparent", width=20, command=self.add_nbbond_fn).grid(row=0, column=3, padx=2, pady=2)
        self.clear_canvas_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_clear_canvas, text="", fg_color="transparent", width=20, command=self.clear_canvas_fn).grid(row=1, column=0, padx=2, pady=2)
        self.donor_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_donor, text="", fg_color="transparent", width=20, command=self.donor_fn).grid(row=1, column=1, padx=2, pady=2)
        self.acceptor_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_acceptor, text="", fg_color="transparent", width=20, command=self.acceptor_fn).grid(row=1, column=2, padx=2, pady=2)
        self.remove_bond_btn = ctk.CTkButton(self.tool_grid_frame, image=self.photo_remove_bond, text="", fg_color="transparent", width=20, command=self.remove_bond_fn).grid(row=1, column=3, padx=2, pady=2)



        self.tools_setting_frame = ctk.CTkFrame(self.tools_frame, fg_color="white", height=70, corner_radius=0, border_color="#27244d", border_width=2)
        self.tools_setting_frame.pack(side="left",fill='y', padx=5, pady=5)

        self.tools_setting_frame1 = ctk.CTkFrame(self.tools_setting_frame, fg_color="white", height=70)
        self.tools_setting_frame1.pack(side="left",fill='y', padx=2, pady=2)

        self.grid_spacing_label = ctk.CTkLabel(self.tools_setting_frame1, text='Grid Spacing', font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=0, padx=2, pady=2)
        self.grid_spacing_entry = ctk.CTkEntry(self.tools_setting_frame1, state="normal",fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=75)
        self.grid_spacing_entry.grid(row=0, column=1, padx=2, pady=2)
        self.grid_spacing_entry.insert(0, "80")


        self.atom_radius_label = ctk.CTkLabel(self.tools_setting_frame1, text='Site Radius', font=('Helvetica', 12, 'bold'), text_color="black").grid(row=1, column=0, padx=2, pady=2)
        self.atom_radius_entry = ctk.CTkEntry(self.tools_setting_frame1, state="normal",fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=75)
        self.atom_radius_entry.grid(row=1, column=1, padx=2, pady=2)
        self.atom_radius_entry.insert(0, "20")

        self.tools_setting_frame2 = ctk.CTkFrame(self.tools_setting_frame, fg_color="white")
        self.tools_setting_frame2.pack(side="left",fill='y', padx=2, pady=2)
        
        self.add_grid_check = ctk.CTkCheckBox(self.tools_setting_frame2, text="Show grid", variable=self.grid_check_var, font=('Helvetica', 12, 'bold'), text_color="black", command=self.toggle_grid)
        self.add_grid_check.grid(row=1, column=1, padx=2, pady=2)
        self.grid_type_btn = ctk.CTkButton(self.tools_setting_frame2, text=f"Cubic", font=('Helvetica', 12, 'bold'), text_color="white", width=75, command=self.toggle_grid_type)
        self.grid_type_btn.grid(row=1, column=2, padx=2, pady=2)

        self.bond_length_label = ctk.CTkLabel(self.tools_setting_frame2, text='Bond Length', font=('Helvetica', 12, 'bold'), text_color="black").grid(row=2, column=1, padx=2, pady=2)
        self.bond_length_entry = ctk.CTkEntry(self.tools_setting_frame2, state="normal",fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=75)
        self.bond_length_entry.grid(row=2, column=2, padx=2, pady=2)
        self.bond_length_entry.insert(0, "0.4")







        self.tools_frame2 = ctk.CTkFrame(self.function_frame, fg_color="#c6c3e6", height=300, corner_radius=0, border_color="#27244d", border_width=2)

        self.EP_check_var = ctk.BooleanVar()
        # self.EP_coupling_label = ctk.CTkLabel(self.function_frame, text="Activate Electron-\nPhonon Coupling",
        #                                       font=('Helvetica', 12, 'bold'), text_color="black").grid(row=1, column=0,
        #                                                                                                padx=5, pady=5)
        self.EP_coupling_chk = ctk.CTkCheckBox(self.tools_frame2, text="Activate Electron-Phonon Coupling",
                                               variable=self.EP_check_var, font=('Helvetica', 12, 'bold'), text_color="black")
        self.EP_coupling_chk.pack(anchor='nw',padx=5, pady=5)


        self.tools_frame2.pack(fill='x', padx=5, pady=5)

        self.tools_frame21 = ctk.CTkFrame(self.tools_frame2, fg_color="#c6c3e6", height=300, corner_radius=0)
        self.tools_frame21.pack(fill='x', padx=5, pady=5)



        self.max_part_label = ctk.CTkLabel(self.tools_frame21, text="Basis Set", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=0, padx=5, pady=5)

        self.max_part_list = ["One Particle", "Two Particles", "Three Particles"]
        self.max_part_optn = ctk.CTkOptionMenu(self.tools_frame21,
                                            values=self.max_part_list,
                                            fg_color="gray30",
                                            button_color="teal",
                                            button_hover_color="cyan",
                                            dropdown_fg_color="gray20",
                                            dropdown_text_color="white",
                                            dropdown_hover_color="teal",
                                            width=130
                            )
        self.max_part_optn.grid(row=0, column=1, padx=5, pady=5)




        self.max_vib_label = ctk.CTkLabel(self.tools_frame21, text="Choose Maximum \nNumber of \nVibration", font=('Helvetica', 12, 'bold'),text_color="black").grid(row=2, column=0, padx=5, pady=5)

        self.max_vib_list = ["0", "1", "2", "3", "4", "5", "6"]
        self.max_vib_optn = ctk.CTkOptionMenu(self.tools_frame21,
                                            values=self.max_vib_list,
                                            fg_color="gray30",
                                            button_color="teal",
                                            button_hover_color="cyan",
                                            dropdown_fg_color="gray20",
                                            dropdown_text_color="white",
                                            dropdown_hover_color="teal",
                                            width=130
                            )
        self.max_vib_optn.grid(row=2, column=1, padx=5, pady=4)

        self.stacking_info_frame = ctk.CTkFrame(self.tools_frame, fg_color="#c6c3e6", height=220, corner_radius=0, border_color="#27244d", border_width=2)
        self.stacking_info_frame.pack(side="left",fill='y', padx=5, pady=5)
        self.stacking_info_label = ctk.CTkLabel(self.stacking_info_frame, text="Stacking", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=0, padx=5, pady=5)


        
        self.stacking_down_btn = ctk.CTkButton(self.stacking_info_frame, text="↓", height=30, width=30, fg_color="#292454",
                                            hover_color="#695ecc",text_color="#ffffff", 
                                            corner_radius=30, font=("Helvetica", 12, "bold"),
                                            command= self.stacking_down_fn)
        self.stacking_down_btn.grid(row=0, column=1, padx=2, pady=5)

        self.stacking_info_entry = ctk.CTkEntry(self.stacking_info_frame,
                                            textvariable=self.stacking_info_entry_var,
                                            width=40,
                                            fg_color="gray30",
                                            justify="center",
                                            state="disabled")
        self.stacking_info_entry.grid(row=0, column=2, padx=2, pady=5)

        self.stacking_up_btn = ctk.CTkButton(self.stacking_info_frame, text="↑", height=30, width=30, fg_color="#292454",
                                            hover_color="#695ecc",text_color="#ffffff", 
                                            corner_radius=30, font=("Helvetica", 12, "bold"),
                                            command= self.stacking_up_fn)
        self.stacking_up_btn.grid(row=0, column=3, padx=2, pady=5)

        self.stacking_add_btn = ctk.CTkButton(self.stacking_info_frame, text="+", height=30, width=40, fg_color="#292454",
                                            hover_color="#695ecc",text_color="#ffffff", 
                                            corner_radius=10, font=("Helvetica", 12, "bold"),
                                            command= self.stacking_add_fn)
        self.stacking_add_btn.grid(row=0, column=4, padx=5, pady=5)

        self.stacking_remove_btn = ctk.CTkButton(self.stacking_info_frame, text="-", height=30, width=40, fg_color="#292454",
                                            hover_color="#695ecc",text_color="#ffffff", 
                                            corner_radius=10, font=("Helvetica", 12, "bold"),
                                            command= self.stacking_remove_fn)
        self.stacking_remove_btn.grid(row=0, column=5, padx=5, pady=5)



# **************************************************************************

        self.tools_frame_op1 = ctk.CTkFrame(self.function_frame, fg_color="#c6c3e6", height=350, corner_radius=0, border_color="#27244d", border_width=2)
        self.tools_frame_op1.pack(fill='x', padx=5, pady=5, ipady=5)


        self.disorder_check = ctk.CTkCheckBox(self.tools_frame_op1, text="Activate Inhomogeneous Site Disorder", variable=self.dis_check_var, font=('Helvetica', 12, 'bold'), text_color="black", command=self.dis_check_toggle)
        self.disorder_check.pack(anchor="se", padx=5, pady=5, fill="x")

        self.dis_info_frame = ctk.CTkFrame(self.tools_frame_op1, fg_color="#c6c3e6", height=350, corner_radius=0)
        self.dis_info_frame.pack(padx=5, fill="x")

        self.dis_sig_label = ctk.CTkLabel(self.dis_info_frame, text="Disorder Width\n(σ)", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=0, padx=5, pady=2)

        self.dis_sig_entry = ctk.CTkEntry(self.dis_info_frame, fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=120, justify="center")
        self.dis_sig_entry.grid(row=0, column=1, padx=5, pady=2)
        self.dis_sig_entry.insert(0, "0.35")
        self.dis_sig_entry.configure(state="disabled")

        self.num_config_label = ctk.CTkLabel(self.dis_info_frame, text="Max Disorder \nConfigurations", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=1, column=0, padx=5, pady=2)

        self.num_config_entry = ctk.CTkEntry(self.dis_info_frame, fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=120, justify="center")
        self.num_config_entry.grid(row=1, column=1, padx=5, pady=2)
        self.num_config_entry.insert(0, "1")
        self.num_config_entry.configure(state="disabled")

        self.num_core_label = ctk.CTkLabel(self.dis_info_frame, text="Number of \nCores", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=2, column=0, padx=5, pady=2)

        self.num_core_entry = ctk.CTkEntry(self.dis_info_frame, fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=120, justify="center")
        self.num_core_entry.grid(row=2, column=1, padx=5, pady=2)
        self.num_core_entry.insert(0, "1")
        self.num_core_entry.configure(state="disabled")



        self.tools_frame_op2 = ctk.CTkFrame(self.function_frame, fg_color="#c6c3e6", height=350, corner_radius=0, border_color="#27244d", border_width=2)
        self.tools_frame_op2.pack(fill='x', padx=5, pady=5, ipady=5)

        self.Dopeing_check = ctk.CTkCheckBox(self.tools_frame_op2, text="Activate Electrostatics", variable=self.Dope_check_var, font=('Helvetica', 12, 'bold'), text_color="black", command=self.Dope_check_toggle)
        self.Dopeing_check.pack(anchor="se", padx=5, pady=5, fill="x")

        self.tools_frame_op4 = ctk.CTkFrame(self.tools_frame_op2, fg_color="#c6c3e6", height=350, corner_radius=0)
        self.tools_frame_op4.pack(fill='x', padx=12, pady=2, ipady=2)

        self.add_e_btn = ctk.CTkButton(self.tools_frame_op4, text="Add Anion", font=('Helvetica', 12, 'bold'),
                                       text_color="black", fg_color="#ffb357", command=self.add_e_fn, width=100)
        self.add_e_btn.grid(row=0, column=0, padx=5, pady=5)

        self.remove_e_btn = ctk.CTkButton(self.tools_frame_op4, text="Remove Anion", font=('Helvetica', 12, 'bold'),
                                          text_color="black", fg_color="#57fff1", command=self.remove_e_fn, width=100)
        self.remove_e_btn.grid(row=0, column=1, padx=5, pady=5)

        self.tools_frame_op3 = ctk.CTkFrame(self.tools_frame_op2, fg_color="#c6c3e6", height=350, corner_radius=0)
        self.tools_frame_op3.pack(fill='x', padx=12, pady=2, ipady=2)


        self.x_e_l = ctk.CTkLabel(self.tools_frame_op3, text="X", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=1, padx=5, pady=1)
        self.y_e_l = ctk.CTkLabel(self.tools_frame_op3, text="Y", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=2, padx=5, pady=1)
        self.z_e_l = ctk.CTkLabel(self.tools_frame_op3, text="Z", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=0, column=3, padx=5, pady=1)
        self.text_l = ctk.CTkLabel(self.tools_frame_op3, text="Coordinate", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=1, column=0, padx=5, pady=1)

        self.x_e_en = ctk.CTkEntry(self.tools_frame_op3, fg_color="white", state="disabled", font=('Helvetica', 12, 'bold'), text_color="black", width=50, justify="center")
        self.x_e_en.grid(row=1, column=1, padx=1, pady=1)

        self.y_e_en = ctk.CTkEntry(self.tools_frame_op3, fg_color="white", state="disabled", font=('Helvetica', 12, 'bold'), text_color="black", width=50, justify="center")
        self.y_e_en.grid(row=1, column=2, padx=1, pady=1)

        self.z_e_en = ctk.CTkEntry(self.tools_frame_op3, fg_color="white", state="disabled", font=('Helvetica', 12, 'bold'), text_color="black", width=50, justify="center")
        self.z_e_en.grid(row=1, column=3, padx=1, pady=1)







        self.tools_frame_op6 = ctk.CTkFrame(self.function_frame, fg_color="#c6c3e6", height=350, corner_radius=0,
                                            border_color="#27244d", border_width=2)
        self.tools_frame_op6.pack(fill='x', padx=5, pady=5, ipady=5)

        self.cTIntegral_l = ctk.CTkLabel(self.tools_frame_op6, text="Choose Charge Transfer Integrals",
                                             font=('Helvetica', 12, 'bold'),
                                             text_color="black")
        self.cTIntegral_l.pack(anchor="se", padx=5, pady=5, fill="x")

        self.tools_frame_op5 = ctk.CTkFrame(self.tools_frame_op6, fg_color="#c6c3e6", height=350, corner_radius=0)
        self.tools_frame_op5.pack(fill='x', padx=12, pady=2, ipady=2)

        self.cTBond_l = ctk.CTkLabel(self.tools_frame_op5, text="Through Bond",
                                             font=('Helvetica', 12, 'bold'),
                                             text_color="black").grid(row=0, column=0, padx=5, pady=5)

        self.cTSpace_l = ctk.CTkLabel(self.tools_frame_op5, text="Through Space",
                                     font=('Helvetica', 12, 'bold'),
                                     text_color="black").grid(row=0, column=1, padx=5, pady=5)

        self.cTBond_e = ctk.CTkEntry(self.tools_frame_op5, fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=120, justify="center")
        self.cTBond_e.grid(row=1, column=0, padx=5, pady=5)
        self.cTBond_e.insert(0, '0.30')

        self.cTSpace_e = ctk.CTkEntry(self.tools_frame_op5, fg_color="white",
                                     font=('Helvetica', 12, 'bold'), text_color="black", width=120, justify="center")
        self.cTSpace_e.grid(row=1, column=1, padx=5, pady=5)
        self.cTSpace_e.insert(0, '0.15')




        

        










        # Function Space 2

        




    
        
        self.root.mainloop()


    # All Functions

    def add_e_fn(self):
        self.mode = "add_anion"
        self.tools_select_text_active.configure(text="Add Anion")
        if self.atom_radius_entry.get() == "":
            self.atom_radius = 20
        else:
            self.atom_radius = float(self.atom_radius_entry.get())
        self.selected_atm_p()

    def remove_e_fn(self):
        self.mode = "clear_anion"
        self.tools_select_text_active.configure(text="Clear Anion")
        self.selected_atm_p()

    def toggle_grid_type(self):
        if self.grid_type_btn.cget("text") == "Cubic":
            self.grid_type = "hexagon"
            self.grid_type_btn.configure(text="Hexagonal")
        else:
            self.grid_type = "cubic"
            self.grid_type_btn.configure(text="Cubic")

    def header_calcu_btn_fn(self):
        calc_atoms_dic = self.atoms_dic
        calc_atoms = self.atoms
        calc_bonds = self.bonds
        calc_das = self.das
        calc_max_vib = self.max_vib_optn.get()
        calc_if_da = self.da_check_var.get()
        calc_if_dis = self.dis_check_var.get()
        calc_stacking =  self.stacking_info_entry.get()
        calc_gridlen = self.grid_spacing_entry.get()
        calc_atomrad = self.atom_radius_entry.get()
        calc_blen = self.bond_length_entry.get()
        calc_num_core = self.num_core_entry.get()
        calc_config = self.num_config_entry.get()
        calc_maxpart = self.max_part_optn.get()
        calc_sigma = self.dis_sig_entry.get()
        calc_if_Dope = "TRUE" if self.x_e_en.get() != "" else "FALSE"
        calc_Dopeing = [float(self.x_e_en.get()), float(self.y_e_en.get()), float(self.z_e_en.get())] if self.x_e_en.get() != "" else [None, None, None]

        new_calc_dic = {}
        new_calc_atoms_dic = {}
        new_calc_atoms = []
        new_calc_bonds = [[],[]]
        new_calc_das = {}

        cnt = 1
        for l in range(len(calc_atoms)):
            arr = self.atoms[l]
            new_arr = []
            for at in arr:
                new_calc_dic[f"{at}"] = cnt
                new_arr.append(cnt)
                new_calc_das[f"{cnt}"] = calc_das[f"{at}"]
                new_calc_atoms_dic[f"{cnt}"] = calc_atoms_dic[f"{at}"]

                cnt += 1
            new_calc_atoms.append(new_arr)

        for k in calc_bonds[0]:
            new_calc_bonds[0].append((new_calc_dic[f"{k[0]}"], new_calc_dic[f"{k[1]}"]))

        for k in calc_bonds[1]:
            new_calc_bonds[1].append((new_calc_dic[f"{k[0]}"], new_calc_dic[f"{k[1]}"]))


        self.atoms_dic = new_calc_atoms_dic
        self.atoms = new_calc_atoms
        self.bonds = new_calc_bonds
        self.das = new_calc_das


        class SetupCalWin():
            
            def __init__(self,
                        calc_atoms_dic,
                        calc_atoms,
                        calc_bonds,
                        calc_das,
                        calc_max_vib,
                        calc_if_dis,
                        calc_if_da,
                        calc_stacking,
                        calc_gridlen,
                        calc_atomrad,
                        calc_blen,
                        calc_num_core,
                        calc_config,
                        calc_maxpart,
                        calc_sigma,
                        calc_if_Dope,
                        calc_Dopeing
                         ):
                ctk.set_appearance_mode("system")
                ctk.set_default_color_theme("dark-blue")

                # Setting the screen
                self.root = ctk.CTk()
                self.root.title("Calculation Setup")
                # self.root.iconbitmap("build/images/lab_logo.ico")
                self.screen_width = 1000
                self.screen_height = 750
                self.root.geometry(f"{self.screen_width}x{self.screen_height}")


                # param

                self.vs_active = "bond"

                self.calc_atoms_dic = calc_atoms_dic
                self.calc_atoms = calc_atoms
                self.calc_bonds = calc_bonds
                self.calc_das = calc_das
                self.calc_max_vib = calc_max_vib
                self.calc_if_dis = calc_if_dis
                self.calc_if_da = calc_if_da
                self.calc_stacking = len(self.calc_atoms)
                self.calc_gridlen = calc_gridlen
                self.calc_atomrad = calc_atomrad
                self.calc_blen = calc_blen
                self.calc_num_core = calc_num_core
                self.calc_config = calc_config
                self.calc_maxpart = calc_maxpart
                self.calc_sigma = calc_sigma
                self.da_vals = [-0.3, -0.15, 0, 0, 0, 0, 0]
                self.calc_Dopeing = calc_Dopeing
                self.calc_if_Dope = calc_if_Dope





                # Info space

                self.info_space_frame = ctk.CTkFrame(self.root, fg_color="#d6d6d6", height=100, corner_radius=0)
                self.info_space_frame.pack(anchor="nw", fill="x")

                self.nparticle_lable = ctk.CTkLabel(self.info_space_frame, text="Sites", text_color="black", font=("Helvetica", 12, "bold"))
                self.nparticle_lable.grid(row=0, column=0, padx=5, pady=5)

                npval = 0
                for i in self.calc_atoms:
                    npval += len(i)

                self.nparticle_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.nparticle_entry.grid(row=0, column=1, padx=5, pady=5)
                self.nparticle_entry.insert(0, f"{npval}")
                self.nparticle_entry.configure(state="disabled")

                self.nbonds_lable = ctk.CTkLabel(self.info_space_frame, text="Couplings", text_color="black", font=("Helvetica", 12, "bold"))
                self.nbonds_lable.grid(row=1, column=0, padx=5, pady=5)

                bval = len(self.calc_bonds[0])
                nbval = len(self.calc_bonds[1])

                self.nbonds_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.nbonds_entry.grid(row=1, column=1, padx=5, pady=5)
                self.nbonds_entry.insert(0, f"{bval}-{nbval}")
                self.nbonds_entry.configure(state="disabled")

                self.aparticle_lable = ctk.CTkLabel(self.info_space_frame, text="Basis Set", text_color="black", font=("Helvetica", 12, "bold"))
                self.aparticle_lable.grid(row=0, column=2, padx=5, pady=5)

                self.aparticle_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=110)
                self.aparticle_entry.grid(row=0, column=3, padx=5, pady=5)
                self.aparticle_entry.insert(0, self.calc_maxpart)
                self.aparticle_entry.configure(state="disabled") 


                self.nvib_lable = ctk.CTkLabel(self.info_space_frame, text="Max Vibration", text_color="black", font=("Helvetica", 12, "bold"))
                self.nvib_lable.grid(row=1, column=2, padx=5, pady=5)

                self.nvib_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.nvib_entry.grid(row=1, column=3, padx=5, pady=5)
                self.nvib_entry.insert(0, self.calc_max_vib)
                self.nvib_entry.configure(state="disabled") 


                self.aDA_lable = ctk.CTkLabel(self.info_space_frame, text="DA Activate", text_color="black", font=("Helvetica", 12, "bold"))
                self.aDA_lable.grid(row=0, column=4, padx=5, pady=5)

                daval = "TRUE" if self.calc_if_da else "FALSE"

                self.aDA_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.aDA_entry.grid(row=0, column=5, padx=5, pady=5)
                self.aDA_entry.insert(0, daval)
                self.aDA_entry.configure(state="disabled") 

                self.disorder_lable = ctk.CTkLabel(self.info_space_frame, text="Disorder", text_color="black", font=("Helvetica", 12, "bold"))
                self.disorder_lable.grid(row=1, column=4, padx=5, pady=5)

                disval = "TRUE" if self.calc_if_dis else "FALSE"

                self.disorder_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.disorder_entry.grid(row=1, column=5, padx=5, pady=5)
                self.disorder_entry.insert(0, disval)
                self.disorder_entry.configure(state="disabled") 

                self.nstack_lable = ctk.CTkLabel(self.info_space_frame, text="Stacking", text_color="black", font=("Helvetica", 12, "bold"))
                self.nstack_lable.grid(row=0, column=6, padx=5, pady=5)

                self.nstack_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.nstack_entry.grid(row=0, column=7, padx=5, pady=5)
                self.nstack_entry.insert(0, self.calc_stacking)
                self.nstack_entry.configure(state="disabled") 

                self.blength_lable = ctk.CTkLabel(self.info_space_frame, text="Bond Length", text_color="black", font=("Helvetica", 12, "bold"))
                self.blength_lable.grid(row=1, column=6, padx=5, pady=5)

                self.blength_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.blength_entry.grid(row=1, column=7, padx=5, pady=5)
                self.blength_entry.insert(0, self.calc_blen)
                self.blength_entry.configure(state="disabled") 


                self.ncore_lable = ctk.CTkLabel(self.info_space_frame, text="Number of Core", text_color="black", font=("Helvetica", 12, "bold"))
                self.ncore_lable.grid(row=0, column=8, padx=5, pady=5)

                self.ncore_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.ncore_entry.grid(row=0, column=9, padx=5, pady=5)
                self.ncore_entry.insert(0, self.calc_num_core)
                self.ncore_entry.configure(state="disabled") 

                self.nconfig_lable = ctk.CTkLabel(self.info_space_frame, text="Disorder Config.", text_color="black", font=("Helvetica", 12, "bold"))
                self.nconfig_lable.grid(row=1, column=8, padx=5, pady=5)

                self.nconfig_entry = ctk.CTkEntry(self.info_space_frame, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=80)
                self.nconfig_entry.grid(row=1, column=9, padx=5, pady=5)
                self.nconfig_entry.insert(0, self.calc_config)
                self.nconfig_entry.configure(state="disabled") 

                self.set_calc_btn = ctk.CTkButton(self.info_space_frame, text="SETUP", text_color="white", font=("Helvetica", 12, "bold"), width=80, command=self.set_calc_fn)
                self.set_calc_btn.grid(row=1, column=10, padx=5, pady=5)



                self.bb1 = ctk.CTkFrame(self.root, fg_color="white", height=2, corner_radius=0)
                self.bb1.pack(anchor="nw", fill="x")

                self.visual_space_frame = ctk.CTkFrame(self.root, fg_color="#9cf7d0", height=30, corner_radius=0)
                self.visual_space_frame.pack(anchor="nw", fill="x")

                self.vs_edit_bond_btn = ctk.CTkButton(self.visual_space_frame, text="Edit Bond", fg_color="#b163ff", corner_radius=0, width=100, text_color="black", font=("Helvetica", 12, "bold"), command=self.vs_bond_toggle_fn)
                self.vs_edit_bond_btn.pack(side="left", fill="y", padx=5)


                self.vs_da_sys_btn = ctk.CTkButton(self.visual_space_frame, text="DA System", fg_color="#9cf7d0", corner_radius=0, width=100, text_color="black", font=("Helvetica", 12, "bold"), command=self.vs_da_toggle_fn)
                self.vs_da_sys_btn.pack(side="left", fill="y", padx=5)


                self.vs_dis_sys_btn = ctk.CTkButton(self.visual_space_frame, text="Disorder", fg_color="#9cf7d0", corner_radius=0, width=100, text_color="black", font=("Helvetica", 12, "bold"), command=self.vs_dis_toggle_fn)
                self.vs_dis_sys_btn.pack(side="left", fill="y", padx=5)





                self.rb1 = ctk.CTkFrame(self.root, fg_color="#b163ff", height=4, corner_radius=0)
                self.rb1.pack(anchor="nw", fill="x")


                self.main_body_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=0)
                self.main_body_frame.pack(anchor="nw", fill="both", expand=True)


                self.widgets = []


                self.vs_body_fn()




















                self.root.mainloop()



            def clear_widgets(self):
                for widget in self.widgets:
                    widget.destroy()
                self.widgets.clear()


            def vs_bondedit_fn(self):
                self.clear_widgets()


                self.vs_bondedit_fn_frame = ctk.CTkFrame(self.main_body_frame, fg_color="white", corner_radius=0)
                self.vs_bondedit_fn_frame.pack(side="left", fill="both", expand=True)
                self.widgets.append(self.vs_bondedit_fn_frame)

                self.calc_canv_frame = ctk.CTkFrame(self.vs_bondedit_fn_frame, width=250, fg_color="white", corner_radius=0)
                self.calc_canv_frame.pack(side="left", fill="y")

                self.calc_canv_frame1 = ctk.CTkFrame(self.calc_canv_frame, width=250, fg_color="white", corner_radius=0, height=300, border_color="black", border_width=5)
                self.calc_canv_frame1.pack(anchor="n", padx=5, pady=5)

                self.calc_canv_frame2 = ctk.CTkFrame(self.calc_canv_frame, width=250, fg_color="white", corner_radius=0, height=300, border_color="black", border_width=5)
                self.calc_canv_frame2.pack(anchor="s", padx=5, pady=5)

                self.bonding_label = ctk.CTkLabel(self.calc_canv_frame1, text="Through Bond Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).pack(padx=5, pady=5)
                self.nbonding_label = ctk.CTkLabel(self.calc_canv_frame2, text="Through Space Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).pack(padx=5, pady=5)


                self.calc_canv_b = ctk.CTkCanvas(self.calc_canv_frame1, width=250, bg="white", height=250)
                self.calc_canv_b.pack(side="left", fill="y",padx=5, pady=5)

                self.calc_canv_nb = ctk.CTkCanvas(self.calc_canv_frame2, width=250, bg="white", height=250)
                self.calc_canv_nb.pack(side="left", fill="y",padx=5, pady=5)

                self.calc_canv_b_scroll = ctk.CTkScrollbar(self.calc_canv_frame1, orientation="vertical", command=self.calc_canv_b.yview)
                self.calc_canv_b_scroll.pack(side="left", fill="y", padx=5, pady=5)

                self.calc_canv_nb_scroll = ctk.CTkScrollbar(self.calc_canv_frame2, orientation="vertical", command=self.calc_canv_nb.yview)
                self.calc_canv_nb_scroll.pack(side="left", fill="y", padx=5, pady=5)

                

                self.bonding_frame = ctk.CTkFrame(self.calc_canv_b, width=250, fg_color="white", corner_radius=0, height=250)
                self.calc_canv_b.create_window((0, 0), window=self.bonding_frame, anchor="nw")
                self.calc_canv_b.configure(yscrollcommand=self.calc_canv_b_scroll.set)
                cnt = 1

                for i in new_calc_bonds[0]:
                    ctk.CTkLabel(self.bonding_frame, text=f"{cnt}.", text_color="black", font=("Helvetica", 12, "bold")).grid(row=cnt, column=0, padx=5, pady=5)
                    ctk.CTkLabel(self.bonding_frame, text=f"< {i[0]} >", text_color="black", font=("Helvetica", 12, "bold")).grid(row=cnt, column=1, padx=5, pady=5)
                    ctk.CTkLabel(self.bonding_frame, text=f"< {i[1]} >", text_color="black", font=("Helvetica", 12, "bold")).grid(row=cnt, column=2, padx=5, pady=5)
                    cnt += 1


                self.bonding_frame.update_idletasks()
                self.calc_canv_b.config(scrollregion=self.calc_canv_b.bbox("all"))



                self.nbonding_frame = ctk.CTkFrame(self.calc_canv_nb, width=250, fg_color="white", corner_radius=0, height=250)
                self.calc_canv_nb.create_window((0, 0), window=self.nbonding_frame, anchor="nw")
                self.calc_canv_nb.configure(yscrollcommand=self.calc_canv_nb_scroll.set)
                cnt = 1

                for i in new_calc_bonds[1]:
                    ctk.CTkLabel(self.nbonding_frame, text=f"{cnt}.", text_color="black", font=("Helvetica", 12, "bold")).grid(row=cnt, column=0, padx=5, pady=5)
                    ctk.CTkLabel(self.nbonding_frame, text=f"< {i[0]} >", text_color="black", font=("Helvetica", 12, "bold")).grid(row=cnt, column=1, padx=5, pady=5)
                    ctk.CTkLabel(self.nbonding_frame, text=f"< {i[1]} >", text_color="black", font=("Helvetica", 12, "bold")).grid(row=cnt, column=2, padx=5, pady=5)
                    cnt += 1


                self.nbonding_frame.update_idletasks()
                self.calc_canv_nb.config(scrollregion=self.calc_canv_nb.bbox("all"))


                self.edit_bond_frame = ctk.CTkFrame(self.vs_bondedit_fn_frame, fg_color="white", corner_radius=0)
                self.edit_bond_frame.pack(side="left", fill="both", expand=True)

                self.edit_bond_frame1 = ctk.CTkFrame(self.edit_bond_frame, fg_color="white", corner_radius=0)
                self.edit_bond_frame1.pack(anchor="nw", padx=5, pady=5)

                self.add_b_label = ctk.CTkLabel(self.edit_bond_frame1, text="Add Through Bond Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=0, column=0, padx=5, pady=5)
                self.add_nb_label = ctk.CTkLabel(self.edit_bond_frame1, text="Add Through Space Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=1, column=0, padx=5, pady=5)
                self.remove_b_label = ctk.CTkLabel(self.edit_bond_frame1, text="Remove Through Bond Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=2, column=0, padx=5, pady=5)
                self.remove_nb_label = ctk.CTkLabel(self.edit_bond_frame1, text="Remove Through Space Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=3, column=0, padx=5, pady=5)

                self.add_b_e1 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.add_b_e1.grid(row=0, column=1, padx=5, pady=5)
                self.add_nb_e1 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.add_nb_e1.grid(row=1, column=1, padx=5, pady=5)
                self.remove_b_e1 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.remove_b_e1.grid(row=2, column=1, padx=5, pady=5)
                self.remove_nb_e1 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.remove_nb_e1.grid(row=3, column=1, padx=5, pady=5)

                self.add_b_e2 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.add_b_e2.grid(row=0, column=2, padx=5, pady=5)
                self.add_nb_e2 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.add_nb_e2.grid(row=1, column=2, padx=5, pady=5)
                self.remove_b_e2 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.remove_b_e2.grid(row=2, column=2, padx=5, pady=5)
                self.remove_nb_e2 = ctk.CTkEntry(self.edit_bond_frame1, fg_color="white", text_color="black", font=("Helvetica", 12, "bold"), width=40)
                self.remove_nb_e2.grid(row=3, column=2, padx=5, pady=5)

                self.add_b_btn = ctk.CTkButton(self.edit_bond_frame1, text="Add", text_color="white", font=("Helvetica", 12, "bold"), width=40, command=self.add_b_fn)
                self.add_b_btn.grid(row=0, column=3, padx=5, pady=5)
                self.add_nb_btn = ctk.CTkButton(self.edit_bond_frame1, text="Add", text_color="white", font=("Helvetica", 12, "bold"), width=40, command=self.add_nb_fn)
                self.add_nb_btn.grid(row=1, column=3, padx=5, pady=5)
                self.remove_b_btn = ctk.CTkButton(self.edit_bond_frame1, text="Remove", text_color="white", font=("Helvetica", 12, "bold"), width=40, command=self.remove_b_fn)
                self.remove_b_btn.grid(row=2, column=3, padx=5, pady=5)
                self.remove_nb_btn = ctk.CTkButton(self.edit_bond_frame1, text="Remove", text_color="white", font=("Helvetica", 12, "bold"), width=40, command=self.remove_nb_fn)
                self.remove_nb_btn.grid(row=3, column=3, padx=5, pady=5)
                

                


            def add_b_fn(self):
                a = self.add_b_e1.get()
                b = self.add_b_e2.get()
                if a != "" and b != "":
                    if a != b:
                        self.calc_bonds[0].append((min([int(a), int(b)]), max([int(a), int(b)])))
                        self.vs_body_fn()

            def add_nb_fn(self):
                a = self.add_nb_e1.get()
                b = self.add_nb_e2.get()
                if a != "" and b != "":
                    if a != b:
                        self.calc_bonds[1].append((min([int(a), int(b)]), max([int(a), int(b)])))
                        self.vs_body_fn()

            def remove_b_fn(self):
                a = self.remove_b_e1.get()
                b = self.remove_b_e2.get()
                if a != "" and b != "":
                    if a != b:
                        c = (min([int(a), int(b)]), max([int(a), int(b)]))
                        if c in self.calc_bonds[0]:
                            self.calc_bonds[0].remove(c)
                            self.vs_body_fn()

            def remove_nb_fn(self):
                a = self.remove_nb_e1.get()
                b = self.remove_nb_e2.get()
                if a != "" and b != "":
                    if a != b:
                        c = (min([int(a), int(b)]), max([int(a), int(b)]))
                        if c in self.calc_bonds[1]:
                            self.calc_bonds[1].remove(c)
                            self.vs_body_fn()


            def vs_da_fn(self):
                self.clear_widgets()

                self.vs_da_fn_frame = ctk.CTkFrame(self.main_body_frame, fg_color="white", corner_radius=0)
                self.vs_da_fn_frame.pack(side="left", fill="both", expand=True)
                self.widgets.append(self.vs_da_fn_frame)

                if self.aDA_entry.get() == "TRUE":
                    self.da_check_var = ctk.BooleanVar(value=True)
                else:
                    self.da_check_var = ctk.BooleanVar(value=False)

                self.da_check = ctk.CTkCheckBox(self.vs_da_fn_frame, text="Donor Acceptor Activate", variable=self.da_check_var, font=('Helvetica', 10, 'bold'), text_color="black", command=self.da_check_toggle)
                self.da_check.pack(anchor="se", padx=5,pady=5, fill="x")

                self.da_primary_f = ctk.CTkFrame(self.vs_da_fn_frame, fg_color="white", corner_radius=0, height=400, border_color="black", border_width=2)
                self.da_primary_f.pack(fill="x", padx=5, pady=5)

                self.da_widgets = []
                







                self.da_check_toggle()


            def nDA_fn(self):
                self.da_primary_f1 = ctk.CTkFrame(self.da_primary_f, fg_color="white", corner_radius=0, height=400)
                self.da_primary_f1.pack(fill="x", padx=5, pady=5)
                self.da_widgets.append(self.da_primary_f1)

                self.ddb_coup_l1 = ctk.CTkLabel(self.da_primary_f1, text="D-D Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=0, column=0, padx=5, pady=5)
                self.ddnb_coup_l1 = ctk.CTkLabel(self.da_primary_f1, text="D-D Non Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=1, column=0, padx=5, pady=5)

                self.ddb_coup_e1 = ctk.CTkEntry(self.da_primary_f1, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.ddb_coup_e1.grid(row=0, column=1, padx=5, pady=5)
                self.ddnb_coup_e1 = ctk.CTkEntry(self.da_primary_f1, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.ddnb_coup_e1.grid(row=1, column=1, padx=5, pady=5)

                self.ddb_coup_se1 = ctk.CTkEntry(self.da_primary_f1, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.ddb_coup_se1.grid(row=0, column=2, padx=5, pady=5)
                self.ddnb_coup_se1 = ctk.CTkEntry(self.da_primary_f1, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.ddnb_coup_se1.grid(row=1, column=2, padx=5, pady=5)

                self.nda_update_btn = ctk.CTkButton(self.da_primary_f1, text="UPDATE", text_color="white", font=("Helvetica", 12, "bold"), command=self.nda_update_fn)
                self.nda_update_btn.grid(row=1, column=3, padx=5, pady=5)




            def yDA_fn(self):
                self.da_primary_f2 = ctk.CTkFrame(self.da_primary_f, fg_color="white", corner_radius=0, height=400)
                self.da_primary_f2.pack(fill="x", padx=5, pady=5)
                self.da_widgets.append(self.da_primary_f2)

                self.ddb_coup_l2 = ctk.CTkLabel(self.da_primary_f2, text="D-D Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=0, column=0, padx=5, pady=5)
                self.ddnb_coup_l2 = ctk.CTkLabel(self.da_primary_f2, text="D-D Non Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=1, column=0, padx=5, pady=5)
                self.aab_coup_l2 = ctk.CTkLabel(self.da_primary_f2, text="A-A Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=2, column=0, padx=5, pady=5)
                self.aanb_coup_l2 = ctk.CTkLabel(self.da_primary_f2, text="A-A Non Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=3, column=0, padx=5, pady=5)
                self.dab_coup_l2 = ctk.CTkLabel(self.da_primary_f2, text="D-A Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=4, column=0, padx=5, pady=5)
                self.danb_coup_l2 = ctk.CTkLabel(self.da_primary_f2, text="D-A Non Bonding Coupling", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=5, column=0, padx=5, pady=5)

                self.ddb_coup_e2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.ddb_coup_e2.grid(row=0, column=1, padx=5, pady=5)
                self.ddnb_coup_e2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.ddnb_coup_e2.grid(row=1, column=1, padx=5, pady=5)
                self.aab_coup_e2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.aab_coup_e2.grid(row=2, column=1, padx=5, pady=5)
                self.aanb_coup_e2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.aanb_coup_e2.grid(row=3, column=1, padx=5, pady=5)
                self.dab_coup_e2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.dab_coup_e2.grid(row=4, column=1, padx=5, pady=5)
                self.danb_coup_e2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="white")
                self.danb_coup_e2.grid(row=5, column=1, padx=5, pady=5)

                self.ddb_coup_se2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.ddb_coup_se2.grid(row=0, column=2, padx=5, pady=5)
                self.ddnb_coup_se2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.ddnb_coup_se2.grid(row=1, column=2, padx=5, pady=5)
                self.aab_coup_se2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.aab_coup_se2.grid(row=2, column=2, padx=5, pady=5)
                self.aanb_coup_se2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.aanb_coup_se2.grid(row=3, column=2, padx=5, pady=5)
                self.dab_coup_se2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.dab_coup_se2.grid(row=4, column=2, padx=5, pady=5)
                self.danb_coup_se2 = ctk.CTkEntry(self.da_primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=250, fg_color="#d6d6d6", state="disabled")
                self.danb_coup_se2.grid(row=5, column=2, padx=5, pady=5)

                self.da_energy_label = ctk.CTkLabel(self.da_primary_f2, text="D-A Energy diffrence", font=('Helvetica', 12, 'bold'), text_color="black").grid(row=6, column=0, padx=5, pady=5)

                self.da_energy_entry = ctk.CTkEntry(self.da_primary_f2, fg_color="white", font=('Helvetica', 12, 'bold'), text_color="black", width=250)
                self.da_energy_entry.grid(row=6, column=1, padx=5, pady=5)

                self.da_energy_sentry = ctk.CTkEntry(self.da_primary_f2, state="disabled", font=('Helvetica', 12, 'bold'), text_color="black", width=250, fg_color="#d6d6d6")
                self.da_energy_sentry.grid(row=6, column=2, padx=5, pady=5)

                self.yda_update_btn = ctk.CTkButton(self.da_primary_f2, text="UPDATE", text_color="white", font=("Helvetica", 12, "bold"), command=self.yda_update_fn)
                self.yda_update_btn.grid(row=6, column=3, padx=5, pady=5)



            def yda_update_fn(self):
                self.ddb_coup_se2.configure(state="normal")
                self.ddnb_coup_se2.configure(state="normal")
                self.aab_coup_se2.configure(state="normal")
                self.aanb_coup_se2.configure(state="normal")
                self.dab_coup_se2.configure(state="normal")
                self.danb_coup_se2.configure(state="normal")
                self.da_energy_sentry.configure(state="normal")

                if self.ddb_coup_e2.get() != "":
                    self.ddb_coup_se2.delete(0, "end")
                    self.ddb_coup_se2.insert(0, self.ddb_coup_e2.get())
                else:
                    self.ddb_coup_se2.delete(0, "end")
                    self.ddb_coup_se2.insert(0, str(self.da_vals[0]))
                if self.ddnb_coup_e2.get() != "":
                    self.ddnb_coup_se2.delete(0, "end")
                    self.ddnb_coup_se2.insert(0, self.ddnb_coup_e2.get())
                else:
                    self.ddnb_coup_se2.delete(0, "end")
                    self.ddnb_coup_se2.insert(0, str(self.da_vals[1]))
                if self.aab_coup_e2.get() != "":
                    self.aab_coup_se2.delete(0, "end")
                    self.aab_coup_se2.insert(0, self.aab_coup_e2.get())
                else:
                    self.aab_coup_se2.delete(0, "end")
                    self.aab_coup_se2.insert(0, str(self.da_vals[2]))
                if self.aanb_coup_e2.get() != "":
                    self.aanb_coup_se2.delete(0, "end")
                    self.aanb_coup_se2.insert(0, self.aanb_coup_e2.get())
                else:
                    self.aanb_coup_se2.delete(0, "end")
                    self.aanb_coup_se2.insert(0, str(self.da_vals[3]))
                if self.dab_coup_e2.get() != "":
                    self.dab_coup_se2.delete(0, "end")
                    self.dab_coup_se2.insert(0, self.dab_coup_e2.get())
                else:
                    self.dab_coup_se2.delete(0, "end")
                    self.dab_coup_se2.insert(0, str(self.da_vals[4]))
                if self.danb_coup_e2.get() != "":
                    self.danb_coup_se2.delete(0, "end")
                    self.danb_coup_se2.insert(0, self.danb_coup_e2.get())
                else:
                    self.danb_coup_se2.delete(0, "end")
                    self.danb_coup_se2.insert(0, str(self.da_vals[5]))
                if self.da_energy_entry.get() != "":
                    self.da_energy_sentry.delete(0, "end")
                    self.da_energy_sentry.insert(0, self.da_energy_entry.get())
                else:
                    self.da_energy_sentry.delete(0, "end")
                    self.da_energy_sentry.insert(0, str(self.da_vals[6]))

                self.ddb_coup_se2.configure(state="disabled")
                self.ddnb_coup_se2.configure(state="disabled")
                self.aab_coup_se2.configure(state="disabled")
                self.aanb_coup_se2.configure(state="disabled")
                self.dab_coup_se2.configure(state="disabled")
                self.danb_coup_se2.configure(state="disabled")
                self.da_energy_sentry.configure(state="disabled")

                self.da_vals[0] = float(self.ddb_coup_se2.get()) if self.ddb_coup_se2.get() != "" else 0
                self.da_vals[1] = float(self.ddnb_coup_se2.get()) if self.ddnb_coup_se2.get() != "" else 0
                self.da_vals[2] = float(self.aab_coup_se2.get()) if self.aab_coup_se2.get() != "" else 0
                self.da_vals[3] = float(self.aanb_coup_se2.get()) if self.aanb_coup_se2.get() != "" else 0
                self.da_vals[4] = float(self.dab_coup_se2.get()) if self.dab_coup_se2.get() != "" else 0
                self.da_vals[5] = float(self.danb_coup_se2.get()) if self.danb_coup_se2.get() != "" else 0
                self.da_vals[6] = float(self.da_energy_sentry.get()) if self.da_energy_sentry.get() != "" else 0

            def nda_update_fn(self):
                self.ddb_coup_se1.configure(state="normal")
                self.ddnb_coup_se1.configure(state="normal")

                if self.ddb_coup_e1.get() != "":
                    self.ddb_coup_se1.delete(0, "end")
                    self.ddb_coup_se1.insert(0, self.ddb_coup_e1.get())
                if self.ddnb_coup_e1.get() != "":
                    self.ddnb_coup_se1.delete(0, "end")
                    self.ddnb_coup_se1.insert(0, self.ddnb_coup_e1.get())

                self.ddb_coup_se1.configure(state="disabled")
                self.ddnb_coup_se1.configure(state="disabled")

                self.da_vals[0] = float(self.ddb_coup_se1.get()) if self.ddb_coup_se1.get() != "" else 0
                self.da_vals[1] = float(self.ddnb_coup_se1.get()) if self.ddnb_coup_se1.get() != "" else 0
                print(self.da_vals)


            def da_check_toggle(self):
                for da_widget in self.da_widgets:
                    da_widget.destroy()
                self.da_widgets = []

                if self.da_check.get():
                    self.aDA_entry.configure(state="normal")
                    self.aDA_entry.delete(0, "end")
                    self.aDA_entry.insert(0, "TRUE")
                    self.aDA_entry.configure(state="disabled")

                    self.yDA_fn()

                else:
                    self.aDA_entry.configure(state="normal")
                    self.aDA_entry.delete(0, "end")
                    self.aDA_entry.insert(0, "FALSE")
                    self.aDA_entry.configure(state="disabled")

                    self.nDA_fn()





            def vs_dis_fn(self):
                self.clear_widgets()

                self.vs_dis_fn_frame = ctk.CTkFrame(self.main_body_frame, fg_color="white", corner_radius=0)
                self.vs_dis_fn_frame.pack(side="left", fill="both", expand=True)
                self.widgets.append(self.vs_dis_fn_frame)

                # if self.disorder_entry.get() == "TRUE":

                # self.disorder_check = ctk.CTkCheckBox(self.vs_dis_fn_frame, text="Disorder Activate", variable=self.dis_check_var, font=('Helvetica', 10, 'bold'), text_color="black", command=self.dis_check_toggle)
                # self.disorder_check.pack(anchor="se", padx=5, pady=5, fill="x")

                # self.primary_f = ctk.CTkFrame(self.vs_dis_fn_frame, fg_color="white", corner_radius=0, height=400, border_color="black", border_width=2)
                # self.primary_f.pack(fill="x", padx=5, pady=5)
                #
                # self.inhomDis_check_var = ctk.BooleanVar()
                # self.disorder_check_inhom = ctk.CTkCheckBox(self.primary_f, text="Activate Inhomogeneous Disorder", variable=self.inhomDis_check_var, font=('Helvetica', 12, 'bold'), text_color="black", command=self.dis_check_toggle)
                # self.disorder_check_inhom.grid(row=0, column=0, padx=5, pady=5)
                #
                # self.sig_l = ctk.CTkLabel(self.primary_f, text="Disorder Width\n(σ)", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=1, column=0, padx=5, pady=5)
                # self.config_l = ctk.CTkLabel(self.primary_f, text="Number of \nDisorder\nConfiguration", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=2, column=0, padx=5, pady=5)
                # self.num_core_l = ctk.CTkLabel(self.primary_f, text="Number of Core", text_color="black", font=("Helvetica", 12, "bold"), width=250).grid(row=3, column=0, padx=5, pady=5)
                #
                # self.sig_e = ctk.CTkEntry(self.primary_f, text_color="black", font=("Helvetica", 12, "bold"), width=110, fg_color="white")
                # self.sig_e.grid(row=1, column=1, padx=5, pady=5)
                # self.config_e = ctk.CTkEntry(self.primary_f, text_color="black", font=("Helvetica", 12, "bold"), width=110, fg_color="white")
                # self.config_e.grid(row=2, column=1, padx=5, pady=5)
                # self.num_core_e = ctk.CTkEntry(self.primary_f, text_color="black", font=("Helvetica", 12, "bold"), width=110, fg_color="white")
                # self.num_core_e.grid(row=3, column=1, padx=5, pady=5)
                #
                # self.dis_update_btn = ctk.CTkButton(self.primary_f, text="Update", text_color="white", font=("Helvetica", 12, "bold"), width=40, command=self.dis_update_fn)
                # self.dis_update_btn.grid(row=3, column=2, padx=5, pady=5)



                self.primary_f2 = ctk.CTkFrame(self.vs_dis_fn_frame, fg_color="white", corner_radius=0, height=400,
                                              border_color="black", border_width=2)
                self.primary_f2.pack(fill="x", padx=5, pady=5)

                self.paraCrys_chk_var = ctk.BooleanVar()
                self.dis_paraCrys_chk = ctk.CTkCheckBox(self.primary_f2, text="Activate Paracrystallinity",
                                                            variable=self.paraCrys_chk_var,
                                                            font=('Helvetica', 12, 'bold'), text_color="black")
                self.dis_paraCrys_chk.grid(row=0, column=0, padx=5, pady=5)




                self.vacDef_chk_var = ctk.BooleanVar()
                self.dis_vacDef_chk = ctk.CTkCheckBox(self.primary_f2, text="Activate Vacancy Defect",
                                                        variable=self.vacDef_chk_var,
                                                        font=('Helvetica', 12, 'bold'), text_color="black")
                self.dis_vacDef_chk.grid(row=1, column=0, padx=5, pady=5)

                self.numVacSite_l = ctk.CTkLabel(self.primary_f2, text="Number of missing Sites", text_color="black",
                                                 font=("Helvetica", 12, "bold"), width=250).grid(row=1, column=1,
                                                                                                padx=5, pady=5)

                self.numVacSite_e = ctk.CTkEntry(self.primary_f2, text_color="black", font=("Helvetica", 12, "bold"), width=110,
                                          fg_color="white")
                self.numVacSite_e.grid(row=1, column=2, padx=5, pady=5)

                self.vacDef_corre_chk_var = ctk.BooleanVar()
                self.dis_vacDef_corr_chk = ctk.CTkCheckBox(self.primary_f2, text="Correlated Disorder",
                                                      variable=self.vacDef_corre_chk_var,
                                                      font=('Helvetica', 12, 'bold'), text_color="black")
                self.dis_vacDef_corr_chk.grid(row=1, column=3, padx=5, pady=5)










                self.lincDef_chk_var = ctk.BooleanVar()
                self.dis_linkDef_chk = ctk.CTkCheckBox(self.primary_f2, text="Activate Linker Defect",
                                                        variable=self.lincDef_chk_var,
                                                        font=('Helvetica', 12, 'bold'), text_color="black")
                self.dis_linkDef_chk.grid(row=2, column=0, padx=5, pady=5)

                self.numlinkDef_l = ctk.CTkLabel(self.primary_f2, text="Number of missing Linkers", text_color="black",
                                                 font=("Helvetica", 12, "bold"), width=250).grid(row=2, column=1,
                                                                                                 padx=5, pady=5)

                self.numlinkDef_e = ctk.CTkEntry(self.primary_f2, text_color="black", font=("Helvetica", 12, "bold"),
                                                 width=110,
                                                 fg_color="white")
                self.numlinkDef_e.grid(row=2, column=2, padx=5, pady=5)

                self.linkDef_corre_chk_var = ctk.BooleanVar()
                self.dis_linkDef_corr_chk = ctk.CTkCheckBox(self.primary_f2, text="Correlated Disorder",
                                                      variable=self.linkDef_corre_chk_var,
                                                      font=('Helvetica', 12, 'bold'), text_color="black")
                self.dis_linkDef_corr_chk.grid(row=2, column=3, padx=5, pady=5)

                self.primF2_update_btn = ctk.CTkButton(self.primary_f2, text="Update", text_color="white",
                                                    font=("Helvetica", 12, "bold"), width=40,
                                                    command=self.dis_update_fn)
                self.primF2_update_btn.grid(row=2, column=4, padx=5, pady=5)



















                self.dis_check_toggle()



            def dis_update_fn(self):
                if self.sig_e.get() != "":
                    self.calc_sigma = self.sig_e.get()
                    self.sig_e.delete(0, "end")
                
                if self.config_e.get() != "":
                    self.nconfig_entry.configure(state="normal")
                    self.nconfig_entry.delete(0, "end")
                    self.nconfig_entry.insert(0, self.config_e.get())
                    self.nconfig_entry.configure(state="disabled")
                    self.config_e.delete(0, "end")

                if self.num_core_e.get() != "":
                    self.ncore_entry.configure(state="normal")
                    self.ncore_entry.delete(0, "end")
                    self.ncore_entry.insert(0, self.num_core_e.get())
                    self.ncore_entry.configure(state="disabled")
                    self.num_core_e.delete(0, "end")



            def dis_check_toggle(self):
                if self.disorder_entry.get() == "TRUE":
                    self.disorder_entry.configure(state="normal")
                    self.disorder_entry.delete(0, "end")
                    self.disorder_entry.insert(0, "TRUE")
                    self.disorder_entry.configure(state="disabled")

                    self.config_e.configure(state="normal")
                    self.num_core_e.configure(state="normal")
                    self.sig_e.configure(state="normal")
                else:
                    self.disorder_entry.configure(state="normal")
                    self.disorder_entry.delete(0, "end")
                    self.disorder_entry.insert(0, "FALSE")
                    self.disorder_entry.configure(state="disabled")

                    self.config_e.configure(state="disabled")
                    self.num_core_e.configure(state="disabled")
                    self.sig_e.configure(state="disabled")


            def vs_body_fn(self):
                if self.vs_active == "bond":
                    self.vs_bondedit_fn()
                elif self.vs_active == "da":
                    self.vs_da_fn()
                elif self.vs_active == "dis":
                    self.vs_dis_fn()



            def vs_bond_toggle_fn(self):
                if self.vs_active != "bond":
                    self.vs_edit_bond_btn.configure(fg_color="#b163ff")
                    self.vs_da_sys_btn.configure(fg_color="#9cf7d0")
                    self.vs_dis_sys_btn.configure(fg_color="#9cf7d0")
                    self.vs_active = "bond"
                    self.vs_body_fn()





            def vs_da_toggle_fn(self):
                if self.vs_active != "da":
                    self.vs_edit_bond_btn.configure(fg_color="#9cf7d0")
                    self.vs_da_sys_btn.configure(fg_color="#b163ff")
                    self.vs_dis_sys_btn.configure(fg_color="#9cf7d0")
                    self.vs_active = "da"
                    self.vs_body_fn()








            def vs_dis_toggle_fn(self):
                if self.vs_active != "dis":
                    self.vs_edit_bond_btn.configure(fg_color="#9cf7d0")
                    self.vs_da_sys_btn.configure(fg_color="#9cf7d0")
                    self.vs_dis_sys_btn.configure(fg_color="#b163ff")
                    self.vs_active = "dis"
                    self.vs_body_fn()


            def set_calc_fn(self):
                file_path = tk.filedialog.asksaveasfilename(
                    title="Save File As",
                    defaultextension=".qp",
                    filetypes=[("QP file", "*.qp"), ("All files", "*.*")]
                )
                if file_path:
                    with open(file_path, "w") as file:
                        cnt_dic = {}
                        file.write("\n")
                        file.write("     Grid Space and Atom Rad     \n")
                        file.write("\n")
                        
                        file.write(f"      Grid Space           {self.calc_gridlen}\n")
                        file.write(f"      Atom Radious         {self.calc_atomrad}\n")
                        file.write(f"      Length of Bonds      {self.calc_blen}\n")
                        
                        file.write("             \n")
                        file.write("\n")
                        file.write("     Other Calculation Information     \n")
                        file.write("\n")

                
                        file.write(f"      Number of Particle   {len(self.calc_das)}\n")
                        file.write(f"      Number of Bonds      {self.nbonds_entry.get()}\n")
                        file.write(f"      Max Vibration        {self.calc_max_vib}\n")
                        file.write(f"      Activated Particle   {self.aparticle_entry.get()}\n")



                        file.write("             \n")
                        file.write("\n")
                        file.write("     Co-ordinates     \n")
                        file.write("\n")
                        cnt = 1

                        for l in range(len(self.calc_atoms)):
                            arr = self.calc_atoms[l]
                            for at in arr:
                                file.write(f"      {cnt}      {'D' if self.calc_das[f'{at}'] == 1 else 'A'}     {((int(self.calc_atoms_dic[f'{at}'][0]) - int(self.calc_atoms_dic[f'{1}'][0])) * float(self.calc_blen) / int(self.calc_gridlen)):.3f}     {((int(self.calc_atoms_dic[f'{at}'][1]) - int(self.calc_atoms_dic[f'{1}'][1])) * float(self.calc_blen) / int(self.calc_gridlen)):.3f}     {f'{l+1}'}\n")
                                cnt_dic[f"{at}"] = cnt
                                cnt += 1

                        file.write("             \n")
                        file.write("\n")
                        file.write("     Bonding Connectivity     \n")
                        file.write("\n")

                        for l in range(len(self.calc_atoms)):
                            arr = self.calc_atoms[l]
                            for at in arr:
                                txt = ""
                                for barr in self.calc_bonds[0]:
                                    if at in barr:
                                        if at == barr[0]:
                                            txt += f"{cnt_dic[f'{barr[1]}']}  "
                                        else:
                                            txt += f"{cnt_dic[f'{barr[0]}']}  "
                                if txt != "":
                                    file.write(f"      {cnt_dic[f'{at}']}     {txt}\n")
                        
                        file.write("\n")

                        for l in range(len(self.calc_atoms)):
                            arr = self.calc_atoms[l]
                            for at in arr:
                                txt = ""
                                for barr in self.calc_bonds[1]:
                                    if at in barr:
                                        if at == barr[0]:
                                            txt += f"{cnt_dic[f'{barr[1]}']}  "
                                        else:
                                            txt += f"{cnt_dic[f'{barr[0]}']}  "
                                if txt != "":
                                    file.write(f"      {cnt_dic[f'{at}']}     {txt}\n")
                                                



                        file.write("             \n")
                        file.write("\n")
                        file.write("     Disorder Information     \n")
                        file.write("\n")

                        file.write(f"      Disorder Activate    {self.disorder_entry.get()}\n")
                        file.write(f"      Number of Nodes      {self.calc_num_core}\n")
                        file.write(f"      Max Configurations   {self.calc_config}\n")
                        file.write(f"      Disorder Width       {self.calc_sigma}\n")
                        file.write("\n")
                        file.write(f"      Random Bond Breaking       {self.calc_sigma}\n")
                        file.write(f"      B-B Percentage      {self.calc_sigma}\n")

                        file.write("             \n")
                        file.write("\n")
                        file.write("     Donor-Acceptor System Information     \n")
                        file.write("\n")

                        file.write(f"      D-A Activate     {self.aDA_entry.get()}\n")
                        file.write(f"      D-D     {self.da_vals[0]}     {self.da_vals[1]}\n")
                        file.write(f"      A-A     {self.da_vals[2]}     {self.da_vals[3]}\n")
                        file.write(f"      D-A     {self.da_vals[4]}     {self.da_vals[5]}\n")
                        file.write(f"      Energy Difference     {self.da_vals[6]}\n")

                        file.write("             \n")
                        file.write("\n")
                        file.write("     Doping System Information     \n")
                        file.write("\n")

                        file.write(f"      Doping Activate     {self.calc_if_Dope}\n")
                        file.write(f"      X position     {(self.calc_Dopeing[0] * float(self.calc_blen) / int(self.calc_gridlen)):.3f}\n")
                        file.write(f"      Y position     {(self.calc_Dopeing[1] * float(self.calc_blen) / int(self.calc_gridlen)):.3f}\n")
                        file.write(f"      Z position     {(self.calc_Dopeing[2] * float(self.calc_blen) / int(self.calc_gridlen)):.3f}\n")


                        






                        file.write("             \n")

                    print(f"File saved as: {file_path}")







            def del_this(self):
                self.root.destroy()

        self.scal = SetupCalWin(
                        new_calc_atoms_dic,
                        new_calc_atoms,
                        new_calc_bonds,
                        new_calc_das,
                        calc_max_vib,
                        calc_if_dis,
                        calc_if_da,
                        calc_stacking,
                        calc_gridlen,
                        calc_atomrad,
                        calc_blen,
                        calc_num_core,
                        calc_config,
                        calc_maxpart,
                        calc_sigma,
                        calc_if_Dope,
                        calc_Dopeing)



    def header_file_btn_fn(self):
        x = self.header_file_btn.winfo_rootx()
        y = self.header_file_btn.winfo_rooty() + self.header_file_btn.winfo_height()
        self.header_file_menu.tk_popup(x, y)

    def new_file(self):
        print("New File selected")
        pass

    def open_file(self):

        file_path = tk.filedialog.askopenfilename(
            title="Open File",
            defaultextension=".crd",
            filetypes=[("CRD file", "*.crd"), ("All files", "*.*")]
        )
        self.clear_canvas_fn()
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                file_list = file_content.split("             ")
                atomic_grid = file_list[0].split("\n")[3:-1]
                atomic_chord = file_list[1].split("\n")[4:-1]
                atomic_bonding = file_list[2].split("\n")[4:-1]
                ind_blank = atomic_bonding.index('')
                a_bonding = atomic_bonding[:ind_blank]
                a_nbonding = atomic_bonding[ind_blank+1:]

                grid = atomic_grid[0].split(" ")
                grid = int([item for item in grid if item != ''][-1])

                ar_rd = atomic_grid[1].split(" ")
                ar_rd = int([item for item in ar_rd if item != ''][-1])
                
                self.atom_radius_entry.delete(0, "end")
                self.atom_radius_entry.insert(0, f"{ar_rd}")

                for atext in atomic_chord:
                    atl = atext.split(" ")
                    atl = [item for item in atl if item != '']
                    
                    self.atoms_dic[f"{atl[0]}"] = (float(atl[2]), float(atl[3]))
                    if atl[1] == "D":
                        self.das[f"{atl[0]}"] = 1
                    else:
                        self.das[f"{atl[0]}"] = -1
                    
                    if int(atl[-1]) != len(self.atoms):
                        self.atoms.append([])
                        self.atoms[int(atl[-1])-1].append(int(atl[0]))
                    else:
                        self.atoms[int(atl[-1])-1].append(int(atl[0]))

                for i in range(1, len(self.atoms)):
                    self.stacking_list.append(f"{i+1}")


                for btext in a_bonding:
                    bbl = btext.split(" ")
                    bbl = [item for item in bbl if item != '']
                    
                    for i in range(1, len(bbl)):
                        barr = (int(bbl[0]), int(bbl[i]))
                        if (min(barr), max(barr)) not in self.bonds[0]:
                            self.bonds[0].append((min(barr), max(barr)))

                for btext in a_nbonding:
                    bbl = btext.split(" ")
                    bbl = [item for item in bbl if item != '']
                    
                    for i in range(1, len(bbl)):
                        barr = (int(bbl[0]), int(bbl[i]))
                        if (min(barr), max(barr)) not in self.bonds[1]:
                            self.bonds[1].append((min(barr), max(barr)))
                


                

                self.grid_spacing_entry.delete(0, "end")
                self.grid_spacing_entry.insert(0, f"{grid}")
                self.st_val_update_screen() 
            
            


    def save_file(self):
        file_path = tk.filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=".crd",
            filetypes=[("CRD file", "*.crd"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                cnt_dic = {}
                file.write("\n")
                file.write("     Grid Space and Atom Rad     \n")
                file.write("\n")
                
                file.write(f"      Grid Space    {self.grid_spacing_entry.get()}\n")
                file.write(f"      Atom Radious    {self.atom_radius_entry.get()}\n")

                file.write("             \n")
                file.write("\n")
                file.write("     Co-ordinates     \n")
                file.write("\n")
                cnt = 1
                for l in range(len(self.atoms)):
                    arr = self.atoms[l]
                    for at in arr:
                        file.write(f"      {cnt}      {'D' if self.das[f'{at}'] == 1 else 'A'}     {self.atoms_dic[f'{at}'][0]}     {self.atoms_dic[f'{at}'][1]}     {f'{l+1}'}\n")
                        cnt_dic[f"{at}"] = cnt
                        cnt += 1

                file.write("             \n")
                file.write("\n")
                file.write("     Bonding Connectivity     \n")
                file.write("\n")

                for l in range(len(self.atoms)):
                    arr = self.atoms[l]
                    for at in arr:
                        txt = ""
                        for barr in self.bonds[0]:
                            if at in barr:
                                if at == barr[0]:
                                    txt += f"{cnt_dic[f'{barr[1]}']}  "
                                else:
                                    txt += f"{cnt_dic[f'{barr[0]}']}  "
                        if txt != "":
                            file.write(f"      {cnt_dic[f'{at}']}     {txt}\n")
                
                file.write("\n")

                for l in range(len(self.atoms)):
                    arr = self.atoms[l]
                    for at in arr:
                        txt = ""
                        for barr in self.bonds[1]:
                            if at in barr:
                                if at == barr[0]:
                                    txt += f"{cnt_dic[f'{barr[1]}']}  "
                                else:
                                    txt += f"{cnt_dic[f'{barr[0]}']}  "
                        if txt != "":
                            file.write(f"      {cnt_dic[f'{at}']}     {txt}\n")
                                        



                file.write("             \n")
            print(f"File saved as: {file_path}")


    def exit_app(self):
        self.root.destroy()



    def add_atom_fn(self):
        self.mode = "add_atom"
        self.tools_select_text_active.configure(text="Add Site")
        if self.atom_radius_entry.get() == "":
            self.atom_radius = 20
        else:
            self.atom_radius = float(self.atom_radius_entry.get())
        self.selected_atm_p()


    def clear_atom_fn(self):
        self.mode = "clear_atom"
        self.tools_select_text_active.configure(text="Remove Site")
        self.selected_atm_p()


    def add_bond_fn(self):
        self.mode = "add_bond"
        self.tools_select_text_active.configure(text="Bonding Coupling")
        self.selected_atm_p()

    def add_nbbond_fn(self):
        self.mode = "add_nbbond"
        self.tools_select_text_active.configure(text="Space Coupling")
        self.selected_atm_p()


    def remove_bond_fn(self):
        self.mode = "remove_bond"
        self.tools_select_text_active.configure(text="Remove Coupling")
        self.selected_atm_p()


    def clear_canvas_fn(self):
        cle_response = tk.messagebox.askyesno("Confirm Clear", "Are you sure you want to clear?")
        if cle_response:
            self.mode = None
            self.tools_select_text_active.configure(text="")
            self.canvas.delete("all")
            self.draw_grid()
            self.atoms = [[]]
            self.atoms_dic = {}
            self.bonds = [[],[]]
            self.das = {}
            self.at_id = []
            self.anions = []
            self.selected_atom = None
            self.AUID = 1
            self.stacking_list = ["1"]
            self.stacking_info_entry_var.set(self.stacking_list[0])


    def donor_fn(self):
        self.mode = "donor"
        self.tools_select_text_active.configure(text="Donor")
        self.selected_atm_p()


    def acceptor_fn(self):
        self.mode = "acceptor"
        self.tools_select_text_active.configure(text="Acceptor")
        self.selected_atm_p()


    def arrow_fn(self):
        self.mode = "arrow"
        self.tools_select_text_active.configure(text="Arrow")
        self.selected_atm_p()


    def to_hex(self, x_val, y_val, x_g, y_g, c_g):
        xx = None
        yy = None
        if y_val % 2 != 0:
            if (y_val+1) % 4 == 0:
                if x_val % 2 == 0:
                    xx = x_val * x_g
                    yy = (y_val * y_g) + c_g

                else:
                    xx = x_val * x_g
                    yy = (y_val * y_g) - c_g
            else:
                if x_val % 2 == 0:
                    xx = x_val * x_g
                    yy = (y_val * y_g) - c_g

                else:
                    xx = x_val * x_g
                    yy = (y_val * y_g) + c_g
        else:
            xx = x_val * x_g
            yy = y_val * y_g
        
        if xx != None and yy != None:
            return xx, yy


   
    

    def draw_grid(self):
        self.canvas.delete("grid")
        if self.grid_spacing_entry.get() == "":
            self.grid_spacing = 80
        else:
            self.grid_spacing = int(self.grid_spacing_entry.get())

        if self.show_grid:
            if self.grid_type == "cubic":
                for x in range(0, 2500, self.grid_spacing):
                    self.grid_items.append(self.canvas.create_line(x, 0, x, 2000, fill="gray", tags="grid"))
                for y in range(0, 2000, self.grid_spacing):
                    self.grid_items.append(self.canvas.create_line(0, y, 2500, y, fill="gray", tags="grid"))
            
            elif self.grid_type == "hexagon":
                c_g = math.sin(math.radians(30)) * self.grid_spacing / 2
                x_g = math.cos(math.radians(30)) * self.grid_spacing
                y_g = self.grid_spacing - c_g

                for x in range(int(2500 // x_g)):
                    self.grid_items.append(self.canvas.create_line(x*x_g, 0, x*x_g, 2000, fill="gray", tags="grid"))
                for y in range(int(2000 // y_g)):
                    self.grid_items.append(self.canvas.create_line(0, y*y_g, 2500, y*y_g, fill="gray", tags="grid"))
            
                
                for y in range(int(2000 // y_g)):
                    for x in range(int(2500 * 2 // x_g)):
                        xx, yy = self.to_hex(x, y, x_g, y_g, c_g)
                        if xx != None and yy != None:
                            self.grid_items.append(self.canvas.create_oval(
                                        xx - 5, yy - 5,
                                        xx + 5, yy + 5,
                                        fill="gray", width=0, tags=f"grid"
                                    ))
                        



    def toggle_grid(self):
        self.show_grid = self.grid_check_var.get()
        self.draw_grid()

    def add_anion_run(self, x, y):
        self.Dope_check_var.set(True)
        self.anions = []
        self.anions.append((x, y, self.stacking_info_entry_var.get()))
        self.st_val_update_screen()
        self.x_e_en.configure(state="normal")
        self.x_e_en.delete(0, "end")
        self.x_e_en.insert(0, f"{x}")
        self.x_e_en.configure(state="disabled")

        self.y_e_en.configure(state="normal")
        self.y_e_en.delete(0, "end")
        self.y_e_en.insert(0, f"{y}")
        self.y_e_en.configure(state="disabled")

        self.z_e_en.configure(state="normal")
        self.z_e_en.delete(0, "end")
        self.z_e_en.insert(0, f"{(int(self.stacking_info_entry_var.get())-1) * float(self.bond_length_entry.get())}")
        self.z_e_en.configure(state="disabled")

    def clear_anion_run(self, x, y):
        self.Dope_check_var.set(False)
        self.anions = []
        self.canvas.delete("anions")
        self.st_val_update_screen()

        self.x_e_en.configure(state="normal")
        self.x_e_en.delete(0, "end")
        self.x_e_en.configure(state="disabled")
        self.y_e_en.configure(state="normal")
        self.y_e_en.delete(0, "end")
        self.y_e_en.configure(state="disabled")
        self.z_e_en.configure(state="normal")
        self.z_e_en.delete(0, "end")
        self.z_e_en.configure(state="disabled")



    def add_atom_run(self, x, y):
        self.atoms[int(self.stacking_info_entry_var.get())-1].append(self.AUID)
        self.atoms_dic[f"{self.AUID}"] = (x, y)
        self.atom_tags.append(f"atom_{self.AUID}")
        self.das[f"{self.AUID}"] = 1
        self.AUID += 1
        self.st_val_update_screen()


    def clear_atom_run(self, x, y):
        for kk in range(len(self.atoms[int(self.stacking_info_entry_var.get())-1]) - 1, -1, -1):
            auid = self.atoms[int(self.stacking_info_entry_var.get())-1][kk]
            atom_x, atom_y = self.atoms_dic[f"{auid}"]
            if (x > atom_x - self.atom_radius and x < atom_x + self.atom_radius) and (y > atom_y - self.atom_radius and y < atom_y + self.atom_radius):
                self.canvas.delete(f"atom_{auid}")
                del self.atoms[int(self.stacking_info_entry_var.get())-1][kk]
                tag_to_remove = f"atom_{auid}"
                if tag_to_remove in self.atom_tags:
                    self.atom_tags.remove(tag_to_remove)
                
                bd_del = [[],[]]

                for k in range(2):
                    for bds1 in self.bonds[k]:
                        if auid in bds1:
                            self.canvas.delete(f"bond_{max(bds1)}_{min(bds1)}")
                            bd_del[k].append(bds1)


                for k in range(2):
                    for bds in bd_del[k]:
                        self.bonds[k].remove(bds)

                

                if f"{auid}" in self.atoms_dic:
                    del self.atoms_dic[f"{auid}"]
                if f"{auid}" in self.das:
                    del self.das[f"{auid}"]
        if self.show_update_ind_btn.cget("text") == "Hide Atom Index":
            self.update_ind_fn()


    def add_bond_run(self, x, y):
        current_layer_index = int(self.stacking_info_entry_var.get()) - 1
        previous_layer_index = current_layer_index - 1
        
        layers_to_check = [self.atoms[current_layer_index]]
        if previous_layer_index >= 0:
            layers_to_check.append(self.atoms[previous_layer_index])

        for layer in layers_to_check:
            for auid in layer:
                atom_x, atom_y = self.atoms_dic[f"{auid}"]
                if abs(x - atom_x) <= self.atom_radius and abs(y - atom_y) <= self.atom_radius:
                    if self.selected_atom is None:
                        self.selected_atom = (atom_x, atom_y)
                        self.canvas.itemconfig(f"atom_{auid}", outline="blue", width=2)
                        self.at_id.append(auid)
                    else:
                        self.at_id.append(auid)
                        bond = tuple(sorted(self.at_id))
                        if self.at_id[0] != self.at_id[1] and bond not in self.bonds[0]:
                            self.bonds[0].append(bond)
                            self.bond_tags.append(f"bond_{bond[0]}_{bond[1]}")
                            self.st_val_update_screen()
                    
                        self.canvas.itemconfig(f"atom_{self.at_id[0]}", outline="black", width=1)
                        self.selected_atom = None
                        self.at_id = []
                    break


    def add_nbbond_run(self, x, y):
        current_layer_index = int(self.stacking_info_entry_var.get()) - 1
        previous_layer_index = current_layer_index - 1
        
        layers_to_check = [self.atoms[current_layer_index]]
        if previous_layer_index >= 0:
            layers_to_check.append(self.atoms[previous_layer_index])

        for layer in layers_to_check:
            for auid in layer:
                atom_x, atom_y = self.atoms_dic[f"{auid}"]
                if abs(x - atom_x) <= self.atom_radius and abs(y - atom_y) <= self.atom_radius:
                    if self.selected_atom is None:
                        self.selected_atom = (atom_x, atom_y)
                        self.canvas.itemconfig(f"atom_{auid}", outline="blue", width=2)
                        self.at_id.append(auid)
                    else:
                        self.at_id.append(auid)
                        bond = tuple(sorted(self.at_id))
                        if self.at_id[0] != self.at_id[1] and bond not in self.bonds[1]:
                            self.bonds[1].append(bond)
                            self.bond_tags.append(f"bond_{bond[0]}_{bond[1]}")
                            self.st_val_update_screen()
                    
                        self.canvas.itemconfig(f"atom_{self.at_id[0]}", outline="black", width=1)
                        self.selected_atom = None
                        self.at_id = []
                    break


    def selected_atm_p(self):
        if self.selected_atom is None:
            pass
        else:
            self.selected_atom = None
            self.canvas.itemconfig(self.at_id[0], outline="black", width=1)
            self.at_id = []

    def remove_bond_run(self, x, y):
        current_layer_index = int(self.stacking_info_entry_var.get()) - 1
        previous_layer_index = current_layer_index - 1
        
        layers_to_check = [self.atoms[current_layer_index]]
        if previous_layer_index >= 0:
            layers_to_check.append(self.atoms[previous_layer_index])

        for layer in layers_to_check:
            for auid in layer:
                atom_x, atom_y = self.atoms_dic[f"{auid}"]
                if abs(x - atom_x) <= self.atom_radius and abs(y - atom_y) <= self.atom_radius:
                    if self.selected_atom is None:
                        self.selected_atom = (atom_x, atom_y)
                        self.canvas.itemconfig(f"atom_{auid}", outline="red", width=2)
                        self.at_id.append(auid)
                    else:
                        self.at_id.append(auid)
                        self.canvas.delete(f"bond_{max(self.at_id)}_{min(self.at_id)}")
                        self.selected_atom = None
                        self.canvas.itemconfig(f"atom_{self.at_id[0]}", outline="black", width=1)
                        if tuple([min(self.at_id), max(self.at_id)]) in self.bonds[0]:
                                self.bonds[0].remove(tuple([min(self.at_id), max(self.at_id)]))
                        elif tuple([min(self.at_id), max(self.at_id)]) in self.bonds[1]:
                            self.bonds[1].remove(tuple([min(self.at_id), max(self.at_id)]))
                        else:
                            print("NA")
                        tag_to_remove = f"bond_{min(self.at_id)}_{max(self.at_id)}"
                        if tag_to_remove in self.bond_tags:
                            self.bond_tags.remove(tag_to_remove)
                        self.at_id = []
                        break


    def donor_run(self, x, y):
        for auid in self.atoms[int(self.stacking_info_entry_var.get())-1]:
            atom_x, atom_y = self.atoms_dic[f"{auid}"]
            if (x > atom_x-self.atom_radius and x < atom_x+self.atom_radius) and (y > atom_y-self.atom_radius and y < atom_y+self.atom_radius):
                self.canvas.itemconfig(f"atom_{auid}", outline="black", fill="#3d3d3d", width=1)
                self.das[f"{auid}"] = 1


    def acceptor_run(self, x, y):
        for auid in self.atoms[int(self.stacking_info_entry_var.get())-1]:
            atom_x, atom_y = self.atoms_dic[f"{auid}"]
            if (x > atom_x-self.atom_radius and x < atom_x+self.atom_radius) and (y > atom_y-self.atom_radius and y < atom_y+self.atom_radius):
                self.canvas.itemconfig(f"atom_{auid}", outline="black", fill="#a38b48", width=1)
                self.das[f"{auid}"] = -1





    def click_on_canvas(self, event):
        self.root.focus()
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.mode == "add_atom":
            if self.show_grid:
                if self.grid_type == "cubic":
                    snapped_x = round(cx / self.grid_spacing) * self.grid_spacing
                    snapped_y = round(cy / self.grid_spacing) * self.grid_spacing
                    self.add_atom_run(snapped_x, snapped_y)
                elif self.grid_type == "hexagon":
                    c_g = math.sin(math.radians(30)) * self.grid_spacing / 2
                    x_g = math.cos(math.radians(30)) * self.grid_spacing
                    y_g = self.grid_spacing - c_g

                    snapped_x = round(cx / x_g)
                    snapped_y = round(cy / y_g)
                    xx, yy = self.to_hex(snapped_x, snapped_y, x_g, y_g, c_g)
                    if xx != None and yy != None:
                        self.add_atom_run(xx, yy)

            else:
                snapped_x = cx
                snapped_y = cy
                self.add_atom_run(snapped_x, snapped_y)
            
        elif self.mode == "clear_atom":
            snapped_x = cx
            snapped_y = cy
            self.clear_atom_run(snapped_x, snapped_y)
        
        elif self.mode == "add_anion":
            if self.show_grid:
                if self.grid_type == "cubic":
                    snapped_x = round(cx / self.grid_spacing) * self.grid_spacing
                    snapped_y = round(cy / self.grid_spacing) * self.grid_spacing
                    self.add_anion_run(snapped_x, snapped_y)
                elif self.grid_type == "hexagon":
                    c_g = math.sin(math.radians(30)) * self.grid_spacing / 2
                    x_g = math.cos(math.radians(30)) * self.grid_spacing
                    y_g = self.grid_spacing - c_g

                    snapped_x = round(cx / x_g)
                    snapped_y = round(cy / y_g)
                    xx, yy = self.to_hex(snapped_x, snapped_y, x_g, y_g, c_g)
                    if xx != None and yy != None:
                        self.add_anion_run(xx, yy)

            else:
                snapped_x = cx
                snapped_y = cy
                self.add_anion_run(snapped_x, snapped_y)

        elif self.mode == "clear_anion":
            snapped_x = cx
            snapped_y = cy
            self.clear_anion_run(snapped_x, snapped_y)
        

        elif self.mode == "add_bond":
            snapped_x = cx
            snapped_y = cy
            self.add_bond_run(snapped_x, snapped_y)
        elif self.mode == "add_nbbond":
            snapped_x = cx
            snapped_y = cy
            self.add_nbbond_run(snapped_x, snapped_y)
        elif self.mode == "remove_bond":
            snapped_x = cx
            snapped_y = cy
            self.remove_bond_run(snapped_x, snapped_y)
        elif self.mode == "donor":
            snapped_x = cx
            snapped_y = cy
            self.donor_run(snapped_x, snapped_y)
        elif self.mode == "acceptor":
            snapped_x = cx
            snapped_y = cy
            self.acceptor_run(snapped_x, snapped_y)


    def da_check_toggle(self):
        pass

    def Dope_check_toggle(self):
        pass

            
    def dis_check_toggle(self):
        if self.dis_check_var.get():
            self.num_config_entry.configure(state="normal")
            self.dis_sig_entry.configure(state="normal")
            self.num_core_entry.configure(state="normal")

        else:
            self.num_config_entry.delete(0, "end")
            self.dis_sig_entry.delete(0, "end")

            self.num_config_entry.configure(state="disabled")
            self.dis_sig_entry.configure(state="disabled")

            self.num_core_entry.delete(0, "end")
            self.num_core_entry.configure(state="disabled")

    def update_ind_fn(self):
        for i in self.s_ind_list:
            self.canvas.delete(i)
        self.a_val_index_list = []
        count = 0

        for a in range(len(self.atoms)):
            a_val = self.atoms[a]
            sub_list = []
            for b in range(len(a_val)):
                count += 1
                atom_x, atom_y = self.atoms_dic[f"{a_val[b]}"]
                sub_list.append((atom_x, atom_y, count))    

            self.a_val_index_list.append(sub_list)

        for dr_x, dr_y, ind in self.a_val_index_list[int(self.stacking_info_entry_var.get())-1]:
            self.canvas.create_text(dr_x, dr_y, text=str(ind), font=("Arial", 15), fill="white", tags=f"ind_{ind}")
            self.s_ind_list.append(f"ind_{ind}")
        if self.stacking_info_entry_var.get() != "1":
            for dr_x, dr_y, ind in self.a_val_index_list[int(self.stacking_info_entry_var.get())-2]:
                self.canvas.create_text(dr_x, dr_y, text=str(ind), font=("Arial", 15), fill="white", tags=f"ind_{ind}")
                self.s_ind_list.append(f"ind_{ind}")


    def show_update_ind_fn(self):
        if self.show_update_ind_btn.cget("text") == "Show Site Index":
            self.show_update_ind_btn.configure(text="Hide Site Index")
            self.update_ind_fn()
            
        
        else:
            self.show_update_ind_btn.configure(text="Show Site Index")
            
            for i in self.s_ind_list:
                self.canvas.delete(i)


    def st_val_update_screen(self):

        current_stacking_val = int(self.stacking_info_entry_var.get())
        this_layer_atoms = self.atoms[current_stacking_val - 1]

        self.canvas.delete("all")
        self.draw_grid()

        if current_stacking_val == 1:
            for bb in range(2):
                if bb == 0:
                    bcol = "black"
                else:
                    bcol = "#bd7fc9"
                for bond in self.bonds[bb]:
                    if (bond[0] in this_layer_atoms) and (bond[1] in this_layer_atoms):
                        self.canvas.create_line(
                                self.atoms_dic[f"{bond[0]}"][0], self.atoms_dic[f"{bond[0]}"][1],
                                self.atoms_dic[f"{bond[1]}"][0], self.atoms_dic[f"{bond[1]}"][1],
                                fill=bcol, width=5, tags=f"bond_{max(bond)}_{min(bond)}"
                            )

                            
            for auid in this_layer_atoms:
                atom_x, atom_y = self.atoms_dic[f"{auid}"]
                if self.das[f"{auid}"] == 1:
                    col = "#3d3d3d"
                else:
                    col = "#a38b48"
                self.canvas.create_oval(
                        atom_x - self.atom_radius, atom_y - self.atom_radius,
                        atom_x + self.atom_radius, atom_y + self.atom_radius,
                        fill=col, outline="black", width=1, tags=f"atom_{auid}"
                    )
            if self.show_update_ind_btn.cget("text") == "Hide Atom Index":
                self.update_ind_fn()

            
            
            
                        
        else:
            last_layer_atoms = self.atoms[current_stacking_val - 2]
            for bb in range(2):
                if bb == 0:
                    bcol = "black"
                else:
                    bcol = "#bd7fc9"
                for bond in self.bonds[bb]:
                    if (bond[0] in this_layer_atoms) and (bond[1] in this_layer_atoms):
                        self.canvas.create_line(
                                self.atoms_dic[f"{bond[0]}"][0], self.atoms_dic[f"{bond[0]}"][1],
                                self.atoms_dic[f"{bond[1]}"][0], self.atoms_dic[f"{bond[1]}"][1],
                                fill=bcol, width=5, tags=f"bond_{max(bond)}_{min(bond)}"
                            )
                    if (bond[0] in last_layer_atoms) and (bond[1] in last_layer_atoms):
                        self.canvas.create_line(
                                self.atoms_dic[f"{bond[0]}"][0], self.atoms_dic[f"{bond[0]}"][1],
                                self.atoms_dic[f"{bond[1]}"][0], self.atoms_dic[f"{bond[1]}"][1],
                                fill=bcol, width=5, tags=f"bond_{max(bond)}_{min(bond)}"
                            )
                        
            for bb in range(2):
                if bb == 0:
                    bcol = "black"
                else:
                    bcol = "#bd7fc9"
                for bond in self.bonds[bb]:
                    if ((bond[0] in this_layer_atoms) and (bond[1] in last_layer_atoms)) or ((bond[1] in this_layer_atoms) and (bond[0] in last_layer_atoms)):
                        self.canvas.create_line(
                                self.atoms_dic[f"{bond[0]}"][0], self.atoms_dic[f"{bond[0]}"][1],
                                self.atoms_dic[f"{bond[1]}"][0], self.atoms_dic[f"{bond[1]}"][1],
                                fill=bcol, width=5, tags=f"bond_{max(bond)}_{min(bond)}"
                            )

            for auid in last_layer_atoms:
                atom_x, atom_y = self.atoms_dic[f"{auid}"]
                if self.das[f"{auid}"] == 1:
                    col = "#757474"
                else:
                    col = "#6b634b"
                self.canvas.create_oval(
                        atom_x - self.atom_radius, atom_y - self.atom_radius,
                        atom_x + self.atom_radius, atom_y + self.atom_radius,
                        fill=col, outline="black", width=1, tags=f"atom_{auid}"
                    )
            for auid in this_layer_atoms:
                atom_x, atom_y = self.atoms_dic[f"{auid}"]
                if self.das[f"{auid}"] == 1:
                    col = "#3d3d3d"
                else:
                    col = "#a38b48"
                self.canvas.create_oval(
                        atom_x - self.atom_radius, atom_y - self.atom_radius,
                        atom_x + self.atom_radius, atom_y + self.atom_radius,
                        fill=col, outline="black", width=1, tags=f"atom_{auid}"
                    )
                

            if self.show_update_ind_btn.cget("text") == "Hide Atom Index":   
                self.update_ind_fn()

        for iarr in self.anions:
            if iarr[2] == str(current_stacking_val):
                self.canvas.create_oval(
                    iarr[0] - self.atom_radius, iarr[1] - self.atom_radius,
                    iarr[0] + self.atom_radius, iarr[1] + self.atom_radius,
                    fill="red", outline="black", width=1, tags=f"anions"
                )

            
                        
                
    
    def stacking_up_fn(self):
        st_val = int(self.stacking_info_entry_var.get())
        if self.stacking_info_entry_var.get() != self.stacking_list[-1]:
            self.stacking_info_entry_var.set(self.stacking_list[st_val])
            self.show_update_ind_btn.configure(text="Show Atom Index")
            self.st_val_update_screen()



    

    def stacking_down_fn(self):
        st_val = int(self.stacking_info_entry_var.get())
        if self.stacking_info_entry_var.get() != "1":
            self.stacking_info_entry_var.set(self.stacking_list[st_val-2])
            self.show_update_ind_btn.configure(text="Show Atom Index")
            self.st_val_update_screen()




    def stacking_add_fn(self):
        st_val = int(self.stacking_info_entry_var.get())
        st_lis_len = len(self.stacking_list)
        self.stacking_list.insert(st_val, str(st_val+1))
        for im in range(st_lis_len-st_val):
            self.stacking_list[st_val + 1 + im] = str(st_val + 2 + im)
        self.stacking_info_entry_var.set(str(st_val + 1))
        self.atoms.insert(st_val, [])
        self.show_update_ind_btn.configure(text="Show Atom Index")
        self.st_val_update_screen()

    def stacking_remove_fn(self):
        st_val = int(self.stacking_info_entry_var.get())
        st_lis_len = len(self.stacking_list)
        if st_lis_len != 1:
            self.stacking_list.remove(str(st_lis_len))
            self.stacking_down_fn()
            del self.atoms[st_val-1]























if __name__ == "__main__":

    QG = Quasi_GUI()












