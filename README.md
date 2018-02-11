# steel_optimisation-problem

Solving the Bin Optimisation problem.
Say you have a number of steel tubes that need to be cut in the most efficient way possible to make up an arbitrary amount of cut-to-length
pieces, if you know the cut lengths, how do you know how many tubes of a fixed length to buy to then cut up?

Essentially what you have is a number of 'containers' problem where you try to fit the most volume (length in our case) into the least amount of 
'containers' of a fixed size.

For example say you have to cut 3x500mm pipes and 2x600mm pipes but can only buy pipes in lengths of 2000mm. 

You can fill up 1500mm of one pipe with your 3x500mm pipes but then you have a wasted 500mm pipe.

This is the kind of optimization I was trying to do for a spaceframe chassis for a formula student car see: https://goo.gl/uWqBZN

Turns out this is a hard problem to solve.

Wiki link: https://en.wikipedia.org/wiki/Bin_packing_problem

Some other resource: https://d-nb.info/993873529/34
