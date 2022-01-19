# spotify-board

## raspotify/librespot

1. Run the raspotify service as root by running `sudo systemctl edit raspotify.service` and adding the following between the comments

    ```
    [Service]
    DynamicUser=no
    ```
    
    Restart raspotify with `sudo service raspotify restart`
    

## Links

https://github.com/hzeller/rpi-rgb-led-matrix
