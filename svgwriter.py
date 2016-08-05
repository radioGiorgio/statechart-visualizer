import svgwrite
from structures.box import Box, radius, char_width

normal_style = "font-size:25;font-family:Arial"
italic_style = "font-size:25;font-family:Arial;font-style:oblique"
bold_style = "font-size:25;font-weight:bold;font-family:Arial"


def get_shape(box: Box):
    """
    get the svg object associated with the shape of the Box

    :param box: the box to render
    :return: the svg object related
    """
    x, y = box.coordinates[0]
    if box.shape == 'rectangle':
        return svgwrite.shapes.Rect(insert=(x, y), size=(box.width, box.height),
                                    fill=svgwrite.rgb(135, 206, 235),
                                    stroke='black', stroke_width=1)
    elif box.shape == 'circle':
        return svgwrite.shapes.Circle(center=(x + radius, y + radius), r=radius)
    else:
        return svgwrite.shapes.Rect(insert=(x, y), size=(box.width, box.height),
                                    fill="#044B94", fill_opacity="0.4")


def render_box(box: Box):
    """
    creates the shapes of the boxes and puts it in a svg group

    :param box: the box to render
    :return: the group that contains the box and their inner boxes
    """
    g = svgwrite.container.Group()

    # First draw the main box
    shape = get_shape(box)
    g.add(shape)

    # Now draw the name of the box
    w, h = box.get_text_position_of('name')
    if box.parallel_states:
        t1 = svgwrite.text.Text("<<parallel>>", insert=(w, h), style=italic_style, textLength=13 * char_width)
        t2 = svgwrite.text.Text(box.name, insert=(w + 14 * char_width, h), style=bold_style,
                                textLength=len(box.name) * char_width)
        g.add(t1)
        g.add(t2)
    else:
        g.add(svgwrite.text.Text(box.name, insert=(w, h), style=bold_style, textLength=len(box.name) * char_width))

    # This draws the 'on entry' zone
    w, h = box.get_text_position_of('entry')
    if box.entry != '':
        g.add(svgwrite.text.Text("entry / ", insert=(w, h), style=italic_style, textLength=8 * char_width))
        g.add(svgwrite.text.Text(box.entry, insert=(w + 9 * char_width, h), style=normal_style,
                                 textLength=len(box.entry) * char_width))

    # TODO: exit zone
    # TODO : do zone

    # Finally draw the children following the axis (horizontal or vertical)
    for child in box.children:
        g.add(render_box(child))

    return g


def render_transitions(transitions):
    lines = []
    for t in transitions:
        (x1, y1), (x2, y2) = t.coordinates
        lines += [svgwrite.shapes.Line(start=(x1, y1), end=(x2, y2), stroke='black', stroke_width=1,
                                       marker_end="url(#arrow)")]
    return lines


def export(box: Box):
    """
    Creates the svg file that represents the Box

    :param box: the box that will be on the svg file
    """
    dwg = svgwrite.Drawing(box.name + ".svg", size=(box.width, box.height))
    dwg.add(render_box(box))
    marker = svgwrite.container.Marker(insert=(8, 3), orient='auto', markerWidth=30, markerHeight=20,
                                       id="arrow")
    path = svgwrite.path.Path(d="M0,0 L0,6 L9,3 z")
    marker.add(path)
    dwg.defs.add(marker)
    for transition in render_transitions(box.transitions):
        dwg.add(transition)
    dwg.save()
