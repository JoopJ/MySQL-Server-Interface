# Event Doc
Developer information about specific events handled by the EventSystem class.

*Name:* **EXAMPLE_EVENT** 
*Description:* What triggers the event
**args: (if any)*
```
arg_name: data_type,
example_arg: Dict[str, List[int]],
example_arg2: int
```

---

*Name:* **OPEN_WINDOW** 
*Description:* When a specific window needs to be opened.
**args:*
```
window_name: str
```

*Name:* **CLOSE_WINDOW** 
*Description:* When a specific window needs to be closed.
**args:*
```
window_name: str
```

*Name:* **QUIT** 
*Description:* Quit button pressed in MainWindow

*Name:* **CONNECT_TO_SERVER**
*Description:* 'Connect' button pressed in NewConnectionWindow.
**args:*
```
host: str
user: str
password: str
```

*Name:* **USE_DATABASE** 
*Description:* Use button pressed in ServerWindow, with database name selected.
**args:*
```
database_name: str
```