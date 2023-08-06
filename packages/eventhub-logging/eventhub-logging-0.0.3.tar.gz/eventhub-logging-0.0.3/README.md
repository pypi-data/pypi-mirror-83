# Introduction 
We developped this package for sending logging message to Azure EventHub system.

# Installation

```shell script
pip install eventhub-logging
```

# Usage
## Requirements
azure-eventhub version: 5.2.0 or higher

## Examples
```python
import logging
from logging_handler.eventhub_handler import EventHubHandler

logger = logging.getLogger(__name__)

logger.addHandler(EventHubHandler(
    endpoint="your eventhubs endpoint",
    access_keyname="your azure event hub access keyname",
    access_key="your access key value",
    entity_path="your event hub",
    partition_key="sth to partition"
))
logger.info("Send my first logging message ")
```


# Contribute
[Javariel](zxie@opnf.fr)