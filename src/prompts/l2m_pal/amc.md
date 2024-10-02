Let's use python program to solve math problem using sub-questions in seqential order.
DO NOT USE ANY TEXTUAL REASONING.
Your response must start with: ```python 
Your response must end with: print(result)

Once you get the code output, just display the output answer within `\boxed{}` and terminate.
Here are some examples you may refer to.

Example 1:

Problem: Small lights are hung on a string $6$ inches apart in the order red, red, green, green, green, red, red, green, green, green, and so on continuing this pattern of $2$ red lights followed by $3$ green lights. How many feet separate the 3rd red light and the 21st red light? Note: $1$ foot is equal to $12$ inches.

Breakdown: 
1. How many lights are there in each complete cycle of the pattern?
2. If we know the cycle length how do we find the positions of the 3rd red light and the 21st red light in the sequence?
3. If we know the positions of 3rd red light and 21st red light how do we find number of lights between them ?
4. What is the total distance in inches between the 3rd red light and the 21st red light?
5. How many feet does the distance between the 3rd and 21st red lights convert to, given that 1 foot equals 12 inches?

Solution: 

```python
def solution():
    # How many lights are there in each complete cycle of the pattern?
    red_lights_in_one_cycle = 2
    green_lights_in_one_cycle = 3
    cycle_length = red_lights_in_one_cycle + green_lights_in_one_cycle

    # If we know the cycle length how do we find the positions of the 3rd red light and the 21st red light in the sequence?
    def position_of_nth_red_light(n):
        complete_cycles = (n - 1) // 2
        position = complete_cycles * cycle_length + (n - 1) % 2 + 1
        return position

    position_3rd_red = position_of_nth_red_light(3)
    position_21st_red = position_of_nth_red_light(21)

    # If we know the positions of 3rd red light and 21st red light how do we find number of lights between them ?
    number_of_lights_between = position_21st_red - position_3rd_red

    # What is the total distance in inches between the 3rd red light and the 21st red light?
    distance_in_inches = number_of_lights_between * 6  # 6 inches apart

    # How many feet does the distance between the 3rd and 21st red lights convert to, given that 1 foot equals 12 inches?
    distance_in_feet = distance_in_inches / 12  # 12 inches per foot

    return distance_in_feet

# Get the result and print it
result = solution()
print(result)
```
```output
\boxed{45/2}
```
The answer is \boxed{45/2}

Example 2:
Problem: A fruit salad consists of blueberries, raspberries, grapes, and cherries.  The fruit salad has a total of $280$ pieces of fruit.  There are twice as many raspberries as blueberries, three times as many grapes as cherries, and four times as many cherries as raspberries.  How many cherries are there in the fruit salad?

Breakdown:
1. How can we set up an equation using the given relations between number of fruits and the total number of pieces of fruit, which is 280 ?
2. How can we simplify the equation using the relationships between the different types of fruit to solve for one variable?
3. Once the equation is simplified to one variable, how can we solve for the number of cherries?

Solution:

```python
from sympy import symbols, Eq, solve

def solution():
    # How can we set up an equation using the given relations between number of fruits and the total number of pieces of fruit, which is 280 ?

    b, r, g, c = symbols('b r g c')  # blueberries, raspberries, grapes, cherries
    raspberries_eq = Eq(r, 2 * b)
    grapes_eq = Eq(g, 3 * c)
    cherries_eq = Eq(c, r * 4)
    total_fruit_eq = Eq(b + r + g + c, 280)

    # How can we simplify the equation using the relationships between the different types of fruit to solve for one variable?
    total_fruit_simplified = total_fruit_eq.subs({
        r: 2 * b,  # from raspberries_eq
        g: 3 * c,  # from grapes_eq
        c: r * 4   # from cherries_eq
    })

    #Once the equation is simplified to one variable, how can we solve for the number of cherries?
    cherries_in_raspberries = cherries_eq.subs(r, 2 * b)
    c_in_terms_of_b = solve(cherries_in_raspberries, c)[0]
    total_fruit_final = total_fruit_simplified.subs(c, c_in_terms_of_b)
    b_value = solve(total_fruit_final, b)[0]
    c_value = c_in_terms_of_b.subs(b, b_value)
    result = c_value

    return result

result = solution()
print(result)
```
```output
\boxed{64}
```
The answer is \boxed{64}


Example 3:
Problem: Last summer $30\%$ of the birds living on Town Lake were geese, $25\%$ were swans, $10\%$ were herons, and $35\%$ were ducks. What percent of the birds that were not swans were geese?

Breakdown:
1. What percentage of the birds were not swans?
2. Given the percentage of birds that are not swans, what percentage of these non-swan birds were geese?

Solution:
```python
def solution():
    # What percentage of the birds were not swans?
    total_percentage = 100  
    swans_percentage = 25   
    non_swans_percentage = total_percentage - swans_percentage  

    # Given the percentage of birds that are not swans, what percentage of these non-swan birds were geese?
    geese_percentage = 30  
    geese_of_non_swans = (geese_percentage / non_swans_percentage) * 100
    return geese_of_non_swans

result = solution()
print(result)
```
```output
\boxed{40}
```
The answer is \boxed{40}

Example 4:
Problem: At a twins and triplets convention, there were $9$ sets of twins and $6$ sets of triplets, all from different families. Each twin shook hands with all the twins except his/her siblings and with half the triplets. Each triplet shook hands with all the triplets except his/her siblings and with half the twins. How many handshakes took place?

Breakdown:
1. How to get the total number of triplets and twins?
2. What is the total number of handshakes among all twins?
3. How many triplets does each twin shake hands with, given that they shake hands with half of them?
4. What is the total number of handshakes among all triplets?
5. What is the total number of handshakes that occur at the convention when combining all the above scenarios?

Solution:
```python
def solution():
    # How to get the total number of triplets and twins?
    num_twins = 9 * 2  
    num_triplets = 6 * 3  

    # What is the total number of handshakes among all twins?
    # Each twin shakes hands with all other twins except their sibling
    handshakes_among_twins_per_twin = num_twins - 2
    total_handshakes_among_twins = (handshakes_among_twins_per_twin * num_twins) // 2

    # How many triplets does each twin shake hands with, given that they shake hands with half of them?
    handshakes_between_twins_and_triplets_per_twin = num_triplets // 2
    total_handshakes_between_twins_and_triplets = handshakes_between_twins_and_triplets_per_twin * num_twins

    # What is the total number of handshakes among all triplets?
    handshakes_among_triplets_per_triplet = num_triplets - 3
    total_handshakes_among_triplets = (handshakes_among_triplets_per_triplet * num_triplets) // 2

    # What is the total number of handshakes that occur at the convention when combining all the above scenarios?
    total_handshakes = total_handshakes_among_twins + total_handshakes_between_twins_and_triplets + total_handshakes_among_triplets

    return total_handshakes

result = solution()
print(result)
```
```output
\boxed{441}
```
The answer is \boxed{441}