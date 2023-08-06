# ADK
 A Develop Kit, for easy coding.

## Develop Tools:
* **adk.TaskQue**, Task Queue with key-value mapping, priority, speed limit, timeout and callbacks.
* **adk.PriQue**, Priority Queue with mutex lock and speed limit.
* **adk.PriDict**, Priority Dict with mutex lock and speed limit.

## Data types:
### Priority containers
extension of heap, main methods are: push, pop, peek
* **adk.PriorityQueue**, Priority Queue, push(data, priority) 
* **adk.SimplePriorityQueue**, Priority Queue, push(priority) 
* **adk.PriorityDict**, Priority Dict, push(key, data, priority)
* **adk.SimplePriorityDict**, Priority Dict, push(key, priority)
