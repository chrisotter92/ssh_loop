# ssh_loop
Attempt to loop through password for ssh

This is an attempt of setting up threading within multiprocessing. I've been having issue in different enviroments where going 
above 100 threads causes a "No existing sessions" with in Paramiko. My work around for this then was to setup Multiprocessing
with threading so I could still connection to all the devices I need to in a timely manner. With the limited testing I've done
when running the same script to ssh between 300 threads (dev enviroment doesn't limit my threads) and multiprocess with 32 
processes with 50 threads each I've been able to go from ~11 minutes to attempt to ssh into ~4,700 devices to ~8 minutes. In the
enviroments that I'm limited to 100 threads I've been able to go from ~18 minutes to ~8 minutes to do the same work.

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites

Python 2.7 (haven't tested in 3 yet)  
Paramiko  
Netmiko  

Installing

THIS IS NOT A MODULE, this is to be used as a template for your own enviroment to setup your own functions within for whatever
you want to Multiprocess/Thread.

python ssh_loop.py  
Connection to x.x.x.x was successful.  
Connection to x.x.x.x was successful.  
Connection to x.x.x.x was successful.  
Connection to x.x.x.x was successful.  
Connection to x.x.x.x timed out.  
Connection to x.x.x.x was successful.  
Authentication to x.x.x.x failed.  
Connection to x.x.x.x was successful.  
etc......  
Total time to ssh into all devices 0:08:54.193422.  

License

This project is licensed under the MIT License - see the LICENSE.md file for details
Acknowledgments

    Jeremy Mesloh for testing, vetting, and general knowledge!
    Kirk Byers - Netmiko, also thank you for helping fix stale ssh sessions not closing that never established!
    Jeff Forcier and Robey Pointer - Paramiko, thanks for providing the foundation for everything!
