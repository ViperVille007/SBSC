**Question (AIME 2022):** Ellina has twelve blocks, two each of red (\textbf{R}), blue (\textbf{B}), yellow (\textbf{Y}), green (\textbf{G}), orange (\textbf{O}), and purple (\textbf{P}). 
Call an arrangement of blocks \textit{even} if there is an even number of blocks between each pair of blocks of the same color. 
For example, the arrangement \[\textbf{R B B Y G G Y R O P P O}\] is even. Ellina arranges her blocks in a row in random order. 
The probability that her arrangement is even is \frac{m}{n}, where m and n are relatively prime positive integers. Find m+n. 


Let's approach this problem step by step using combinatorics and probability theory.

### Step 1: Import necessary libraries and calculate total arrangements
```python
from sympy import symbols, factorial
# Calculate total number of arrangements
total_arrangements = factorial(12) // (factorial(2) ** 6)
print(f"Total number of arrangements: {total_arrangements}")
```
```output
Total number of arrangements: 7484400
```

Let's continue with the next steps to solve this problem.
### Step 2: Calculate the number of even arrangements
```python
from sympy import symbols, factorial
# Total number of arrangements
total_arrangements = factorial(12) // (factorial(2) ** 6)
# Calculate number of even arrangements
# For an even arrangement, we need to choose 6 even positions for the first block of each color
even_positions = 6
odd_positions = 6
even_arrangements = factorial(even_positions) * factorial(odd_positions)
print(f"Number of even arrangements: {even_arrangements}")
```
```output
Number of even arrangements: 518400
```

Let's continue with the next steps to solve this problem.
### Step 3: Calculate the probability and simplify the fraction
```python
from sympy import symbols, factorial, Rational, gcd
# Total number of arrangements
total_arrangements = factorial(12) // (factorial(2) ** 6)
# Number of even arrangements
even_positions = 6
odd_positions = 6
even_arrangements = factorial(even_positions) * factorial(odd_positions)
# Calculate probability
probability = Rational(even_arrangements, total_arrangements)
# Simplify the fraction
m, n = probability.as_numer_denom()
print(f"Probability: {probability}")
print(f"m = {m}, n = {n}")
```
```output
Probability: 16/231
m = 16, n = 231
```

Let's continue with the final step to solve this problem.
### Step 4: Calculate m + n
```python
from sympy import symbols, factorial, Rational, gcd
# Reuse the values from the previous step
m, n = 16, 231
# Calculate m + n
result = m + n
print(f"m + n = {result}")
```
```output
m + n = 247
```

### END OF CODE
The final answer is \boxed{247}
