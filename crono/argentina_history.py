"""Roles and historical framing, separate from the student's question bank."""
CONTEXT=(
    'Mayo de 1810 fue un proceso político. La aventura combina su escenario con figuras realistas de ficción inspiradas en los conflictos del período.',
    'La escena combina el Congreso de Tucumán de 1816 con ecos de las guerras de independencia. Los uniformes son interpretaciones, no réplicas de un regimiento.',
    'La dictadura ejerció terrorismo de Estado; también hubo atentados de organizaciones armadas. Los enemigos evocan violencias previas al regreso democrático de 1983.',
)
SIMPLE_CONTEXT='En 1983 se recuperó la democracia. Los adversarios representan violencias del pasado; las personas que celebran el regreso democrático no son enemigos.'
FACTION_LABELS={'royalist':'Realistas','state_force':'Militares · represión estatal','armed_cell':'Organizaciones armadas · terrorismo'}
ROLE_NAMES={'walker':'Fusilero realista','hopper':'Granadero realista','sentry':'Tirador realista',
            'charger':'Oficial realista','armored':'Coracero realista'}

def role_for(enemy):
    if enemy.stage<2:return ROLE_NAMES.get(enemy.kind,'Realista')
    return 'Militar · eco del pasado' if enemy.faction=='state_force' else 'Célula terrorista · eco del pasado'

def annotate_roster(specs,stage):
    for n,spec in enumerate(specs):
        # Human adversaries never inherit the old flying-animal behaviour.
        if spec['kind']=='flyer':spec['kind']='sentry'
        spec.update(stage=stage,faction='royalist' if stage<2 else ('state_force' if n%2==0 or spec['kind']=='armored' else 'armed_cell'))
    return specs
