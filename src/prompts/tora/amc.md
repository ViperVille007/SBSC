Integrate step-by-step reasoning and Python code to solve math problems using the following guidelines:

- Analyze the question and write functions to solve the problem; the function should not take any arguments.
- Present the final result in LaTeX using a `\boxed{}` without any units.
- Utilize the `pi` symbol and `Rational`` from Sympy for $\pi$ and fractions, and simplify all fractions and square roots without converting them to decimal values.

Once you get the code output, just display the output answer within `\boxed{}` and terminate.
Here are some examples you may refer to:

Example Problem: Small lights are hung on a string $6$ inches apart in the order red, red, green, green, green, red, red, green, green, green, and so on continuing this pattern of $2$ red lights followed by $3$ green lights. How many feet separate the 3rd red light and the 21st red light? Note: $1$ foot is equal to $12$ inches.

Example Solution: 
Let's approach this step-by-step:
1. First, we need to understand the pattern of lights:
   - Every 5 lights (2 red + 3 green) complete one cycle of the pattern.
   - Each cycle is 30 inches long (5 lights * 6 inches).
2. We need to find how many complete cycles are between the 3rd and 21st red lights:
   - 3rd red light is at the end of the 2nd cycle (as each cycle has 2 red lights).
   - 21st red light is at the end of the 11th cycle (as 21 ÷ 2 = 10.5, rounded up to 11).
   - So there are 9 complete cycles between them (11 - 2 = 9).
3. Calculate the distance:
   - 9 cycles * 30 inches per cycle = 270 inches
   - Convert 270 inches to feet: 270 ÷ 12 = 22.5 feet

Here's the Python code to solve this:
```python
from sympy import Rational
def calculate_distance():
    lights_per_cycle = 5
    inches_per_light = 6
    inches_per_cycle = lights_per_cycle * inches_per_light
    start_cycle = 2  # 3rd red light is at the end of 2nd cycle
    end_cycle = 11   # 21st red light is at the end of 11th cycle
    cycles_between = end_cycle - start_cycle
    total_inches = cycles_between * inches_per_cycle
    total_feet = Rational(total_inches, 12)
    return f"\\boxed{{{total_feet}}}"
print(calculate_distance())
```
```output
\boxed{45/2}
```
The answer is \boxed{45/2}



Example Problem: A fruit salad consists of blueberries, raspberries, grapes, and cherries.  The fruit salad has a total of $280$ pieces of fruit.  There are twice as many raspberries as blueberries, three times as many grapes as cherries, and four times as many cherries as raspberries.  How many cherries are there in the fruit salad?

Example Solution:
Let's approach this problem step-by-step:
1. Let's define variables for each fruit:
   b = number of blueberries
   r = number of raspberries
   g = number of grapes
   c = number of cherries
2. We can set up equations based on the given information:
   r = 2b (twice as many raspberries as blueberries)
   g = 3c (three times as many grapes as cherries)
   c = 4r (four times as many cherries as raspberries)
3. We also know that the total number of fruits is 280:
   b + r + g + c = 280
4. Now, let's write a Python function to solve this system of equations:

```python
from sympy import symbols, Eq, solve
def solve_fruit_salad():
    b, r, g, c = symbols('b r g c')
    eq1 = Eq(r, 2*b)
    eq2 = Eq(g, 3*c)
    eq3 = Eq(c, 4*r)
    eq4 = Eq(b + r + g + c, 280)
    solution = solve((eq1, eq2, eq3, eq4))
    return f"\\boxed{{{solution[c]}}}"
print(solve_fruit_salad())
```
```output
\boxed{64}
```
The answer is \boxed{64}



Example Problem: Last summer $30\%$ of the birds living on Town Lake were geese, $25\%$ were swans, $10\%$ were herons, and $35\%$ were ducks. What percent of the birds that were not swans were geese?

Example Solution:
Let's approach this step-by-step:
1. First, we need to calculate the percentage of birds that were not swans.
2. Then, we'll calculate what percentage of this non-swan group were geese.

Here's the Python code to solve this:
```python
from sympy import Rational

def calculate_geese_percentage():
    # Total percentage of birds
    total = 100
    # Percentage of swans
    swans = 25
    # Percentage of non-swans
    non_swans = total - swans
    # Percentage of geese among all birds
    geese = 30
    # Calculate the percentage of geese among non-swans
    geese_among_non_swans = Rational(geese, non_swans) * 100
    # Simplify the fraction
    result = geese_among_non_swans.simplify()
    return f"\\boxed{{{result}}}"
print(calculate_geese_percentage())
```
```output
\boxed{40}
```
The answer is \boxed{40}



Example  Problem: At a twins and triplets convention, there were $9$ sets of twins and $6$ sets of triplets, all from different families. Each twin shook hands with all the twins except his/her siblings and with half the triplets. Each triplet shook hands with all the triplets except his/her siblings and with half the twins. How many handshakes took place?

Example Solution:
Let's approach this problem step-by-step:
1. Calculate the number of handshakes between twins
2. Calculate the number of handshakes between triplets
3. Calculate the number of handshakes between twins and triplets
4. Sum up all handshakes

Here's the Python code to solve this:
```python
from sympy import Rational
def calculate_handshakes():
    # Number of twins and triplets
    twins = 9 * 2
    triplets = 6 * 3
    # Handshakes between twins
    twin_handshakes = (twins * (twins - 2)) // 2  
    # Handshakes between triplets
    triplet_handshakes = (triplets * (triplets - 3)) // 2  
    # Handshakes between twins and triplets
    twin_triplet_handshakes = twins * triplets * Rational(1, 2)  
    # Total handshakes
    total_handshakes = twin_handshakes + triplet_handshakes + twin_triplet_handshakes
    return f"\\boxed{{{int(total_handshakes)}}}"
print(calculate_handshakes())
```
```output
\boxed{441}
```
The answer is \boxed{441}
