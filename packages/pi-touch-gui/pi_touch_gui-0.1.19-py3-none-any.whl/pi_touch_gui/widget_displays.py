# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Displays are decorative or informative widgets that are not interactive,
    but provide feedback state via a function.
"""
import logging

import pygame
from custom_inherit import doc_inherit

from pi_touch_gui._widget_bases import IWidget

LOG = logging.getLogger(__name__)


class Label(IWidget):
    """ Text Label with a fixed color and no state function.
    """

    def __init__(self, position, size,
                 font_size=None,
                 label=None,
                 label_color1=None):
        """ Initialize the label with a subset of the Widget parameters.

        Parameters
        ----------
        position : Tuple[int, int]
            The (x, y) top-left corner of the Label. The screen positioning
            is accounted at (0, 0) being the far top-left, increasing down
            and to the right.
        size : Tuple[int, int]
            The (w, h) of the Label's rectangular extent.
        font_size : int
            Height of the font in pixels.  If not specified, defaults to
            the Label height (size[1])
        label : str
        label_color1 : Union[Tuple[int, int, int], Tuple[int, int, int, int]]
            Color of the Label
        """
        font_size = size[1] if font_size is None else font_size
        super(Label, self).__init__(position, size,
                                    font_size=font_size,
                                    label=label,
                                    label_color1=label_color1,
                                    label_color2=label_color1)

    def render(self, surface):
        color, label_color = self.state_colors()

        self.render_centered_text(surface, self.label, label_color)

    def can_focus(self):
        return False


class Light(IWidget):
    """ Lights are circles whose color state is determined by their function.
    """

    def __init__(self, position, size, function):
        """ Initialize the light with a subset of the Widget parameters.

        Parameters
        ----------
        position : Tuple[int, int]
            The (x, y) top-left corner of the light. The screen positioning
            is accounted at (0, 0) being the far top-left, increasing down
            and to the right.
        size : Tuple[int, int]
            The (w, h) of the Light's rectangular extent.  The diameter of
            the circle is given by the minimum of w,y.
        function : Callable[[Light], [Color, Color]]
            The function returns the (ring, fill) colors
        """
        # The parent init sets convenience properties like self.x, etc
        super(Light, self).__init__(position, size)

        self.function = function
        self.radius = min(size[0], size[1]) >> 1
        self.center = (self.x + self.w // 2), (self.y + self.h // 2)

    def render(self, surface):
        if self.function is None:
            color1 = self.color1
            color2 = self.color2
        else:
            color1, color2 = self.function(self)
        # Fill
        pygame.draw.circle(surface, color2, self.center, self.radius, 0)
        # Outline ring
        pygame.draw.circle(surface, color1, self.center, self.radius, 2)

    def can_focus(self):
        return False


class Indicator(IWidget):
    """ Indicators are dynamic Labels, controlled by their function.
    """

    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 function=None,
                 **kwargs):
        """ Initialize the Indicator.

        If color1 is None, the indicator is colored like a label, with only
        the label colors being used.

        If color1 is specified, then the indicator is set in a filled
        rectangle with the active/inactive color.

        Parameters
        ----------
        function : Callable[[Indicator], [bool, str]]
            The function that defines the content and state of the indicator.
            The bool is an 'active' flag, which sets the active color
            palette if True.  The string sets the indicator label.  If it is
            None, then the indicator defaults to self.label.
        """
        # Set up the boxing behavior and font size.
        kw_font_size = kwargs.pop('font_size', None)
        if kwargs.get('color1') is None:
            self.box = False
            font_size = size[1] if kw_font_size is None else kw_font_size
        else:
            self.box = True
            font_size = (size[1] >> 1) if kw_font_size is None else kw_font_size
        self.function = function

        super(Indicator, self).__init__(position, size,
                                        font_size=font_size,
                                        **kwargs)

    def render(self, surface):
        if self.function:
            active, label = self.function(self)
        else:
            active, label = False, None
        # Default to the internal label
        label = self.label if label is None else label

        color, label_color = self.state_colors(active=active)

        if self.box:
            pygame.draw.rect(surface, color, (self.position, self.size), 0)

        self.render_centered_text(surface, label, label_color)

    def can_focus(self):
        return False
