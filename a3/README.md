This code is meant to replicate the leader election algorithm using asynchronous rings operating in O(n^2) time. To use it, you must configure the config.txt file first
to match port numbers in a circle (like 5001,5002,5003,->5001), keep ip as 127.0.0.1(localhost) and port number 5001, then 5002, like this:
127.0.0.1,5001
127.0.0.1,5002
Then do 5002, 5003, and then 5003, 5001 to complete a ring.
Make sure you update the config file right before running each process, or you might make a duplicate IP (which it will warn you about), and also don't take too long
so it doesn't time out.
The three log files write down what each process is printing in console.

The first node:
![Screenshot 2025-07-08 233127](https://github.com/user-attachments/assets/3db594da-8db9-4d7b-a42d-65fca69747e5)
The second node:
![Screenshot 2025-07-08 233142](https://github.com/user-attachments/assets/14332044-61ca-41a3-8bfd-c6957fc350b8)
The third node:
![Screenshot 2025-07-08 233150](https://github.com/user-attachments/assets/60bf9a62-9c56-4c4e-a962-b4123fab3ccf)

