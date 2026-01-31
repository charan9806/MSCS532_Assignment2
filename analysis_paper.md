
# Analysis of Sorting Algorithms: Quick Sort and Merge Sort

## Introduction
Divide-and-conquer is a widespread strategy for designing algorithms. The basic idea is to break a big, complicated problem into smaller pieces, solve those pieces individually, and then combine the answers. This is popular because it usually saves a lot of work as the input gets bigger.

For this assignment, I looked at two classic sorting algorithms that use this method: Quick Sort and Merge Sort. The goal was to build them both and see how they compare. I wanted to understand not just the math behind their speed (the time complexity), but also how they actually perform when you run them on real data.

## Quick Sort

### How it Works
Quick Sort works by "partitioning" a list. You pick one number to be the "pivot," and then you rearrange the list so that everything smaller than the pivot goes to the left, and everything larger goes to the right. This splits the problem into two smaller lists. You keep doing this recursively until the whole thing is sorted.

Even though the logic is simple, the speed depends a lot on that pivot. If you pick a bad pivot, the splits are uneven. To stop that from happening, I used a random pivot in my code.

### Time Complexity (The Math)
Quick Sort's speed changes based on how lucky we are with the pivot:
*   **Best Case:** If the pivot splits the list right down the middle every time, the recursion isn't too deep. The time complexity here is Θ(n log n).
*   **Average Case:** Since I'm picking pivots randomly, we usually get a pretty balanced split. So, on average, it's also Θ(n log n).
*   **Worst Case:** If we get really unlucky and the pivot is always the smallest or largest number, the split is terrible. The list doesn't get cut in half; it just shrinks by one. This makes the algorithm slow, taking Θ(n²) time.

Formal notation here requires some nuance. Strictly speaking, Quick Sort is $O(n^2)$ (upper bound) and $\Omega(n \log n)$ (lower bound). Because the runtime varies so heavily based on the input order, we can't always slap a single $\Theta$ bound on it without context. However, since the random pivot essentially eliminates the worst-case scenario in practice, the industry standard is to treat it as $\Theta(n \log n)$ on average.

### Recurrence Relation
If the split is balanced, the math looks like this: $T(n) = 2T(n/2) + cn$.
If the split is worst-case, it looks like this: $T(n) = T(n-1) + cn$.

To rigorously prove the average-case bound, I used the **Substitution Method**. Starting with the hypothesis that $T(n) = O(n \log n)$, I assumed that for some constant $c$, $T(k) \le c k \log k$ holds for all $k < n$. Substituting this into our recurrence $T(n) = 2T(n/2) + n$:

$$T(n) \le 2(c(n/2)\log(n/2)) + n$$
$$T(n) \le cn(\log n - \log 2) + n$$
$$T(n) \le cn \log n - cn + n$$

This simplifies to $T(n) \le cn \log n - (cn - n)$. As long as we choose a constant $c \ge 1$, the residual term is negative, proving that the algorithm is indeed bounded by $O(n \log n)$.

### Real World Performance
Even though the "worst case" sounds scary, Quick Sort is usually the fastest option in real life. It doesn't need much extra memory, and it works well with how computers handle memory (caching). Because I used random pivots, the chance of hitting that slow worst-case scenario is extremely low.

## Merge Sort

### How it Works
Merge Sort is a bit more rigid. It doesn't care about the values in the list when dividing. It just cuts the list into two equal halves over and over until you have lists of just one number. Then, the real work happens in the "merge" step, where it puts those pieces back together in the correct order.

### Time Complexity (The Math)
Because Merge Sort always cuts the list in half perfectly, its speed is very predictable. It doesn't matter if the list is random, sorted, or backwards.
*   **Best, Average, and Worst Case:** It's always Θ(n log n).

Unlike Quick Sort, Merge Sort is incredibly stable. Because it performs the exact same splits and merges regardless of the data ordering, its Best Case ($\Omega$), Worst Case ($O$), and Tight Bound ($\Theta$) are identical. It is $\Theta(n \log n)$ across the board.

### Recurrence Relation
The math for Merge Sort is always: $T(n) = 2T(n/2) + cn$.

**Solving with the Master Method**
To solve this formally, I applied the Master Theorem. Here, we have $a = 2$ subproblems and a division factor of $b = 2$. Comparing the recurrence term $n^{\log_b a}$ (which simplifies to $n^1$) with the driving function $f(n) = cn$, we see they grow at the same rate. This puts us squarely in **Case 2** of the Master Theorem. Consequently, we multiply by a logarithmic factor, confirming that $T(n) = \Theta(n \log n)$.

**Solving with the Recursion Tree Method**
Visualizing the algorithm as a tree makes the cost analyzing intuitive:
*   At the top level (Level 0), the cost is simply $cn$.
*   At Level 1, the problem splits into two nodes of size $n/2$, which sum up to $cn$ again ($2 \times cn/2$).
*   In fact, at any given depth $i$, the total work across all $2^i$ nodes remains constant at $cn$.
*   Since the tree divides repeatedly until the problem size is 1, the total height is $\log_2 n$.

Summing the constant work $cn$ across all $\log_2 n$ levels yields a total complexity of $\Theta(n \log n)$.

### Real World Performance
The best thing about Merge Sort is that you know exactly how long it will take. It's consistent. The downside is memory. You need extra space (auxiliary arrays) to hold the numbers while merging them. This can be a problem if you are working with huge amounts of data and don't have much RAM.

## My Experiments

### Setup
I wrote both algorithms in Python. To test them out, I created three different types of lists:
1.  Already sorted numbers.
2.  Reverse sorted numbers.
3.  Random numbers.

I timed how long they took to run and checked how much memory they used. I ran the tests multiple times and took the average to make sure the results were accurate.

### Results
The results pretty much matched what the theory predicted. Merge Sort was very steady. It took about the same amount of time no matter what the input looked like, but it definitely used more memory because of the merging process.
Quick Sort was generally faster than Merge Sort on the random data. It used less memory, which helps it run faster on the computer hardware. However, its speed varied a bit more from run to run because of the random pivots. Even with that variation, it never hit the slow "worst-case" scenario in my tests.

The only differences between my numbers and the theoretical math probably come from Python itself—things like the cost of recursion and how Python handles memory allocation aren't included in the simple Big-O math.

## Conclusion
This project showed me the main trade-offs between these two algorithms. Merge Sort is the "safe" bet—it's predictable and handles worst-case scenarios well, but it eats up memory. Quick Sort is the "risky but fast" option—it's great for average use and saves memory, but you have to be careful about the pivot implementation. Choosing the right one really just depends on whether you care more about raw speed or guaranteed consistency.

## References
*   Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
*   Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
