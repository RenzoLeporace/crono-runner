"""Roles and historical framing, separate from the student's question bank."""
CONTEXT=(
    'La Revolución de Mayo de 1810 fue un proceso político que llevó a la formación de la Primera Junta de gobierno en Buenos Aires.',
    'El Congreso de Tucumán declaró la independencia el 9 de julio de 1816. En Cuyo, San Martín preparaba la expedición que cruzaría los Andes en 1817.',
    'La última dictadura argentina gobernó entre 1976 y 1983 y ejerció terrorismo de Estado. Las elecciones del 30 de octubre de 1983 precedieron a la asunción de Raúl Alfonsín el 10 de diciembre.',
)
SIMPLE_CONTEXT='En 1983 se recuperó la democracia en Argentina. La ciudadanía volvió a elegir presidente mediante el voto. Raúl Alfonsín asumió el 10 de diciembre.'
FACTION_LABELS={'royalist':'Realistas','state_force':'Militares · represión estatal','armed_cell':'Organizaciones armadas · terrorismo'}
ROLE_NAMES={'walker':'Fusilero realista','hopper':'Granadero realista','sentry':'Tirador realista',
            'charger':'Oficial realista','armored':'Coracero realista'}

def role_for(enemy):
    if enemy.faction=='naval_raider':return 'Marinero · eco anglofrancés'
    if enemy.faction=='imperial_brazil':return 'Marinero · Imperio del Brasil'
    if enemy.stage<2:return ROLE_NAMES.get(enemy.kind,'Realista')+' · Corona española'
    return 'Militar · eco del pasado' if enemy.faction=='state_force' else 'Célula terrorista · eco del pasado'

def annotate_roster(specs,stage):
    for n,spec in enumerate(specs):
        # Human adversaries never inherit the old flying-animal behaviour.
        if spec['kind']=='flyer':spec['kind']='sentry'
        spec.update(stage=stage,faction='royalist' if stage<2 else ('state_force' if n%2==0 or spec['kind']=='armored' else 'armed_cell'))
    return specs
