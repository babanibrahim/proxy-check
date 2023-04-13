import requests
import concurrent.futures

# Define the function to test each proxy
def test_proxy(proxy):
    try:
        # Set the URL to test
        url = 'https://www.google.com'
        # Set the proxy URL with the format "http://username:password@proxy_ip:proxy_port"
        proxy_url = f"http://{proxy}"
        # Define the request headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
        }
        # Send the request using the proxy
        response = requests.get(url, headers=headers, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
        # Check if the request was successful
        if response.status_code == 200:
            print(f"\033[32mProxy {proxy} is working!\033[0m")
            return proxy
        else:
            print(f"\033[31mProxy {proxy} returned status code {response.status_code}\033[0m")
    except:
        # If there is an error, assume the proxy is not working
        print(f"\033[31mProxy {proxy} is not working\033[0m")

# Define the function to read the list of proxies from a text file
def read_proxies():
    with open(file_name, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

# Define the function to write the working proxies to a new text file
def write_proxies(proxies):
    with open('newproxies.txt', 'w') as file:
        for proxy in proxies:
            file.write(proxy + '\n')

# Set the maximum number of threads to use
MAX_THREADS = 20

# Print the banner
print("\033[1m*******************************************************************\033[0m")
print("\033[1m*\033[0m                                                                 \033[1m*\033[0m")
print("\033[1m*\033[0m                     \033[1m🐬Ocean Academy🐬 Proxy Tester🐬\033[0m            \033[1m*\033[0m")
print("\033[1m*\033[0m                                                                 \033[1m*\033[0m")
print("\033[1m*******************************************************************\033[0m")

try:
    # Get the name of the file containing the list of proxies from the user
    file_name = input("Enter the name of the file containing the list of proxies: ")

    # Read the list of proxies from the text file
    proxies = read_proxies()

    # Create a thread pool executor to run the tests
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Submit each proxy to the thread pool
        futures = [executor.submit(test_proxy, proxy) for proxy in proxies]

        # Gather the results from the completed futures
        working_proxies = [future.result() for future in concurrent.futures.as_completed(futures) if future.result()]

    # Write the working proxies to a new text file
    write_proxies(working_proxies)

except KeyboardInterrupt:
    print("\nProgram stopped by user.") # Print a message to inform the user that the program was stopped by them
    exit()
