from manim import *
from numpy import sin, cos, sign, sum
from random import random

# config.background_color = WHITE
# manim -pql -s result.py

class Result(Scene):
    caption = None
    animations_queue = []

    def construct(self):
        headerT = UP*3.2
        content_y = -0.5
        text_pos = (0,content_y,0) + LEFT*4
        embed_pos = (0,content_y,0) + RIGHT*4

        textH = Text('TEXT').move_to(headerT+LEFT*4)
        embedH = Text('EMBEDDING').move_to(headerT+RIGHT*4)
        divider = Line((1, 0, 0), (23, 0, 0)).set_opacity(0.5).next_to(textH, DOWN, buff=0.2)
        self.add(textH, embedH, divider)

        mtitle = Text('Despicable Me').move_to(text_pos)
        mtitlebox = Rectangle(height=1, width=5.5, color=WHITE).move_to(mtitle)
        mplot = Text('''
        When a criminal mastermind \n
        uses a trio of orphan girls \n
        as pawns for a grand scheme, \n
        he finds their love is profoundly \n
        changing him for the better.
        ''', line_spacing=0.01)
        mplot.scale(0.4).next_to(mtitlebox, DOWN)
        mplotbox = Rectangle(height=2.35, width=5.5, color=WHITE).next_to(mtitlebox, DOWN, buff=0)
        text = VGroup(mtitle, mtitlebox, mplot, mplotbox).move_to(text_pos)


        self.add(mtitle, mtitlebox, mplot, mplotbox)

        embedding = Matrix(
            [[round(random()/10, 4)] for x in range(10)]+['…']
        )
        embedding.set_row_colors(YELLOW,YELLOW,YELLOW,YELLOW,YELLOW,YELLOW,YELLOW,YELLOW,YELLOW,YELLOW).scale(0.5)
        embedding.move_to(embed_pos)

        encodeArrow = CurvedArrow(start_point=mplotbox.get_right()+(0.3,0,0), end_point=embedding.get_left()-(0.3,0,0))
        arrowCaption = Text('ENCODE').scale(0.5).next_to(encodeArrow, DOWN)
        self.add(encodeArrow, arrowCaption)

        self.add(embedding)

        self.wait(5)

    def describe(self, text, enqueue=True):
        '''
        Display/Update bottom caption.
        '''
        caption_pos = DOWN*2.9
        text.move_to(caption_pos)
        text.scale(0.4)
        if self.caption == None:
            self.play(Write(text), run_time=0.4, enqueue=enqueue)
        else:
            self.play(ReplacementTransform(self.caption, text), enqueue=enqueue)
        self.caption = text  # ReplacementTransform needs a reference to the previous object!

    def play(self, *args, enqueue=False, subcaption=None, subcaption_duration=None, subcaption_offset=0, **kwargs):
        '''
        A wrapper for Manim's `play`, to be able to enqueue a bunch of animations
        and wait until buffer is flushed for them to play all together.
        '''
        self.animations_queue += args

        if not enqueue:
            super().play(*self.animations_queue, subcaption=subcaption, subcaption_duration=subcaption_duration, subcaption_offset=subcaption_offset, **kwargs)
            self.animations_queue = []