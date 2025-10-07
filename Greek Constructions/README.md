# Greek Constructions

I've done a lot of customization to the standard Manim engine in order to make coding these greek constructions much easier. Most of them fall into the following categories
- Standardization of style, e.g. `Animate` and `Unanimate` functions
- Automatic formatting of content, e.g. `self.write_proof_spec` and `self.write_footnotes` functions

The most complicated has to be the parameter `self.add_updaters` inside the `self.initialize_construction` function. I wanted the ability to permutate my greek constructions, wiggle points around, etc. Manim has a mechanism for this called `updaters`. This turns out to be extremely complicated, and there are a lot of steps in order to accomplish this.

First, in the functions `self.write_givens` and `self.write_solutions`, it's very important that everything is ultimately derived from the initial value trackers. No magic numbers allowed. 

Second, write a function `self._compute_construction` which computes the values of all mobjects in the greek construction (all variables returned by `self.write_givens` and `self.write_solutions` + some color formatting). 

This, In the function `self.add_updaters`, an updater is added to each mobject which recompute all construction variables (calls `self._compute_construction`) in order to determine its new value. I realize that this is extremely not efficient since this means every mobject on every frame is independently running `self._compute_construction`, but it'll take slightly inefficient for generality. 

We've done all this work, but there is still one fatal flaw. Animations such as `Create`, `GrowFromCenter`, etc, don't work on variables with updaters. Why? Because the updater overrides the animation. The solution to this is that I created my own `self.custom_play` function which is essentially just a wrapper around `self.play`. It works as follows
1. Given an `animation` object, copy the relevant mobject (different for different animations)
2. Clear the updater from the copied mobject
3. Run the animation on the copied mobject
4. Remove the resultant mobject and add the original mobject back into the scene

So finally we get the best of all worlds, I can use standard Manim syntax to write my animations and if I so choose can permute them if the proof necessitates.