def write_log(response, filetype, name):
    """ Write a requests response object as a file for logging """
    with open(f"{name}_response.{filetype}", "w") as response_file:
        response_file.writelines(response)
