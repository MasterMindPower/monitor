import os
import requests
import datetime

def main():
    # Get URLs from environment variable (GitHub Secret)
    # Expected format: comma-separated or newline-separated
    urls_env = os.environ.get("URLS", "")
    
    if not urls_env:
        print("No URLs found in the 'URLS' environment variable.")
        return

    # Split by comma or newline and strip whitespace
    urls = [url.strip() for url in urls_env.replace('\n', ',').split(',') if url.strip()]
    
    log_entries = []
    
    for index, url in enumerate(urls):
        try:
            response = requests.get(url, timeout=10)
            status = "success" if response.status_code == 200 else f"failed (status code: {response.status_code})"
        except requests.RequestException as e:
            # Shorten the error message to avoid overly long logs
            status = f"failed (error: {type(e).__name__})"
            
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"URL {index + 1} : {status} {current_time}"
        print(log_entry)
        log_entries.append(log_entry)
        
    # Write to log-url file (overwriting previous data)
    log_file_path = "log-url"
    
    with open(log_file_path, "w", encoding="utf-8") as f:
        for entry in log_entries:
            f.write(entry + "\n")

if __name__ == "__main__":
    main()
