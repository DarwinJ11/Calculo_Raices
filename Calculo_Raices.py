import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import sympify, symbols, diff, N
from PIL import Image, ImageTk

class RootFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos para Raíces")
        
        try:
            self.logo_img = Image.open("logo.png")
            self.logo_img = self.logo_img.resize((80, 80), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(self.logo_img)
            
            logo_frame = tk.Frame(self.root)
            logo_frame.pack(pady=5)
            
            tk.Label(logo_frame, image=self.logo).pack(side=tk.LEFT, padx=10)
            tk.Label(logo_frame, 
                    text="Instituto Tecnológico de Tuxtla Gutierrez\nMÉTODOS NUMÉRICOS PARA RAÍCES",
                    font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        except:

            tk.Label(self.root, 
                    text="Instituto Tecnológico de Tuxtla Gutierrez\nMÉTODOS NUMÉRICOS PARA RAÍCES",
                    font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        control_frame = tk.Frame(main_frame)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        tk.Label(control_frame, text="Método:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.method_var = tk.StringVar(value="Bisección")
        self.method_menu = ttk.Combobox(control_frame, textvariable=self.method_var, 
                                      values=["Bisección", "Falsa Posición", "Newton-Raphson"])
        self.method_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.method_var.trace("w", self.toggle_entries)

        tk.Label(control_frame, text="Función f(x):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_func = tk.Entry(control_frame, width=25)
        self.entry_func.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_func.insert(0, "x**3 - 2*x - 5") 

        self.label_a = tk.Label(control_frame, text="Extremo izquierdo (a):")
        self.label_a.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_a = tk.Entry(control_frame, width=15)
        self.entry_a.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.entry_a.insert(0, "2.0")

        self.label_b = tk.Label(control_frame, text="Extremo derecho (b):")
        self.label_b.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_b = tk.Entry(control_frame, width=15)
        self.entry_b.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.entry_b.insert(0, "3.0")


        self.label_x0 = tk.Label(control_frame, text="Valor inicial (x0):")
        self.entry_x0 = tk.Entry(control_frame, width=15)
        self.entry_x0.insert(0, "2.5")

        tk.Label(control_frame, text="Tolerancia:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_tol = tk.Entry(control_frame, width=15)
        self.entry_tol.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.entry_tol.insert(0, "1e-6")

        tk.Label(control_frame, text="Máx iteraciones:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.entry_max_iter = tk.Entry(control_frame, width=15)
        self.entry_max_iter.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.entry_max_iter.insert(0, "100")

        tk.Label(control_frame, text="Decimales a mostrar:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.entry_decimals = tk.Entry(control_frame, width=15)
        self.entry_decimals.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.entry_decimals.insert(0, "6")

        tk.Button(control_frame, text="Calcular", command=self.compute, 
                 bg="#4CAF50", fg="white").grid(row=7, column=0, columnspan=2, pady=10)

        results_frame = tk.Frame(main_frame)
        results_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.columns = ("Iteración", "x", "f(x)")
        self.table = ttk.Treeview(results_frame, columns=self.columns, show="headings", height=10)
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        self.toggle_entries()

    def toggle_entries(self, *args):
        method = self.method_var.get()
        if method == "Newton-Raphson":
            self.label_a.grid_remove()
            self.entry_a.grid_remove()
            self.label_b.grid_remove()
            self.entry_b.grid_remove()
            self.label_x0.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.entry_x0.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        else:
            self.label_a.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.entry_a.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.label_b.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.entry_b.grid(row=3, column=1, padx=5, pady=5, sticky="w")
            self.label_x0.grid_remove()
            self.entry_x0.grid_remove()

    def bisection_method(self, f, a, b, tol, max_iter):
        x = symbols('x')
        f_expr = sympify(f)
        f_lambda = lambda val: N(f_expr.subs(x, val))
        
        iterations = []
        if f_lambda(a) * f_lambda(b) >= 0:
            messagebox.showerror("Error", "El intervalo [a, b] no cumple con f(a)*f(b) < 0.")
            return [], None
        
        for i in range(max_iter):
            c = (a + b) / 2
            f_c = f_lambda(c)
            iterations.append((i, c, f_c))
            
            if abs(f_c) < tol:
                break
            
            if f_lambda(a) * f_c < 0:
                b = c
            else:
                a = c
        
        return iterations, c

    def false_position_method(self, f, a, b, tol, max_iter):
        x = symbols('x')
        f_expr = sympify(f)
        f_lambda = lambda val: N(f_expr.subs(x, val))
        
        iterations = []
        if f_lambda(a) * f_lambda(b) >= 0:
            messagebox.showerror("Error", "El intervalo [a, b] no cumple con f(a)*f(b) < 0.")
            return [], None
        
        for i in range(max_iter):
            c = (a * f_lambda(b) - b * f_lambda(a)) / (f_lambda(b) - f_lambda(a))
            f_c = f_lambda(c)
            iterations.append((i, c, f_c))
            
            if abs(f_c) < tol:
                break
            
            if f_lambda(a) * f_c < 0:
                b = c
            else:
                a = c
        
        return iterations, c

    def newton_raphson_method(self, f, x0, tol, max_iter):
        x = symbols('x')
        f_expr = sympify(f)
        f_lambda = lambda val: N(f_expr.subs(x, val))
        df_expr = diff(f_expr, x)
        df_lambda = lambda val: N(df_expr.subs(x, val))
        
        iterations = []
        xn = x0
        
        for i in range(max_iter):
            fxn = f_lambda(xn)
            dfxn = df_lambda(xn)
            
            if dfxn == 0:
                messagebox.showerror("Error", "Derivada cero. No se puede continuar.")
                return [], None
                
            xn1 = xn - fxn / dfxn
            fxn1 = f_lambda(xn1)
            iterations.append((i, xn1, fxn1))
            
            if abs(fxn1) < tol:
                break
                
            xn = xn1
        
        return iterations, xn1

    def compute(self):
        try:
            method = self.method_var.get()
            f = self.entry_func.get()
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_max_iter.get())
            decimals = int(self.entry_decimals.get())
            
            if method in ["Bisección", "Falsa Posición"]:
                a = float(self.entry_a.get())
                b = float(self.entry_b.get())
                
                if method == "Bisección":
                    results, root = self.bisection_method(f, a, b, tol, max_iter)
                else:
                    results, root = self.false_position_method(f, a, b, tol, max_iter)
                    
            elif method == "Newton-Raphson":
                x0 = float(self.entry_x0.get())
                results, root = self.newton_raphson_method(f, x0, tol, max_iter)
            
            # Limpiar tabla
            for row in self.table.get_children():
                self.table.delete(row)
            
            if results:
                x_vals, y_vals = [], []
                for i, c, fc in results:

                    formatted_c = f"{float(c):.{decimals}f}"
                    formatted_fc = f"{float(fc):.{decimals}e}"  
                    self.table.insert("", "end", values=(i, formatted_c, formatted_fc))
                    x_vals.append(i)
                    y_vals.append(abs(fc))
                
                # Configurar gráfico
                self.ax.clear()
                self.ax.plot(x_vals, y_vals, marker='o', linestyle='-', color='royalblue')
                self.ax.set_xlabel("Iteración", fontsize=10)
                self.ax.set_ylabel("|f(x)|", fontsize=10)
                self.ax.set_title(f"Convergencia del Método de {method}", fontsize=12)
                self.ax.grid(True, linestyle='--', alpha=0.7)
                self.canvas.draw()
                
                if root is not None:
                    messagebox.showinfo("Resultado", 
                                     f"Raíz aproximada: {float(root):.{decimals}f}\n"
                                     f"Iteraciones: {len(results)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en los datos de entrada:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RootFinderApp(root)
    root.mainloop()