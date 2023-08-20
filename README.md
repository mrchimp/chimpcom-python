# Chimpcom CLI

So there's a website that looks like a command line. So what else do we need? Why a way to access the website from your command line. Of course.

# Setup

1. Copy `main.py` to somewhere on your `$PATH`. E.g.

   ```sh
   $ cp main.py /usr/local/bin/chimpcom
   ```

2. Get a token from [Chimpcom](https://deviouschimp.co.uk)

   ```sh
   # Note: Run this on deviouschimp.co.uk not in your terminal!
   $ token --create some_token_name
   ```

3. Enter your token.

   ```sh
   $ chimpcom token
   # ...then follow the instructions
   ```

4. You shouldn't have to enter your token again.

5. You might want to alias chimpcom with your username. E.g.

   ```sh
   alias chimpcom="chimpcom --username=AzureDiamond"
   ```

# Arguments

- `--token`

  Use this flag to set your token. Your token will be stored in your OS's keyring.

- `--url`

  The URL to use as the Chimpcom API. Defaults to `https://deviouschimp.co.uk/api/respond`.

- `--username`

  The Chimpcom username to use. This allows you to store multiple tokens.
