import tkinter
import turtle


def Turtle(shape=turtle._CFG["shape"],
           undobuffersize=turtle._CFG["undobuffersize"],
           visible=turtle._CFG["visible"]) -> turtle.Turtle:
    """RawTurtle auto-creating (scrolled) canvas.

    When a Turtle object is created or a function derived from some
    Turtle method is called a TurtleScreen object is automatically created.
    """
    new_turtle: turtle.Turtle = turtle.Turtle(shape=shape, undobuffersize=undobuffersize, visible=visible)
    move_screen_to_top(screen=new_turtle.getscreen())
    return new_turtle


__turtle: turtle.Turtle = None


def __SingletonTurtle() -> turtle.Turtle:
    global __turtle
    if (__turtle is None):
        __turtle = Turtle()
    return __turtle


def Screen() -> turtle._Screen:
    """Return the singleton screen object.
    If none exists at the moment, create a new one and return it,
    else return the existing one."""
    return turtle.Screen()


__is_screen_topmost = {}


def move_screen_to_top(screen: turtle._Screen = None):
    '''
    Moves the given screen over all other windows and keeps it there. Defaults to the Screen() object.
    '''
    global __is_screen_topmost
    if screen is None:
        screen = Screen()

    canvas = screen.getcanvas()
    if id(canvas) not in __is_screen_topmost:
        tk_screen = canvas.winfo_toplevel()
        tk_screen.call('wm', 'attributes', '.', '-topmost', '0')
        tk_screen.call('wm', 'attributes', '.', '-topmost', '1')
        __is_screen_topmost[id(canvas)] = True


def clone() -> turtle.Turtle:
    """Create and return a clone of the turtle.

    No argument.

    Create and return a clone of the turtle with same position, heading
    and turtle properties.

    Example (for a Turtle instance named mick):
    mick = Turtle()
    joe = mick.clone()
    """
    return __SingletonTurtle().clone()


def getturtle() -> turtle.Turtle:
    """Return the Turtleobject itself.

    No argument.

    Only reasonable use: as a function to return the 'anonymous turtle':

    Example:
    >>> pet = getturtle()
    >>> pet.fd(50)
    >>> pet
    <turtle.Turtle object at 0x0187D810>
    >>> turtles()
    [<turtle.Turtle object at 0x0187D810>]
    """
    return __SingletonTurtle()


def getpen() -> turtle.Turtle:
    """Return the Turtleobject itself.

    No argument.

    Only reasonable use: as a function to return the 'anonymous turtle':

    Example:
    >>> pet = getturtle()
    >>> pet.fd(50)
    >>> pet
    <turtle.Turtle object at 0x0187D810>
    >>> turtles()
    [<turtle.Turtle object at 0x0187D810>]
    """
    return __SingletonTurtle().getpen()


def getscreen() -> turtle._Screen:
    """Return the TurtleScreen object, the turtle is drawing  on.

    No argument.

    Return the TurtleScreen object, the turtle is drawing  on.
    So TurtleScreen-methods can be called for that object.

    Example (for a Turtle instance named turtle):
    >>> ts = turtle.getscreen()
    >>> ts
    <turtle.TurtleScreen object at 0x0106B770>
    >>> ts.bgcolor("pink")
    """
    return __SingletonTurtle().getscreen()


Screen().setup(500, 500, None, None)


def right(angle: int = 90):
    '''turns the pen direction to the right

    Parameters
    ----------
            angle : int, optional (default: 90)
            degrees to turn right
    '''
    __SingletonTurtle().right(angle)


def left(angle: int = 90):
    '''turns the pen direction to the left

    Parameters
    ----------
            angle : int, optional (default: 90)
            degrees to turn left
    '''
    __SingletonTurtle().left(angle)


def forward(step: int = 10):
    '''Moves the pen forward

    Parameters
    ----------
            step : int, optional
            pixels to go forward
    '''
    __SingletonTurtle().forward(step)


def backward(step: int = 10):
    """Move the turtle backward by distance.

    Argument:
    distance -- a number

    Move the turtle backward by distance ,opposite to the direction the
    turtle is headed. Do not change the turtle's heading.

    Example (for a Turtle instance named turtle):
    >>> turtle.position()
    (0.00, 0.00)
    >>> turtle.backward(30)
    >>> turtle.position()
    (-30.00, 0.00)
    """
    __SingletonTurtle().backward(step)


def step_down():
    '''draws a step down on a stair'''
    right()
    forward()
    left()
    forward()


def step_up():
    '''draws a step up on a stair'''
    left()
    forward()
    right()
    forward()


def done():
    '''hides the turtle and waits until the resulting window is clicked'''
    __SingletonTurtle().hideturtle()
    Screen().update()
    Screen().exitonclick()


def goto(x: int, y: int = None, draw: bool = True):
    """Move turtle to an absolute position.

    Aliases: setpos | goto:

    Arguments:
    x -- a number      or     a pair/vector of numbers
    y -- a number             None
    draw -- bool              True

    call: `goto(x, y)`        # two coordinates
    --or: `goto((x, y))`      # a pair (tuple) of coordinates
    --or: `goto(vec)`         # e.g. as returned by pos()

    Move turtle to an absolute position. If the pen is down and draw=True,
    a line will be drawn. The turtle's orientation does not change.

    Example (for a Turtle instance named turtle):
    >>> tp = turtle.pos()
    >>> tp
    (0.00, 0.00)
    >>> turtle.setpos(60,30)
    >>> turtle.pos()
    (60.00,30.00)
    >>> turtle.setpos((20,80))
    >>> turtle.pos()
    (20.00,80.00)
    >>> turtle.setpos(tp)
    >>> turtle.pos()
    (0.00,0.00)
    """

    was_down = False

    if not draw:
        was_down = __SingletonTurtle().isdown()
        __SingletonTurtle().penup()

    __SingletonTurtle().goto(x, y=y)

    if not draw and was_down:
        __SingletonTurtle().pendown()


def home(draw: bool = True):
    """
    Move turtle to the origin - coordinates (0,0).

    Arguments:
    draw -- bool              True

    Move turtle to the origin - coordinates (0,0) and set its
    heading to its start-orientation (which depends on mode).

    Example (for a Turtle instance named turtle):
    >>> turtle.home()
    """
    if draw == False:
        goto(0, 0, draw=False)
    __SingletonTurtle().home()


def pos() -> turtle.Vec2D:
    """Return the turtle's current location (x,y), as a Vec2D-vector.

    Aliases: pos | position

    No arguments.

    Example (for a Turtle instance named turtle):
    >>> turtle.pos()
    (0.00, 240.00)
    """
    __SingletonTurtle().pos()


def position() -> turtle.Vec2D:
    """Return the turtle's current location (x,y), as a Vec2D-vector.

    Aliases: pos | position

    No arguments.

    Example (for a Turtle instance named turtle):
    >>> turtle.pos()
    (0.00, 240.00)
    """
    __SingletonTurtle().pos()


def setpos(x: int, y: int = None, draw=False):
    """Move turtle to an absolute position.

    Aliases: setpos | goto:

    Arguments:
    x -- a number      or     a pair/vector of numbers
    y -- a number             None

    call: goto(x, y)         # two coordinates
    --or: goto((x, y))       # a pair (tuple) of coordinates
    --or: goto(vec)          # e.g. as returned by pos()

    Move turtle to an absolute position. If the pen is down,
    a line will be drawn. The turtle's orientation does not change.

    Example (for a Turtle instance named turtle):
    >>> tp = turtle.pos()
    >>> tp
    (0.00, 0.00)
    >>> turtle.setpos(60,30)
    >>> turtle.pos()
    (60.00,30.00)
    >>> turtle.setpos((20,80))
    >>> turtle.pos()
    (20.00,80.00)
    >>> turtle.setpos(tp)
    >>> turtle.pos()
    (0.00,0.00)
    """
    goto(x, y, draw=draw)


def heading() -> float:
    '''
    Return the turtle's current heading.
    '''
    return __SingletonTurtle().heading()


def setheading(to_angle) -> float:
    """Set the orientation of the turtle to to_angle.

    Parameters
    ----------
    to_angle -- a number (integer or float)

    Set the orientation of the turtle to to_angle.
    Here are some common directions in degrees:

    |    standard - mode: |          logo-mode:|
    |:--------------------|:-------------------|
    |    0 - east         |       0 - north    |
    |    90 - north       |       90 - east    |
    |    180 - west       |       180 - south  |
    |    270 - south      |       270 - west   |

    Example (for a Turtle instance named turtle):
    >>> turtle.setheading(90)
    >>> turtle.heading()
    90
    """
    return __SingletonTurtle().setheading(to_angle=to_angle)


def fillcolor(*args):
    """ Return or set the fillcolor.

    Arguments:
    Four input formats are allowed:
        - fillcolor()
        Return the current fillcolor as color specification string,
        possibly in hex-number format (see example).
        May be used as input to another color/pencolor/fillcolor call.
        - fillcolor(colorstring)
        s is a Tk color specification string, such as "red" or "yellow"
        - fillcolor((r, g, b))
        *a tuple* of r, g, and b, which represent, an RGB color,
        and each of r, g, and b are in the range 0..colormode,
        where colormode is either 1.0 or 255
        - fillcolor(r, g, b)
        r, g, and b represent an RGB color, and each of r, g, and b
        are in the range 0..colormode

    If turtleshape is a polygon, the interior of that polygon is drawn
    with the newly set fillcolor.

    Example (for a Turtle instance named turtle):
    >>> turtle.fillcolor('violet')
    >>> col = turtle.pencolor()
    >>> turtle.fillcolor(col)
    >>> turtle.fillcolor(0, .5, 0)
    """
    return __SingletonTurtle().fillcolor(*args)


def color(*args):
    """Return or set the pencolor and fillcolor.

    Arguments:
    Several input formats are allowed.
    They use 0, 1, 2, or 3 arguments as follows:

    color()
        Return the current pencolor and the current fillcolor
        as a pair of color specification strings as are returned
        by pencolor and fillcolor.
    color(colorstring), color((r,g,b)), color(r,g,b)
        inputs as in pencolor, set both, fillcolor and pencolor,
        to the given value.
    color(colorstring1, colorstring2),
    color((r1,g1,b1), (r2,g2,b2))
        equivalent to pencolor(colorstring1) and fillcolor(colorstring2)
        and analogously, if the other input format is used.

    If turtleshape is a polygon, outline and interior of that polygon
    is drawn with the newly set colors.
    For more info see: pencolor, fillcolor

    Example (for a Turtle instance named turtle):
    >>> turtle.color('red', 'green')
    >>> turtle.color()
    ('red', 'green')
    >>> colormode(255)
    >>> color((40, 80, 120), (160, 200, 240))
    >>> color()
    ('#285078', '#a0c8f0')
    """
    __SingletonTurtle().color(*args)
    return __SingletonTurtle().color()


def colormode(cmode=None):
    """Return the colormode or set it to 1.0 or 255.

    Optional argument:
    cmode -- one of the values 1.0 or 255

    r, g, b values of colortriples have to be in range 0..cmode.

    Example (for a TurtleScreen instance named screen):
    >>> screen.colormode()
    1.0
    >>> screen.colormode(255)
    >>> pencolor(240,160,80)
    """
    return Screen().colormode(cmode=cmode)


def pencolor(*args):
    """ Return or set the pencolor.

    Arguments:
    Four input formats are allowed:
        - pencolor()
        Return the current pencolor as color specification string,
        possibly in hex-number format (see example).
        May be used as input to another color/pencolor/fillcolor call.
        - pencolor(colorstring)
        s is a Tk color specification string, such as "red" or "yellow"
        - pencolor((r, g, b))
        *a tuple* of r, g, and b, which represent, an RGB color,
        and each of r, g, and b are in the range 0..colormode,
        where colormode is either 1.0 or 255
        - pencolor(r, g, b)
        r, g, and b represent an RGB color, and each of r, g, and b
        are in the range 0..colormode

    If turtleshape is a polygon, the outline of that polygon is drawn
    with the newly set pencolor.

    Example (for a Turtle instance named turtle):
    >>> turtle.pencolor('brown')
    >>> tup = (0.2, 0.8, 0.55)
    >>> turtle.pencolor(tup)
    >>> turtle.pencolor()
    '#33cc8c'
    """
    return __SingletonTurtle().pencolor(*args)


def clear():
    """Delete all drawings and all turtles from the TurtleScreen.

    No argument.

    Reset empty TurtleScreen to its initial state: white background,
    no backgroundimage, no eventbindings and tracing on.

    Example (for a TurtleScreen instance named screen):
    >>> screen.clear()

    Note: this method is not available as function.
    """
    return __SingletonTurtle().clear()


def distance(x, y=None):
    """Return the distance from the turtle to (x,y) in turtle step units.

    Arguments:
    x -- a number   or  a pair/vector of numbers   or   a turtle instance
    y -- a number       None                            None

    call: distance(x, y)         # two coordinates
    --or: distance((x, y))       # a pair (tuple) of coordinates
    --or: distance(vec)          # e.g. as returned by pos()
    --or: distance(mypen)        # where mypen is another turtle

    Example (for a Turtle instance named turtle):
    >>> turtle.pos()
    (0.00, 0.00)
    >>> turtle.distance(30,40)
    50.0
    >>> pen = Turtle()
    >>> pen.forward(77)
    >>> turtle.distance(pen)
    77.0
    """
    return __SingletonTurtle().distance(x, y=y)


def dot():
    """Draw a dot with diameter size, using color.

    Optional arguments:
    size -- an integer >= 1 (if given)
    color -- a colorstring or a numeric color tuple

    Draw a circular dot with diameter size, using color.
    If size is not given, the maximum of pensize+4 and 2*pensize is used.

    Example (for a Turtle instance named turtle):
    >>> turtle.dot()
    >>> turtle.fd(50); turtle.dot(20, "blue"); turtle.fd(50)
    """
    return __SingletonTurtle().dot()


def pendown():
    """Pull the pen down -- drawing when moving.

    Aliases: pendown | pd | down

    No argument.

    Example (for a Turtle instance named turtle):
    >>> turtle.pendown()
    """
    return __SingletonTurtle().pendown()


def penup():
    """Pull the pen up -- no drawing when moving.

    Aliases: penup | pu | up

    No argument

    Example (for a Turtle instance named turtle):
    >>> turtle.penup()
    """
    return __SingletonTurtle().penup()


def pensize(width=None):
    """Set or return the line thickness.

    Aliases:  pensize | width

    Argument:
    width -- positive number

    Set the line thickness to width or return it. If resizemode is set
    to "auto" and turtleshape is a polygon, that polygon is drawn with
    the same line thickness. If no argument is given, current pensize
    is returned.

    Example (for a Turtle instance named turtle):
    >>> turtle.pensize()
    1
    >>> turtle.pensize(10)   # from here on lines of width 10 are drawn
    """
    return __SingletonTurtle().pensize(width=width)


def begin_fill(width=None):
    """Called just before drawing a shape to be filled.

    No argument.

    Example (for a Turtle instance named turtle):
    >>> turtle.color("black", "red")
    >>> turtle.begin_fill()
    >>> turtle.circle(60)
    >>> turtle.end_fill()
    """
    return __SingletonTurtle().begin_fill()


def end_fill(width=None):
    """Fill the shape drawn after the call begin_fill().

    No argument.

    Example (for a Turtle instance named turtle):
    >>> turtle.color("black", "red")
    >>> turtle.begin_fill()
    >>> turtle.circle(60)
    >>> turtle.end_fill()
    """
    return __SingletonTurtle().end_fill()


def isdown() -> bool:
    """Return True if pen is down, False if it's up.

    No argument.

    Example (for a Turtle instance named turtle):
    >>> turtle.penup()
    >>> turtle.isdown()
    False
    >>> turtle.pendown()
    >>> turtle.isdown()
    True
    """
    return __SingletonTurtle().isdown()


def write(arg, move=False, align="left", font=("Arial", 8, "normal")):
    """Write text at the current turtle position.

    Arguments:
    arg -- info, which is to be written to the TurtleScreen
    move (optional) -- True/False
    align (optional) -- one of the strings "left", "center" or right"
    font (optional) -- a triple (fontname, fontsize, fonttype)

    Write text - the string representation of arg - at the current
    turtle position according to align ("left", "center" or right")
    and with the given font.
    If move is True, the pen is moved to the bottom-right corner
    of the text. By default, move is False.

    Example (for a Turtle instance named turtle):
    >>> turtle.write('Home = ', True, align="center")
    >>> turtle.write((0,0), True)
    """
    return __SingletonTurtle().write(arg, move=move, align=align, font=font)


def hideturtle():
    """Makes the turtle invisible.

    Aliases: hideturtle | ht

    No argument.

    It's a good idea to do this while you're in the
    middle of a complicated drawing, because hiding
    the turtle speeds up the drawing observably.

    Example (for a Turtle instance named turtle):
    >>> turtle.hideturtle()
    """
    return __SingletonTurtle().hideturtle()


def speed(speed=None):
    """ Return or set the turtle's speed.

    Optional argument:
    speed -- an integer in the range 0..10 or a speedstring (see below)

    Set the turtle's speed to an integer value in the range 0 .. 10.
    If no argument is given: return current speed.

    If input is a number greater than 10 or smaller than 0.5,
    speed is set to 0.
    Speedstrings  are mapped to speedvalues in the following way:
        'fastest' :  0
        'fast'    :  10
        'normal'  :  6
        'slow'    :  3
        'slowest' :  1
    speeds from 1 to 10 enforce increasingly faster animation of
    line drawing and turtle turning.

    Attention:
    speed = 0 : *no* animation takes place. forward/back makes turtle jump
    and likewise left/right make the turtle turn instantly.

    Example (for a Turtle instance named turtle):
    >>> turtle.speed(3)
    """
    return __SingletonTurtle().speed(speed)


def showturtle():
    """Makes the turtle visible.

    Aliases: showturtle | st

    No argument.

    Example (for a Turtle instance named turtle):
    >>> turtle.hideturtle()
    >>> turtle.showturtle()
    """
    return __SingletonTurtle().showturtle()


def isvisible():
    """Return True if the Turtle is shown, False if it's hidden.

    No argument.

    Example (for a Turtle instance named turtle):
    >>> turtle.hideturtle()
    >>> print turtle.isvisible():
    False
    """
    return __SingletonTurtle().isvisible()


def grid(xmin: int, xmax: int, ymin: int, ymax: int, tick: int, scale: int = 1):
    '''draws a grid and draws the coordinate numbers
    '''
    if tkinter.TkVersion < 8.6:
        raise "TkVersion must be >= 8.6"
    old_pos = getturtle().pos()
    old_pensize = getturtle().pensize()
    pensize(1)
    old_color = getturtle().color()
    old_update_freq = Screen().tracer()
    old_delay = Screen().delay()
    Screen().tracer(0, 0)
    pencolor('lightgray')
    offset_x = len(str(max(xmax, xmin))) * 2
    offset_y = len(str(max(ymax, ymin))) * 2
    for xtick in range(scale * xmin, scale * xmax + 1, tick):
        Screen().getcanvas().create_text(xtick * Screen().xscale + offset_x, -(scale * xmin - 2) *
                                         Screen().yscale, text=xtick, fill="black", anchor="se", angle=90, font=("Arial", 8, "normal"))
        Screen().update()
        goto(xtick, scale * ymin, draw=False)
        goto(xtick, scale * ymax, draw=True)

    for ytick in range(scale * ymin, scale * ymax + 1, tick):
        goto(scale * xmin, ytick - offset_y, draw=False)
        pencolor('black')
        write(ytick, align='right')
        pencolor('lightgray')
        goto(scale * xmin, ytick, draw=False)
        goto(scale * xmax, ytick, draw=True)
    Screen().update()
    goto(*old_pos, draw=False)
    pensize(old_pensize)
    color(*old_color)
    Screen().tracer(old_update_freq, old_delay)


if __name__ == '__main__':
    forward(10)
    pencolor(0.2, 0.8, 0.55)
    left(90)
    write('blaaa', True)
    forward(20)
    Screen().exitonclick()
