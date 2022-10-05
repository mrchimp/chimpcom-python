# Chimpcom CLI

So there's a website that looks like a command line. So what else do we need? Why a way to access the website from your command line. Of course.

# Setup

1. Copy `main.py` to somewher on your `$PATH`. E.g.

    ```sh
    cp main.py /usr/local/bin/chimpcom
    ```

2. Get a token from [Chimpcom](https://deviouschimp.co.uk)

    ```sh
    $ token --create some_token_name
    ```

3. Enter your token.

    ```sh
    $ chimpcom token
    # ...then follow the instructions
    ```

4. You shouldn't have to enter your token again.