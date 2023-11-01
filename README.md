### Features:
- Torpoker is an open-source client application to play **_no-limit Texas hold'em poker._**
- 6 Players tables are available
- **Socks5 and TLS** are supported.
    - Note: when using **socks5** , **TLS** is optional, and **wihtout socks5, TLS is required**
- **No registration is required** to play and player's session is lost after closing the application.
    -  To recover player's session, there are shortcuts to get and set its value
        -  On tables list, `Ctrl + N` to set its value,
        -  and `Ctrl + T` to get its value.
-  Torpoker UI has been developed with `PyQt5` libraries. A live chat is also included on 6-players tables and game can be watched as spectator.

### Requirements
- Python version `[>= 3.7]`
    - check by typing on terminal:
        `$ python3 --version`
- `PyQt5`

### Installation
 * For Windows Operating Systems
 ```bat
 $ pip install PyQt5
 ```
 * For Linux and Mac OS
```sh
$ python3 -m pip install --upgrade pip setuptools wheel
$ python3 -m pip install PyQt5
```
For debian-based install using `apt-get install python3-pyqt5`
- [**Important:** For windows and Mac OS, `certifi` is required for TLS connections]
    ```sh
    $ pip install certifi
    ```

### Usage
After installing the required packages, to launch Torpoker, run the following command from terminal:
```sh
$ python3 run_torpoker.py
```

## Official Servers:
Torpoker's official servers are as follows:
- torpoker766qetslucfe2jrq7wz63r4tt5vn4pznq5crzniin5up65id.onion port 80
- torpoker.gg port 443


## Testrun for Developer:
-If you want to do a test run to check whether the workflow works, 
you have to start the test_workflow script in the test_files folder.

