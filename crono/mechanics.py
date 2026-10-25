"""Optional historical fieldwork, traversal tools and contextual encounters.

Every route introduces its device on safe ground, repeats it with a physical
application, then offers a mastery station. Main route geometry stays stable.
"""
import math
import pygame as pg
from .art import rect,line,circle,diamond,text,PAPER,CYAN,GOLD,MUTED,polygon

# title, physical system, objective, ordered field operations, contextual note
ROWS=(
('La marea primigenia','tide','Regula tres compuertas y usa las corrientes.',('Abrir canal de entrada','Esperar la pleamar','Cerrar el canal lateral'),'Las mareas actuales ayudan a interpretar antiguas costas; esta instalación es una herramienta ficticia de Crono.'),
('Un fósil en su contexto','excavate','Excava, compara estratos y conserva el hallazgo.',('Retirar sedimento superficial','Registrar el estrato','Extraer con soporte'),'La posición del fósil aporta información; extraerlo sin registro destruye parte de esa evidencia.'),
('Bajo la lluvia de impactos','shelter','Activa refugios y cruza cuando se apaguen las señales.',('Asegurar el primer refugio','Reforzar el techo','Activar aviso de evacuación'),'Los refugios son ficción del viaje. La extinción del final del Cretácico no fue una batalla de personas.'),
('Huellas sobre el glaciar','wind','Orienta balizas y aprovecha ráfagas entre salientes.',('Leer la dirección del viento','Orientar la primera baliza','Asegurar el paso elevado'),'El clima condicionaba la movilidad. No todas las poblaciones del Paleolítico vivían junto a glaciares.'),
('Un hogar compartido','warmth','Recupera combustible y mantén encendidos los hogares.',('Reunir madera seca','Proteger las brasas','Compartir el calor'),'El control del fuego facilitó cocinar, iluminarse y reunirse; su dominio fue un proceso prolongado.'),
('La pared que recuerda','reveal','Ilumina señales para descubrir una galería de pigmentos.',('Preparar una lámpara','Comparar las huellas','Iluminar el panel completo'),'Las pinturas rupestres son fuentes que requieren interpretación; no conocemos el significado de todas.'),
('Voces en la asamblea','assembly','Recoge propuestas y distingue a quiénes excluía la ciudadanía.',('Escuchar a los ciudadanos','Reconocer las exclusiones','Registrar la decisión colectiva'),'La democracia ateniense excluía a mujeres, esclavos y extranjeros residentes. No equivale al sufragio universal.'),
('El puerto y sus poleas','crane','Acciona una grúa para mover cargas y abrir un atajo.',('Sujetar la carga','Elevar con la polea','Girar hacia el muelle'),'Los puertos conectaban personas, productos e ideas; el intercambio también tenía conflictos y desigualdades.'),
('Una vuelta al estadio','race','Activa los hitos de una carrera sin perder las señales de salida.',('Esperar la señal de salida','Cruzar el primer hito','Registrar la llegada'),'Los antiguos juegos tenían reglas y participantes muy diferentes a los Juegos Olímpicos actuales.'),
('El agua mueve el molino','wheel','Dirige el caudal hacia una rueda y usa su elevador.',('Abrir el canal de toma','Regular el caudal','Conectar la rueda'),'Los molinos aprovecharon agua y viento para transformar trabajo, con técnicas diversas según la región.'),
('Una cuenta del mercado','trade','Compara cantidades y realiza un intercambio razonado.',('Identificar la mercancía','Comparar pesos y medidas','Acordar el intercambio'),'Las monedas, las medidas y los mercados cambiaban entre ciudades; no existía un mercado medieval uniforme.'),
('Luz en la vidriera','beam','Orienta haces para revelar una pasarela de la catedral.',('Abrir la contraventana','Orientar el espejo azul','Alinear el panel central'),'Las vidrieras transmitían relatos y organizaban la luz. El espejo temporal del juego es ficticio.'),
('La presión de la caldera','steam','Abre válvulas para levantar una plataforma sin sobrepresión.',('Abrir la válvula de seguridad','Alimentar la caldera','Conectar el pistón'),'La máquina de vapor transformó energía térmica en movimiento y modificó el trabajo y el ambiente.'),
('Señales del ferrocarril','rail','Prepara cambios de vía y conduce un carro auxiliar.',('Cerrar el paso de peatones','Alinear el cambio de vía','Dar señal de salida'),'Las señales y los horarios coordinaban recorridos compartidos y reducían colisiones.'),
('Una ciudad encendida','circuit','Cierra circuitos en paralelo para encender barrios.',('Aislar la línea dañada','Cerrar el circuito protegido','Conectar el alumbrado'),'La electrificación fue gradual y desigual; no llegó a todos los hogares al mismo tiempo.'),
('Cartas entre líneas','courier','Lleva correspondencia entre refugios y comprueba su origen.',('Recoger la carta fechada','Verificar remitente y destino','Entregar en el refugio'),'Las cartas permiten conocer experiencias personales, pero una sola carta no representa a todas las personas.'),
('Una alarma para proteger','siren','Reconoce avisos, activa refugios y acompaña a civiles.',('Probar la sirena','Abrir el refugio','Guiar a la población'),'La población civil sufrió bombardeos, desplazamientos y persecuciones. La misión prioriza el cuidado.'),
('Reconstruir un puente','bridge','Distribuye materiales y recompón una ruta interrumpida.',('Inspeccionar los apoyos','Colocar las vigas','Asegurar el paso civil'),'La posguerra incluyó reconstrucción y cooperación, además de nuevos conflictos y desigualdades.'),
('Paquetes en la red','packet','Reconecta nodos y encuentra una ruta alternativa.',('Asignar un destino','Elegir un nodo disponible','Confirmar la recepción'),'Internet distribuye datos por redes. Un paquete puede recorrer una ruta distinta de otro.'),
('Energía para la ciudad','energy','Equilibra generación y consumo sin agotar la reserva.',('Reducir consumos evitables','Conectar generación renovable','Guardar energía de respaldo'),'Una transición energética requiere generación, redes, almacenamiento y decisiones sobre el consumo.'),
('El cielo como evidencia','telescope','Alinea instrumentos y contrasta observaciones.',('Calibrar el telescopio','Registrar la observación','Comparar con otro registro'),'La ciencia contrasta datos y revisa explicaciones. Una observación aislada no basta para cualquier afirmación.'),
('Noticias bajo la lluvia','plaza','Protege documentos y abre el paso por una plaza lluviosa.',('Buscar resguardo para el papel','Comprobar la fecha de la noticia','Compartir la información'),'Mayo de 1810 inició un proceso político; la independencia formal se declaró en 1816.'),
('La ruta hacia Cuyo','documents','Ordena comunicaciones y explora el desvío de San Martín.',('Leer el lugar de procedencia','Ordenar las comunicaciones','Preparar la posta hacia Cuyo'),'San Martín organizó el Ejército de los Andes desde Cuyo. El rescate del juego es una misión ficticia.'),
('Volver a decidir','ballot','Abre el circuito electoral y acompaña una urna simbólica.',('Verificar el padrón','Garantizar el voto secreto','Contar los votos con control'),'Las elecciones de 1983 permitieron recuperar el gobierno constitucional tras la última dictadura.'),
('El ritmo del Nilo','canal','Regula canales y navega una barca entre orillas.',('Observar el nivel del agua','Abrir el canal de riego','Distribuir el caudal'),'Las crecidas del Nilo condicionaban la agricultura. El control del agua implicaba trabajo y organización.'),
('Piedras y contrapesos','counterweight','Equilibra cargas para elevar un bloque y llegar al taller.',('Preparar la rampa','Equilibrar el contrapeso','Asegurar el bloque'),'Las pirámides fueron obras de trabajadores organizados; los métodos exactos siguen siendo objeto de estudio.'),
('Signos junto al templo','glyph','Compara signos y utiliza un espejo para revelar un pasaje.',('Identificar el soporte escrito','Comparar dos signos','Registrar su posición'),'Los jeroglíficos son escritura. La referencia a Moisés del mapa pertenece a la tradición bíblica.'),
('El paso de Obligado','chain','Tensa cadenas de defensa y orienta baterías de la costa.',('Anclar la cadena en la orilla','Coordinar las baterías','Proteger la comunicación ribereña'),'En 1845 se intentó impedir el paso de una escuadra anglofrancesa por el Paraná. La escuadra finalmente atravesó la defensa.'),
('Una cordillera por cruzar','provisions','Prepara postas, víveres y pasos abrigados para el cruce.',('Repartir los víveres','Asegurar las cargas de las mulas','Elegir el paso reconocido'),'El cruce de los Andes exigió preparación logística y distintas columnas, no un único camino.'),
('Brown al timón','naval','Conduce un barco: izquierda/derecha, subir/bajar y F para el cañón.',('Comprobar el rumbo','Ajustar las velas','Coordinar la batería naval'),'La guerra con el Imperio del Brasil ocurrió entre 1825 y 1828. Las maniobras del juego son una recreación ficticia.'),
('Un faro para orientarse','beacon','Enciende señales costeras y orienta el haz del Faro.',('Reunir combustible','Encender la señal elevada','Orientar hacia el puerto'),'El Faro de Alejandría pertenece a la época helenística, posterior a la Grecia clásica de la ruta de rescate.'),
('El expreso nocturno','train','Conduce un carro: acelera con derecha, frena con izquierda.',('Comprobar los frenos','Alinear la vía del refugio','Dar salida al convoy'),'Los trabajadores ferroviarios coordinaban vehículos, vías y señales. El convoy es una misión ficticia.'),
('Una camilla al refugio','escort','Acompaña una camilla, despeja el camino y habilita asistencia.',('Reunir material limpio','Preparar el puesto de asistencia','Acompañar a la persona herida'),'La asistencia humanitaria prioriza a las personas heridas y civiles. Esta misión no concede puntos por dañarlas.'),
('Voces desde Malvinas','radio','Repara comunicaciones y lleva suministros entre refugios.',('Proteger el equipo del viento','Conectar la antena','Confirmar recepción del mensaje'),'La guerra de 1982 dejó muertes y secuelas. Esta grieta aborda experiencias y memoria, sin alterar su desenlace.'),
('Pompeya bajo las cenizas','ash','Activa avisos y refugios para una evacuación ficticia.',('Reconocer la caída de ceniza','Avisar a las personas cercanas','Buscar una ruta protegida'),'El Vesubio destruyó Pompeya en el año 79. La misión es ficción y no representa una evacuación histórica documentada.'),
('Un salto pequeño en la Luna','lunar','Aprovecha menor gravedad y registra muestras de superficie.',('Registrar el lugar de la muestra','Sellar el recipiente','Transmitir la identificación'),'Apolo 11 alunizó el 20 de julio de 1969. Collins permaneció en órbita mientras Armstrong y Aldrin descendían.'),
)

class Mechanic:
    def __init__(self,world):
        self.world=world;self.title,self.kind,self.objective,self.operations,self.note=ROWS[world.level_id]
        self.state=dict(step=0,activated=[],escort_x=0.,vehicle=False,vehicle_x=0.,vehicle_y=500.)
        self.devices=[]
        floors=[p for p in world.platforms if not p.moving and p.rect.w>=220]
        used=set()
        blocked=[(x,y) for x,y,*_ in world.data['stations']+world.data.get('cultural_sites',[])]
        if world.rescue_site:blocked.append(world.rescue_site[:2])
        if world.rift_site:blocked.append(world.rift_site[:2])
        candidates=[p for p in floors if all(abs(p.rect.centerx-x)>230 or abs(p.rect.top-y)>150 for x,y in blocked)]
        if len(candidates)>=3:floors=candidates
        for fraction in (.12,.46,.78):
            platform=min((p for p in floors if id(p) not in used),key=lambda p:abs(p.rect.centerx-world.width*fraction))
            used.add(id(platform))
            self.devices.append((platform.rect.centerx,platform.rect.top))
        self.vehicle_kind=False
        self.state['vehicle_x']=self.devices[1][0];self.state['vehicle_y']=self.devices[1][1]-32
        self.wind=0.;self.gravity=1.;self.speed=1.;self.sheltered=False
        from .field_systems import FieldSystem
        self.field=FieldSystem(self)
        # First contact teaches the device on safe ground.
        sx,sy=self.devices[0]
        for enemy in world.enemies:
            if abs(enemy.rect.centerx-sx)<260 and abs(enemy.rect.bottom-sy)<130:
                floors=[p for p in world.platforms if not p.oneway and not p.moving and p.rect.w>=240 and p.rect.left>sx+300]
                if floors:
                    floor=min(floors,key=lambda p:p.rect.left)
                    enemy.left=floor.rect.left+35;enemy.right=floor.rect.right-35
                    enemy.rect.midbottom=(max(enemy.left+22,min(enemy.right-22,enemy.rect.centerx)),floor.rect.top-(100 if enemy.kind=='flyer' else 0))
                    enemy.base_y=enemy.rect.y

    @property
    def completed(self):return self.state['step']>=3 and self.field.done
    def restore(self,value):
        step=value.get('step',0)
        self.state['step']=max(0,min(3,step)) if type(step) is int else 0
        self.state['activated']=[i for i in value.get('activated',[]) if type(i) is int and 0<=i<3] if isinstance(value.get('activated',[]),list) else []
        # Mounting never survives loading; restore to a safe anchor first.
        self.state['vehicle']=False
        self.state['sea_complete']=value.get('sea_complete') is True
        self.field.restore(value)
    def near(self):
        p=self.world.player.rect
        return next((i for i,(x,y) in enumerate(self.devices) if abs(p.centerx-x)<90 and abs(p.bottom-y)<110),None)
    def activate(self,index,choice=None):
        if index in self.state['activated']:return 'revisit'
        # Each field operation must be applied in order, with guided feedback.
        if index>self.state['step']:return 'Busca primero el puesto anterior; aparece marcado en tu plano.'
        if choice is not None and choice!=index:return 'Observa la secuencia y vuelve a elegir. No pierdes energía ni puntos.'
        self.state['activated'].append(index);self.state['step']=len(self.state['activated'])
        w=self.world
        if self.vehicle_kind and index==1:self.state['vehicle']=True
        if self.completed:
            w.say('Actividad completada: atajo temporal y apoyo contra el guardián disponibles.')
            if w.boss:w.boss.field_support=True
        else:w.say('Puesto activado · '+self.operations[index]+'. Continúa hasta el siguiente hito.')
        return 'ok'

    def update(self,dt,controls):
        w=self.world;p=w.player;t=w.time;step=self.state['step']
        self.state['vehicle']=False
        self.gravity=.48 if self.kind=='lunar' else 1.
        self.wind=(math.sin(t*.55)*38 if self.kind in ('wind','provisions','radio') else 0.)
        self.speed=.85 if self.kind=='plaza' and step<2 else 1.
        nearest=min((abs(p.rect.centerx-x) for x,y in self.devices),default=9999)
        self.sheltered=nearest<140 and step>0 and self.kind in ('shelter','siren','warmth','ash','radio')
        if self.sheltered:p.invincible=max(p.invincible,.1)
        if self.kind=='warmth' and nearest<100 and step and int(t*120)%600==0:p.hp=min(p.max_hp,p.hp+1)
        if self.state['vehicle']:
            p.dash_time=0.;p.hurt_time=0.;p.cooldown=max(0,p.cooldown-dt);p.anim+=dt*3
            # A controllable temporal support craft bridges gaps; dismount with E.
            vx=controls.axis*(380 if self.kind=='naval' else 300)
            if abs(controls.axis)>.1:p.facing=1 if controls.axis>0 else -1
            self.state['vehicle_x']=max(60,min(w.width-80,self.state['vehicle_x']+vx*dt))
            vy=(-controls.held+controls.drop)*150 if self.kind in ('naval','canal','tide') else 0
            self.state['vehicle_y']=max(330,min(525,self.state['vehicle_y']+vy*dt))
            p.rect.midbottom=(self.state['vehicle_x'],self.state['vehicle_y']);p.vx=vx;p.vy=0;p.grounded=True;p.dash_ready=True
        # Earned support has tangible traversal and combat effects.
        if self.completed:
            p.cooldown=max(0,p.cooldown-dt*.35)
            if w.boss:w.boss.field_support=True
        return bool(self.state['vehicle'])

    def dismount(self):
        if not self.state['vehicle']:return False
        p=self.world.player
        # Always disembark on nearest real surface, never over a gap.
        candidates=[f for f in self.world.platforms if not f.moving and f.rect.w>110]
        floor=min(candidates,key=lambda f:abs(f.rect.centerx-p.rect.centerx))
        p.rect.midbottom=(max(floor.rect.left+25,min(floor.rect.right-25,p.rect.centerx)),floor.rect.top)
        p.vx=p.vy=0;self.state['vehicle']=False;return True

    def draw(self,s,camera,t):
        self.field.draw(s,camera,t)
        for i,(wx,y) in enumerate(self.devices):
            x=wx-camera
            if not -160<x<s.get_width()+160:continue
            active=i in self.state['activated'];c=CYAN if active else GOLD
            # Compact markers; detailed tools are inspected in the activity panel.
            rect(s,(30,44,49),(x-18,y-44,36,38),5)
            rect(s,(94,102,97),(x-23,y-6,46,6),2)
            if self.kind in ('wheel','steam','counterweight','crane'):
                circle(s,c,(x,y-49),22,3)
                for n in range(6):
                    a=n*math.pi/3+(t if active else 0)
                    line(s,c,(x,y-49),(x+math.cos(a)*19,y-49+math.sin(a)*19),2)
            elif self.kind in ('radio','packet','circuit','telescope','beacon'):
                line(s,c,(x,y-73),(x,y-110),3)
                for n in range(3):pg.draw.arc(s,c,pg.Rect(x-12-n*7,y-117-n*7,24+n*14,24+n*14),.3,2.8,2)
                circle(s,c,(x,y-44),10,2)
            elif self.kind in ('shelter','siren','ash','warmth','provisions','escort'):
                polygon(s,(89,110,104),[(x-62,y-6),(x,y-103),(x+62,y-6)])
                line(s,c,(x,y-95),(x,y-12),2)
                rect(s,(22,35,41),(x-19,y-39,38,35),2)
            elif self.kind in ('naval','canal','tide'):
                for radius in (22,29):pg.draw.ellipse(s,c,pg.Rect(x-radius,y-76,radius*2,70),2)
                polygon(s,(194,167,113),[(x-12,y-31),(x+12,y-31),(x+7,y-20),(x-8,y-20)])
            else:
                polygon(s,c,[(x-19,y-60),(x,y-67),(x+19,y-60),(x+19,y-27),(x,y-21),(x-19,y-27)],2)
                line(s,c,(x,y-61),(x,y-28),2)
            diamond(s,(x,y-119),6,c,active)
            if abs(wx-self.world.player.rect.centerx)<160:
                text(s,f'E · Puesto {i+1}'+(' · LISTO' if active else ''),(x,y-139),12,c,True,'center')
        if self.state['vehicle']:
            x=self.state['vehicle_x']-camera;y=self.state['vehicle_y']
            polygon(s,(90,69,56),[(x-80,y+4),(x+85,y+4),(x+55,y+35),(x-55,y+35)])
            for j in range(8):line(s,(161,129,83),(x-63+j*18,y+6),(x-56+j*16,y+27),2)
            line(s,(223,209,168),(x-24,y+3),(x-24,y-90),4)
            polygon(s,(222,211,167),[(x-19,y-86),(x-19,y-21),(x+40,y-21)])
            rect(s,(49,61,64),(x+25,y-7,55,9),2)
            text(s,'E desembarcar · F cañón · ↑/↓ altura',(x,y+49),12,CYAN,True,'center')
        if self.state['escort_x']:
            x=self.state['escort_x']-camera
            if -90<x<1370:
                rect(s,(123,100,72),(x-18,541,36,25),3);circle(s,(211,172,136),(x,526),10)
                text(s,'A SALVO',(x,509),11,CYAN,True,'center')
