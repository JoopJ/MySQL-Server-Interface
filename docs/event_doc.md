# Event Doc
Developer information about specific events handled by the EventSystem class.


*Name:* **EXAMPLE_EVENT** 
*Description:* What triggers the event
**args: (if any):*
```
arg_name: data_type,
example_arg: Dict[str, List[int]],
example_arg2: int
```
---
### NewConnectionWindow

*Name:* **CONNECT_BTN**
*Description:* 'Connect' button pressed, to connect to a MySQL server.
**args:*
```
host: str
user: str
password: str
```