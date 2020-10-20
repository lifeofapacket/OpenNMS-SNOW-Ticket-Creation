# OpenNMS ServiceNOW Ticket Creation with REST API
The script is created to document the proof of concept of using the REST API to create tickets from events of the OpenNMS.

In our test environment, we have generated 4 different events to see if we can generate tickets through ServiceNOW REST API.

[![events.png](https://i.postimg.cc/tJ4wngzg/events.png)](https://postimg.cc/ZBXV142k)

In our python script, we communicated with OpenNMS with their REST API as well for every 10 seconds. The check time can be changed as needed. We can also see the current Alarm lists but in this test, we have only used current events for minimal settings.  

In first part of our script, we comminate with OpenNMS through REST link with http basic authentication. If our commination succeeds, we will continue with else statement. 

In our else statement, we have ticket check where we check the tickets if they have created already on ServiceNOW. If the ticket is existing – the script won’t create a ticket for that event ID with the particular IP address.

[![log.png](https://i.postimg.cc/x8p7vSs3/log.png)](https://postimg.cc/H85BmF1r)

If the ticket doesn’t exist, the ticket will be generated through ServiceNOW as seen below. 

[![log2.png](https://i.postimg.cc/cCCk4bsg/log2.png)](https://postimg.cc/PvGQSKvT)

The ticket generation is fully customizable. For the newer version of script, we will have alert levels and other required inputs.

[![tickets.png](https://i.postimg.cc/VvhGSW67/tickets.png)](https://postimg.cc/tnhtwPFP)

For our timing loop we have used sched and time modules. Logging we will be added to script where we can see the timestamps for each ticket checks/generations. As well as positive traps to be clearing a ticket on ServiceNOW. 
