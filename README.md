# ec2-custom-proxy

Redirect web traffic via an ec2 instance(global IP) to a desired web application behind a NAT(Accessible via VPN).
Usage: Change up the ec2 instance links to thr global IP which acts as the proxy. 

Run the web_server_pipe.py file on the ec2 instance/ global IP server. Run the client file on a local machine which has access to the guarded network you want to reach out. 
