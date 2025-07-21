This code is meant to replicate the leader election algorithm using asynchronous rings operating in O(n^2) time. To use it, you must configure the config.txt file first to match port numbers in a circle (like 5001,5002,5003,->5001), keep ip as 127.0.0.1(localhost) and port number 5001, then 5002, like this: 127.0.0.1,5001 127.0.0.1,5002 Then do 5002, 5003, and then 5003, 5001 to complete a ring. Make sure you update the config file right before running each process, or you might make a duplicate IP (which it will warn you about), and also don't take too long so it doesn't time out. The three log files write down what each process is printing in console.

Edit: This has been fixed to always work now, because now the correct message is forwarded (it used to fail to forward).
Process 1:
<img width="902" height="282" alt="image" src="https://github.com/user-attachments/assets/3fac831f-6857-4b74-94c4-c7b98415f7b8" />
Process 2:
<img width="910" height="310" alt="image" src="https://github.com/user-attachments/assets/3a15fabc-5954-4d74-88c1-7449f7583315" />
Process 3:
<img width="897" height="229" alt="image" src="https://github.com/user-attachments/assets/5589b6c2-f66e-443a-b6dd-3687f143e1b4" />
