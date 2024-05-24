# Define the path to your .env file
$envFile = ".\.env"

# Check if the file exists
if (Test-Path $envFile) {
    # Read each line in the file
    Get-Content $envFile | ForEach-Object {
        # Split each line around the '=' character
        $keyValue = $_.Split('=')
        if ($keyValue.Length -eq 2) {
            # Trim spaces and remove surrounding quotes from the value
            $key = $keyValue[0].Trim()
            $value = $keyValue[1].Trim().Trim('"')

            # Set the environment variable
            [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
        }
    }
    Write-Host "Environment variables loaded from .env"
} else {
    Write-Host "No .env file found"
}
