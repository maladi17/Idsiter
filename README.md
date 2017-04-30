We wrote a "virus" which steal data from computer.

Our algorithem is as the following:

Our algorithem:

We get as an input text files of logs of the hids-s into some certain folder.  Those logs carry the number of queries in it as file names. Those files arrive after some parsing  and optimization.

We will use elk parser in order to do it and in order to count the packets type.
after getting the repeated packets time, we will insert it into a learning machine which calculate its series and predict the future packet of this type. we then notify the hids about our new rules.


We configured a Virtual  system in order to test our algorithem.  It wont work outside Our system because it demands the existence of hids,  parser and more. 

A youtube link as poc will be updated soon!
