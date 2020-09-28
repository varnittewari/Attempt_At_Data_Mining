#
#   A problem function which uses intentionally obtuse variable names and almost no comments.
#   The goal is for students to find the maximum of the function using gradient ascent,
#   axially-aligned grid search, full grid search, or some combination of these techniques.
#   CSCI-420 students who wish to try using Genetic Algorithms can try that too.
#
#   Dr. Thomas B. Kinsman
#
import math
import numpy as np

def urxyz( exes_parameter, why, zircon, rta, rtb, rtc ) :
    bogart  = np.array( [ exes_parameter, why, zircon ] )
    nu      = rta * (np.pi/180)
    delta   = np.array( [ [1, 0, 0], [0, np.cos(nu), -np.sin(nu)], [0, np.sin(nu), np.cos(nu)] ] )
    mu      = rtb * (np.pi/180);
    unicorn = np.array( [ [np.cos(mu), 0, np.sin(mu)], [0, 1, 0], [-np.sin(mu), 0, np.cos(mu)] ] )
    tu      = rtc * (np.pi/180);
    iocane  = np.array( [[np.cos(tu), -np.sin(tu), 0], [np.sin(tu), np.cos(tu), 0], [0, 0, 1]] )
    rq      = np.matmul( delta, np.matmul( unicorn, iocane ))
    Pegasus = np.matmul( rq, bogart )
    return Pegasus


def BirdbathFunc459( Harry, Dumbledore, Sirius ) :
    Snuffleupagus   = np.array( [ -204e-9, 20e-9, 427.854e-6, 999.87597e-3, 995.41971e-2  ] )
    Susan           = np.array( [  0.99254, -0.67955, -0.85840 ] )
    Ernie           = np.array( Harry )
    Bob             = np.array( [  0.12187,  0.70388, -0.50123 ] )
    Troll           = np.polyval( Snuffleupagus, Ernie )
    Hooper          = np.array( [  0.00436,  0.20682, -0.10926 ] )
    rot_tri         = urxyz( Susan, Bob, Hooper, Troll, Dumbledore, Sirius )
    if ( rot_tri[2][0] < rot_tri[2][1] ) :
         if ( rot_tri[2][0] < rot_tri[2][2] ) :
             min_idx = 0
         else :
             min_idx = 2
    else :
         if ( rot_tri[2][1] < rot_tri[2][2] ) :
             min_idx = 1
         else :
             min_idx = 2
    minic                   = rot_tri[2][min_idx]
    pradius                 = math.sqrt( 1 - (minic*minic) )
    Hagrid                  = 1 - abs(rot_tri[2][min_idx]) 
    Hedgewig                = ( math.pi * (Hagrid*Hagrid) / 3 ) * ( 3*1 - Hagrid )
    Hermoine                = 4/3 * math.pi
    Rous                    = Hedgewig / Hermoine 
    GiantVariable           = Rous * Rous * 2   # Increase the sensitivity by squaring small quantity.
    return GiantVariable

def convex_optimization():
    # Initialize our best fraction to 0. Any possible tilt will be better than this.
    best_fraction = 0

    # The roll, twist, and tilt must all be between -30 and 30
    min_value = -31
    max_value =  31

    # We start with our best value directly in the center of our max and min values
    # and our increment is the difference between the center and the ends of the 
    # search space. This way we cover the entire search space in the first iteration
    # checking the max, the min, and the center. We can hone in on the best value from
    # there.
    center = (min_value + max_value) / 2
    best_roll  = center
    best_twist = center
    best_tilt  = center
    increment  = max_value - center

    # We continually make the degree increments smaller and smaller
    # so every time we search a smaller and smaller portion of the
    # possible values as we narrow in on the best one.
    while increment > 0.00025:

        # We get the biggest and smallest values that define the 
        # ranges that we will be searching in this iteration. 
        # We get this range by taking the best value we've found
        # so far, and adding and subtracting our current increment 
        # value. If any of the max value is past our absolute max 
        # set it to the absolute max. If any of the min values is
        # past the absolute min, set it to the absolute min
        roll_min  = best_roll  - increment if best_roll  - increment >= min_value else min_value
        roll_max  = best_roll  + increment if best_roll  + increment <= max_value else max_value
        tilt_min  = best_tilt  - increment if best_tilt  - increment >= min_value else min_value
        tilt_max  = best_tilt  + increment if best_tilt  + increment <= max_value else max_value
        twist_min = best_twist - increment if best_twist - increment >= min_value else min_value
        twist_max = best_twist + increment if best_twist + increment <= max_value else max_value

        # The parameters we check are the best we've found so far, and
        # the max and min that we're checking in this search space
        tilts  = [tilt_min,  best_tilt,  tilt_max ]
        twists = [twist_min, best_twist, twist_max]
        rolls  = [roll_min,  best_roll,  roll_max ]
    
        # We check every combination of those values to find the one that
        # gives us the highest fraction. 
        for roll in rolls:
            for tilt in tilts:
                for twist in twists:
                    fraction = BirdbathFunc459(roll, tilt, twist)

                    # If this fraction is better than the previous best,
                    # save it as the new best, and save the paramaters
                    if fraction > best_fraction:
                        best_fraction = fraction
                        best_roll  = roll
                        best_tilt  = tilt
                        best_twist = twist
        
        # Then we shrink the increment by 15/16 and go again, with the new
        # best values we've found so far as the center of our search space
        increment = (increment * 15)/16

    print('\n Best Value found:')
    print('    Roll:\t', best_roll)
    print('    Tilt:\t', best_tilt)
    print('    Twist:\t', best_twist)
    print('    Fraction:\t', best_fraction)


if __name__ == '__main__' :


    #  Emit a trial test case here, etc...:
    print('\n\n\n')
    nn  = BirdbathFunc459( -31, 11.774184580272616, 8.526793561079431 )
    print('Fraction of Water = ', nn, '\t<-- Example test case results' )
    nn  = BirdbathFunc459( -26.735304997711946, 17.901837682497572, -10.325665449578272 )
    print('Fraction of Water = ', nn, '\t<-- Example test case results' )
    nn  = BirdbathFunc459( -34.323504434231815, -1.8566215272517583, 39.72819474238093 )
    print('Fraction of Water = ', nn, '\t<-- Example test case results' )
    nn  = BirdbathFunc459( -12, -1, 14 )
    print('Fraction of Water = ', nn, '\t<-- Example test case results' )



    print('###########################################################################################')
    print('Implementing the grid search to find the best values of roll, tilt and twist')
    convex_optimization()
