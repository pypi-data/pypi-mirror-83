# Braincube Token Getter

Braincube Token Getter is small program that uses the braincube sso in order to obtain a temporary token.

The program uses the flask python framework.

## Installation

```bash
pip install braincube-token-getter
```

## Usage

### Create a new configuration

By default the new configuration is stored in `~/.braincube/`  but the option `-p` or `--path` can be used to specify a specific configuration directory.

```bash
braincube-token-getter -c -p my_directory
```

The program will ask for a Baincube application *Client ID*  and *Client Secret*. If you do not know how to find these informations or how to create a Braincube application, see the section *Create a Braincube application*.

### Request a token

```bash
braincube-token-getter -t
```

The token is added to the `my_directory/config.json` file.

Note: your browser may warn you with a Security risk because your ssl certificate is not known by firefox or chrome. In this case click on `Advanced...` and `Accept the Risk an Continue`.

## Create a Braincube application

1. Connect to [mybraincube.com/](https://mybraincube.com/)

2. Go to `Configure` by clicking on you *username* on the top left corner.
3. Go to application on the thin horizontal menu bar just below the black header.
4. Either select an existing application you want to use or create a new one with the +/- icon.
5. Note that the url of your application should be `https://localhost:5000/token` so that the program gets the right url when it logs in.
