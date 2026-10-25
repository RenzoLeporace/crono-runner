"""Game credits and original-project copyright notice."""
from .art import text,tracked,line,PAPER,CYAN,GOLD,MUTED
from .learning_ui import wrapped

def draw(game):
    s=game.canvas;s.fill((13,27,37))
    tracked(s,'CRONO · ECOS DEL TIEMPO',(65,35),14,CYAN,3)
    text(s,'Créditos',(62,86),49,PAPER,True,serif=True)
    text(s,'Renzo Leporace',(65,190),42,GOLD,True)
    text(s,'Creador del proyecto · concepto y dirección',(65,248),23,PAPER)
    text(s,'© 2026 Renzo Leporace. Todos los derechos reservados.',(65,320),23,CYAN,True)
    wrapped(s,'Desarrollo, ilustraciones originales mediante código y asistencia de revisión: herramientas de inteligencia artificial de OpenAI. Las pruebas automáticas y auditorías complementan la revisión de personas y docentes.',(65,383),1110,20,MUTED,leading=30)
    wrapped(s,'Tecnología: Python, pygame-ce / SDL y herramientas de distribución. Las licencias y atribuciones de terceros se conservan en LICENCIAS.txt. Las fuentes históricas y educativas se detallan en FUENTES.md y en las fichas del juego.',(65,491),1110,19,MUTED,leading=29)
    game.button('Volver',(65,632,270,55),lambda:game.set_state('menu'),True)
