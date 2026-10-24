"""Visual roles shared by collision bodies, the renderer and the field guide."""
ROLES={
 2:dict(walker='Hoplita',sentry='Arquero de bronce',charger='Lancero',armored='Hoplita con escudo'),
 3:dict(walker='Hombre de armas',sentry='Ballestero',charger='Caballero',armored='Guardia de placas'),
 4:dict(sentry='Operario de vapor',armored='Autómata de caldera'),
 5:dict(walker='Infantería',sentry='Fusilero',charger='Patrulla de asalto'),
 6:dict(walker='Robot de vigilancia',sentry='Unidad de precisión',armored='Robot de protección'),
 8:dict(walker='Guardia del Nilo',sentry='Arquero del templo',charger='Lancero del desierto',armored='Guardián de escudo'),
}
HEIGHTS={2:76,3:78,4:80,5:76,6:80,8:76}

def humanoid(era,kind):
    return kind in ROLES.get(era,{})
