#!/bin/sh


# Load environment variables from the specified file
ENV_FILE="$(dirname "$(dirname "$(readlink -f "$0")")")/public.env"

if [ -f "$ENV_FILE" ]; then
    # shellcheck disable=SC1090
    source "$ENV_FILE"
else
    echo "Environment file not found. Please make sure to create a file named '.env' with your subdomains." >&2
    /bin/sh ./setup-env.sh
    echo "The env files has been created. Please configure it!"
    exit 1
fi

# IP address to which you want to route the subdomains
ip_address="127.0.0.1"

# Check if the user is an administrator (root)
if [ "$(id -u)" -ne 0 ]; then
    echo "Administrator (root) privileges are required to run this script." >&2
    exit 1
fi

# Check if DEBUG_BACKEND_HOST is set in the environment
if [ -z "$DEBUG_BACKEND_HOST" ]; then
    echo "DEBUG_BACKEND_HOST is not set in the environment. Please define it in your .env file." >&2
    exit 1
fi

# Check if DEBUG_FRONTEND_HOST is set in the environment
if [ -z "$DEBUG_FRONTEND_HOST" ]; then
    echo "DEBUG_FRONTEND_HOST is not set in the environment. Please define it in your .env file." >&2
    exit 1
fi

# List of subdomains from environment variables
subdomains=("$DEBUG_BACKEND_HOST" "$DEBUG_FRONTEND_HOST")

# Check for existing entries in /etc/hosts
for subdomain in "${subdomains[@]}"; do
    # Use grep to search for the subdomain and IP address in /etc/hosts
    if grep -q "$ip_address[[:space:]]*$subdomain" /etc/hosts; then
        echo "Entry for $subdomain already exists in /etc/hosts. Skipping."
    else
        # If entry doesn't exist, add it to /etc/hosts
        echo "$ip_address       $subdomain" >> /etc/hosts
        echo "Added entry for $subdomain to /etc/hosts."
    fi
done

echo "Done."
