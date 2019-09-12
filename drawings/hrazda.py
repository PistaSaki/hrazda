import numpy as np
from FreeCAD import Placement, Vector, Rotation
import Draft
    
doc = App.ActiveDocument


def get_box(dims=[1, 1, 1], shift=[0, 0, 0]):
    box = doc.addObject("Part::Box","Box")
    box.Placement.move(Vector(shift))
    box.Length, box.Width, box.Height = dims
    return box


def get_L(length, width, thickness, left=True, shift=[0, 0, 0]):
    shift = np.array(shift)
    box1 = get_box([length, width, width], shift = shift)
    if left:
        shift2 = shift + np.array([0, thickness, thickness])
    else:
        shift2 = shift + np.array([0, -thickness, thickness])
    box2 = get_box([length, width, width], shift = shift2)    
    cut = doc.addObject("Part::Cut","Cut")
    cut.Base = box1
    cut.Tool = box2
    return cut

def get_rails(length, thickness, width, distance, shift=[0,0,0]):
    shift = np.array(shift)
    left = get_L(length, width, thickness, shift = shift)
    shift = shift + [0, distance - width, 0]
    right = get_L(length, width, thickness, shift=shift, left=False)
    return (left, right)

#get_rails(length = 3887, thickness = 5, width = 50, distance=1610)

def make_steps(rail_dist, step_rail_gap, step_diam, first_step, padding,
               L_thickness, n_steps, step_dist):
    step_length = rail_dist - 2*L_thickness - 2 * step_rail_gap
    cyl = doc.addObject("Part::Cylinder","Cylinder")
    cyl.Height = step_length
    cyl.Radius = step_diam / 2
    shift = [first_step, (rail_dist - step_length) / 2,
             step_diam / 2 + padding + L_thickness]
    cyl.Placement = Placement(Vector(shift), Rotation(Vector(1, 0, 0), -90))
        
    obj = Draft.makeArray(cyl,Vector(step_dist,0,0),Vector(0,1,0),n_steps, 1)
    Draft.autogroup(obj)
    return obj

##make_steps(
##    rail_dist = 1610,
##    step_rail_gap = 10,
##    step_diam = 30,
##    first_step = 100,
##    padding = 1,
##    L_thickness = 5,
##    n_steps = 10,
##    step_dist = 300,
##)


def get_ladder(length, rail_dist, step_rail_gap, step_diam, first_step,
               padding,L_thickness, L_width, step_dist):
    rails = get_rails(length=length, thickness=L_thickness,
              width=L_width, distance=rail_dist)
    n_steps = (length - first_step) // step_dist + 1
    steps = make_steps(
        rail_dist=rail_dist, step_rail_gap=step_rail_gap,
        step_diam=step_diam,
        first_step=first_step,
        padding=padding,
        L_thickness=L_thickness,
        n_steps=n_steps,
        step_dist=step_dist,
    )
    return rails, steps



get_ladder(
    length = 3887,
    rail_dist = 1610,
    step_rail_gap = 10,
    step_diam = 30,
    first_step = 100,
    padding = 1,
    L_thickness = 5,
    L_width = 50,
    step_dist = 300,
)
