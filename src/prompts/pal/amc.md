Let's use python program to solve math problems.
DO NOT USE ANY TEXTUAL REASONING.
Your response must start with: ```python 
Your response must end with: print(result)

Here are some examples you may refer to.

Example Problem: Small lights are hung on a string $6$ inches apart in the order red, red, green, green, green, red, red, green, green, green, and so on continuing this pattern of $2$ red lights followed by $3$ green lights. How many feet separate the 3rd red light and the 21st red light? Note: $1$ foot is equal to $12$ inches.

Example Solution: 

```python
def solution():
    # Find position of 3rd red light
    n_3rd = 3
    complete_cycles_3rd = (n_3rd - 1) // 2
    remaining_lights_3rd = (n_3rd - 1) % 2
    pos_3rd = complete_cycles_3rd * 5 * 6 + remaining_lights_3rd * 6
    # Find position of 21st red light
    n_21st = 21
    complete_cycles_21st = (n_21st - 1) // 2
    remaining_lights_21st = (n_21st - 1) % 2
    pos_21st = complete_cycles_21st * 5 * 6 + remaining_lights_21st * 6
    # Calculate the distance in inches
    distance_inches = pos_21st - pos_3rd
    # Convert to feet
    distance_feet = distance_inches / 12
    return distance_feet
result = solution()
print(result)
```



Example Problem: A fruit salad consists of blueberries, raspberries, grapes, and cherries.  The fruit salad has a total of $280$ pieces of fruit.  There are twice as many raspberries as blueberries, three times as many grapes as cherries, and four times as many cherries as raspberries.  How many cherries are there in the fruit salad?

Example Solution:

```python
from sympy import symbols, Eq, solve
def solution():
    # Define the symbols for the variables
    b, r, g, c = symbols('b r g c')
    # Define the equations based on the problem statement
    eq1 = Eq(r, 2*b)           
    eq2 = Eq(g, 3*c)           
    eq3 = Eq(c, 4*r)           
    eq4 = Eq(b + r + g + c, 280)  
    # Solve the system of equations
    sol = solve((eq1, eq2, eq3, eq4))
    return sol[c]
result = solution()  
print(result)        

```



Example Problem: Last summer $30\%$ of the birds living on Town Lake were geese, $25\%$ were swans, $10\%$ were herons, and $35\%$ were ducks. What percent of the birds that were not swans were geese?

Example Solution:

```python
def solution():
    # Total percentage of all birds
    total = 100
    # Percentages of each bird type
    geese = 30
    swans = 25
    herons = 10
    ducks = 35
    # Calculate percentage of birds that are not swans
    not_swans = total - swans
    # Calculate percentage of geese among birds that are not swans
    geese_among_not_swans = (geese / not_swans) * 100
    # Round to nearest whole number
    return round(geese_among_not_swans)
result = solution()
print(result)
```



Example  Problem: At a twins and triplets convention, there were $9$ sets of twins and $6$ sets of triplets, all from different families. Each twin shook hands with all the twins except his/her siblings and with half the triplets. Each triplet shook hands with all the triplets except his/her siblings and with half the twins. How many handshakes took place?

Example Solution:

```python
def solution():
    # Number of twins and triplets
    twins = 9 * 2
    triplets = 6 * 3
    # Handshakes between twins
    twin_handshakes = (twins * (twins - 2)) // 2
    # Handshakes between triplets
    triplet_handshakes = (triplets * (triplets - 3)) // 2
    # Handshakes between twins and triplets
    twin_triplet_handshakes = (twins * triplets) // 2
    # Total handshakes
    total_handshakes = twin_handshakes + triplet_handshakes + twin_triplet_handshakes
    return total_handshakes
result = solution()
print(result)
```