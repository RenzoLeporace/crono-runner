"""Prepare historical prerequisites in tests whose subject is another system."""
def complete_story(world):
    m=world.mechanic;f=m.field
    m.state.update(step=3,activated=[0,1,2],sea_complete=True)
    f.collected={0,1,2};f.crossed={0,1,2};f.distance=900;f.sheltered_time=3
    f.escort_x=m.devices[2][0];f.persist()
    world.answered.add(world.level_id*2)
