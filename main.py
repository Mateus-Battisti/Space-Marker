import tkinter as tk
from tkinter import simpledialog, messagebox

# Dicionário para armazenar as marcações
marks = {}

# Função para salvar as marcações em um arquivo
def save_marks():
    try:
        with open('marks.txt', 'w') as file:
            for mark_id, data in marks.items():
                file.write(f"{mark_id}:{data['name']}:{data['position'][0]},{data['position'][1]}\n")
        messagebox.showinfo('Salvar', 'Marcações salvas com sucesso!')
    except Exception as e:
        messagebox.showerror('Erro ao salvar', f'Ocorreu um erro ao salvar as marcações: {str(e)}')

# Função para carregar as marcações de um arquivo
def load_marks():
    global marks
    marks.clear()  # Limpa as marcações atuais
    try:
        with open('marks.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                mark_id = int(parts[0])
                name = parts[1]
                position = tuple(map(int, parts[2].split(',')))
                marks[mark_id] = {'name': name, 'position': position}
        redraw_marks()
        messagebox.showinfo('Carregar', 'Marcações carregadas com sucesso!')
    except FileNotFoundError:
        messagebox.showwarning('Carregar', 'Nenhum arquivo de marcações encontrado.')
    except Exception as e:
        messagebox.showerror('Erro ao carregar', f'Ocorreu um erro ao carregar as marcações: {str(e)}')

# Função para limpar todas as marcações
def clear_marks():
    global marks
    marks.clear()
    redraw_marks()
    messagebox.showinfo('Limpar', 'Marcações removidas.')

# Função para desenhar as marcações na tela
def redraw_marks():
    canvas.delete('all')  # Limpa o canvas
    for mark_id, data in marks.items():
        x, y = data['position']
        canvas.create_oval(x-5, y-5, x+5, y+5, outline='red', width=2)
        canvas.create_text(x, y-10, text=data['name'])

# Função para lidar com o clique do mouse na imagem
def on_click(event):
    x, y = event.x, event.y
    name = simpledialog.askstring('Nome da Estrela', 'Digite o nome da estrela:')
    if name is None or name.strip() == '':
        name = 'desconhecido'
    marks[len(marks)+1] = {'name': name, 'position': (x, y)}
    redraw_marks()

# Configurando a janela principal
root = tk.Tk()
root.title('Marcação de Estrelas')

# Criando o canvas para exibir a imagem
canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.pack()

# Carregando marcações previamente salvas, se existirem
load_marks()

# Associando evento de clique do mouse à função on_click
canvas.bind('<Button-1>', on_click)

# Criando menu de opções
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Opções', menu=file_menu)
file_menu.add_command(label='Salvar marcações', command=save_marks)
file_menu.add_command(label='Carregar marcações', command=load_marks)
file_menu.add_command(label='Excluir todas as marcações', command=clear_marks)

# Função para salvar as marcações antes de fechar a janela
def on_closing():
    save_marks()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciando o loop principal da aplicação
root.mainloop()
