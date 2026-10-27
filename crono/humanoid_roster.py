"""Visual roles shared by collision bodies, the renderer and the field guide."""
ROLES={
 2:dict(walker='Hoplita',sentry='Arquero de bronce',charger='Lancero',armored='Hoplita con escudo'),
 3:dict(walker='Hombre de armas',sentry='Ballestero',charger='Caballero',armored='Guardia de placas'),
 4:dict(walker='Guardia de fábrica',hopper='Vigilante de pasarela',sentry='Guarda de almacén',charger='Capataz',armored='Guardia con protección'),
 5:dict(walker='Infantería',hopper='Explorador',sentry='Fusilero',charger='Patrulla de asalto',armored='Infantería protegida'),
 6:dict(walker='Vigilante',hopper='Patrulla',sentry='Guardia',charger='Agente de seguridad',armored='Guardia con escudo'),
 8:dict(walker='Guardia del Nilo',sentry='Arquero del templo',charger='Lancero del desierto',armored='Guardián de escudo'),
}
HEIGHTS={2:76,3:78,4:80,5:76,6:80,8:76}

def humanoid(era,kind):
    return kind in ROLES.get(era,{})
