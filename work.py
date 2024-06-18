import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox

pygame.init()
fundo = pygame.image.load("assets/bg.jpg")

RED = (255, 0, 0)

WINDOW_SIZE = (800, 600)



screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Space marker')


marks = {}


def save_marks():
    try:
        with open('marks.txt', 'w') as file:
            for mark_id, data in marks.items():
                file.write(f"{mark_id}:{data['name']}:{data['position'][0]},{data['position'][1]}\n")
        messagebox.showinfo('Salvar', 'Marcações salvas com sucesso!')
    except Exception as e:
        messagebox.showerror('Erro ao salvar', f'Ocorreu um erro ao salvar as marcações: {str(e)}')


def load_marks():
    global marks
    marks.clear()  
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


def clear_marks():
    global marks
    marks.clear()
    redraw_marks()
    messagebox.showinfo('Limpar', 'Marcações removidas.')


def redraw_marks():
     
    for mark_id, data in marks.items():
        x, y = data['position']
        pygame.draw.circle(screen, RED, (x, y), 5)  
        font = pygame.font.Font(None, 20)
        text = font.render(data['name'], True, RED)
        screen.blit(text, (x - 10, y - 20))


def handle_click(pos):
    name = simpledialog.askstring('Nome da Estrela', 'Digite o nome da estrela:')
    if name is None or name.strip() == '':
        name = 'desconhecido'
    marks[len(marks)+1] = {'name': name, 'position': pos}
    redraw_marks()


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_marks()  
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                pos = pygame.mouse.get_pos()
                handle_click(pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_marks()  
                running = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
