import os
import httpx
import sys

def unpause_supabase():
    # Use environment variables directly, often provided by GitHub Secrets in a cron job
    access_token = os.environ.get("SUPABASE_ACCESS_TOKEN")
    project_ref = os.environ.get("SUPABASE_PROJECT_REF")

    if not access_token or not project_ref:
        print("Error: SUPABASE_ACCESS_TOKEN and SUPABASE_PROJECT_REF environment variables must be set.")
        sys.exit(1)

    url = f"https://api.supabase.com/v1/projects/{project_ref}/restore"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    print(f"Attempting to unpause Supabase project: {project_ref}")

    try:
        # Using a timeout as the restoration trigger might take a moment to respond
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers)

            if response.status_code in (200, 201):
                print(f"Success! Status code: {response.status_code}")
                print(f"Response: {response.text}")
            elif response.status_code == 403:
                print("Error: 403 Forbidden. Check if your access token is valid and has permission for this project.")
                sys.exit(1)
            elif response.status_code == 404:
                print(f"Error: 404 Not Found. Check if the project ref '{project_ref}' is correct.")
                sys.exit(1)
            elif response.status_code == 409:
                print("Project is already active or another operation is in progress.")
            else:
                print(f"Failed to unpause project. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                sys.exit(1)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    unpause_supabase()
