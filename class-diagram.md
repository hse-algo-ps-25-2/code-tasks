
```mermaid
---
title: Диаграмма классов решения
---
classDiagram
	DoublyLinkedList "1" *-- "*" DoublyListNode : композиция
    Queue "1" *-- "1" DoublyLinkedList : композиция
    
    class DoublyLinkedList{
	    +head
	    +tail
	    +int size
	    +append()
	    +insert()
	    +remove()
	    +index()
	    -__len__()
	    -__iter__()
	    -__reversed__()
	    -__str__()
    }
    
    class DoublyListNode{
        +value
        +DoublyListNode prev
        +DoublyListNode next
    }
    class Queue{
       +DoublyLinkedList list
       +enqueue()
       +dequeue()
       +peek()
       +is_empty()
       -__len__()
    } 

```

