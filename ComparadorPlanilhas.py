import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import re

def select_files():
    root = tk.Tk()
    root.withdraw()

    file_path1 = filedialog.askopenfilename()
    file_path2 = filedialog.askopenfilename()

    return file_path1, file_path2

def select_columns(df):
    root = tk.Tk()
    root.title("Select Column")

    column = tk.StringVar(root)
    column.set(df.columns[0])  # default value

    opt = ttk.OptionMenu(root, column, *df.columns)
    opt.pack()

    def ok():
        root.quit()

    btn = ttk.Button(root, text="OK", command=ok)
    btn.pack()

    root.mainloop()
    root.destroy()

    return column.get()

def formatar_numero(numero):
    # Remover espaços em branco e adicionar o código de país e área
    numero_formatado = re.sub(r'\s', '', numero)
    if len(numero_formatado) == 11:  # Se o número já incluir o código de área
        return '55' + numero_formatado
    else:
        return '55' + '11' + numero_formatado[2:]

def compare_files(file1, file2):
    try:
        df1 = pd.read_csv(file1, delimiter='\t', encoding='utf-16')
        df2 = pd.read_csv(file2, delimiter='\t', encoding='utf-16')
    except UnicodeDecodeError:
        df1 = pd.read_csv(file1, delimiter='\t', encoding='latin1')
        df2 = pd.read_csv(file2, delimiter='\t', encoding='latin1')

    column_to_compare = select_columns(df1)

    df = pd.concat([df1, df2])
    df_final = df.drop_duplicates(subset=[column_to_compare], keep=False)

    # Aplicar a formatação de número à coluna "FONE"
    if 'FONE' in df_final.columns:
        df_final.loc[:, 'FONE'] = df_final['FONE'].apply(formatar_numero)

    df_final.to_excel("output.xlsx", index=False)

def main():
    file1, file2 = select_files()
    compare_files(file1, file2)

if __name__ == "__main__":
    main()
