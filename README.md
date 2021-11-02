# ABB_RWS_REST_API
ABB Robot Web Services through REST API

## Quick Start Guide

1. Turn the Robot On, and check that you are on the same subnet: `192.168.125.xxx`
2. Set the Flexpendant to **Manual Mode**, and Set motors to **ON**
3. Here is a small example:

```python
import RWSwrapper as RWS

rws = RWS()

# connect and activate LeadThrough:

if(rws.connect()):
    rws.activateLeadThrough("ROB_R") # ROB_L

print(rws.getLeadThroughStatus("ROB_R")) # ROB_L
```
To deactivate Lead Through Mode:

```python
import RWSwrapper as RWS

rws = RWS()
# deactivate LeadThrough Mode
rws.deactivateLeadThrough("ROB_R")
```

## Note:

The functionality in this code is non-exhaustive, to enhance it you can add any get/post functionalities from the [REST-API](https://developercenter.robotstudio.com/api/rwsApi/), if you find it ugly and difficult, you can take a look into a simpler version of the [REST-API-V2.0](https://developercenter.robotstudio.com/api/RWS).

I have implemented a (somehow) generalized simplified way to get and post, through the functions: [getResponse](RWSwrapper.py#L56) and [postResponse](RWSwrapper.py#L84), please fell free to use them to add any functionality that you want  from the **REST API**.