# Lazy computing

Based on haskell features, exemples are worth a 1000 words



## Usage

```python
from lazy_computing import *
```



```python
for x in infinity: print(x)                         # 1 2 3 4 5 ...

for x in remove(100, infinity): print(x)            # 100 101 102 103 ...
    
for x in take(5, remove(100, infinity)): print(x)   # 100 101 102 103 104
    
for x in arithm(1, 5, ...): print(x)                # 1 5 9 13 17 ...
    
for x in arithm(1, 5, ..., 17): print(x)            # 1 5 9 13
    
for x in geom(1, 5, ...): print(x)                  # 1 5 25 125 625 ...
    
for x in geom(1, 5, ..., 500): print(x)             # 1 5 25 125 625 ...
    
for x in tail([5, 6, 7, 8]): print(x)               # 6 7 8

print(head([5, 6, 7, 8]))                           # 5
print(extract(2, [5, 6, 7, 8]))                     # 7
    

```



## Documentation



* infinity: iterable representing the infinity
* remove(number, iterable): return an iterator without the _number_ first element
* extract(index, iterable): return the value at _index_ from iterable
* take(limit, iterable): return an iterator taking _limit_ first value from iterable
* head(iterable): return the first value of an iterable
* tail(iterable): return an iterator on an iterable, without the head
* arithm(*args): return an iterable. It guess the step from the arguments
* geom(*args): return an iterable: It guess the factor from the arguments