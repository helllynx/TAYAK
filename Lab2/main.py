import os, sys, inspect

cmd_folder = os.path.realpath(
    os.path.dirname(
        os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from transitions import *
from transitions.extensions import GraphMachine
from IPython.display import Image, display, display_png

class Matter(object):
    def is_valid(self):
        return True

    def is_not_valid(self):
        return False

    def is_also_valid(self):
        return True

    # graph object is created by the machine
    def show_graph(self, **kwargs):
        self.get_graph(**kwargs).draw('state.png', prog='dot')
        display(Image('state.png'))


transitions = [
    ['melt', 'solid', 'liquid'],
    ['evaporate', 'liquid', 'gas'],
    ['sublimate', 'solid', 'gas'],
    ['ionize', 'gas', 'plasma']
]
states=['solid', 'liquid', 'gas', 'plasma']

model = Matter()
machine = GraphMachine(model=model,
                       states=states,
                       transitions=transitions,
                       initial='solid',
                       show_auto_transitions=False, # default value is False
                       title="Lab2",
                       show_conditions=True)
model.show_graph()

