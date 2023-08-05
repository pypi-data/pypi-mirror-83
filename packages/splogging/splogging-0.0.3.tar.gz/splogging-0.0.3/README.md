# splogging

Ever had that feeling like quickly wanting to activate logging for your script, 
but were slightly overwhelmed by the plethora of settings and commands,
so you are now running with no logging at all?

Enter splogging!
 
Just run *pip install*, 
do a *from ... import ...* and finally 
initialise your logger with *my_logger=logger.setup_logging()*.

That's all it takes to get your logging up and running.

Of course, you can customise your new logger with the parameters shown below.

Happy logging! 

## Install splogging

```shell
$ pip install splogging 
```

## Use splogging

### Create one logger
Use this "one logger" setup, if you want same config for output to screen (terminal) and log file.

```python
from splogging import logger

if __name__ == "__main__":
    logger = logger.setup_logging(
        filename="my.log", when="W0", file_level="info", console_level="info",
    )

    logger.info("Log message to console and in file.")
```

### Create multiple loggers
Use this "multiple logger" setup, if you want to configure (and use) multiple loggers separately.

Specify a unique name for each logger.

```python
from splogging import logger

if __name__ == "__main__":
    logger_file = logger.setup_logging(
        name="A",
        filename="steven.log",
        when="W0",
        file_level="info",
        console_level=None,
    )
    logger_console = logger.setup_logging(
        name="B",
        filename="steven.log",
        when="W0",
        file_level=None,
        console_level="info",
    )

    logger_file.warning("In File!")
    logger_console.warning("In console!!!")
``` 

# Parameters
- **name**
<br/>Can be left empty.
<br/>Useful only when creating multiple, separate loggers.
- **filename**
<br/>Path and name of logfile.
- **when**
<br/>Defines when to rotate the log file.
<br/>Check [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html?highlight=logging#timedrotatingfilehandler) for more info.
- **backup_count**
<br/>Number of backups to keep (set to 0 to keep all rotated logs).
- **file_level**
<br/> Save log messages that have this or a higher level.
<br/>Set to None to disable logging to file.
- **file_format**
<br/>Format of message saved to file.
<br/>Check docs.python.org for more info.
- **file_log_datefmt**
<br/>Format of timestamp in the log message, saved to file.
<br/>See [strftime](https://docs.python.org/3/library/time.html#time.strftime) for details.
- **console_level**
<br/>Display log messages that have this or a higher level.
<br/>Set to None to disable logging to console.
- **console_format**
<br/>Format of message, displayed in the console.
<br/>Check [Formatter Objects](https://docs.python.org/3/library/logging.html#formatter-objects) for more info.
- **console_log_datefmt**
<br/>Format of timestamp in the message, displayed in the console.

