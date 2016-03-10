# Distributed Load balancer
### Classes
* **Balancer** - will only contain the load balancing algo code. Will distrube the
tokens based on weight etc.
* **Client** - produces interface for the users to submit work or workers.
* **Token_serv** - Twister class which will accept tokens from others and also send
their status back to Token_client
* **Token_client** - Twister class which will send tokens to others and also accept
status from Token_serv
* **Worker** - will be implemented by the user. This will work on a token
* **Token** - This class will provide the token. there will be a data feild where
the user will put it data. It will also have a feild for solved.. which will
show wether the token is for solving or is it returing a result.
* **Worker_client/Worker_serv** - will distribute a worker.
* **Overview** - will collect log from all the hosts and show the transfer of
tokens etc..!!
* **Host_serv** - will announce the service, distribute the workers, produce the
status etc. Get the tokens as well as send them.

### First milestone
* Token
* Token_serv
* Token_client

### Second milestone
* Balancer
* Host_serv
* client

### Third milestone
* Worker_client/Worker_serv
* Worker

### Fourth Milestone
* Overview
