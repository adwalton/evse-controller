# evse-controller

This is a system whose purpose is to control "smart" EVSEs such as the Wallbox Quasar. I have referred to
the source code of the [v2g-liberty](https://github.com/SeitaBV/v2g-liberty/) project to create it, but none of the code
is shared; this is intended to be simpler and more of a standalone project. In particular, this project is not intended
to use Home Assistant; if your needs include using Home Assistant then the above project may well be more suited to your
needs.

I have completed some library routines declaring the interfaces used for controlling EVSEs and reading from power
monitors and I have implemented these for the following devices:

* [Wallbox Quasar](https://wallbox.com/en_ca/quasar-dc-charger) for EV charging and discharging (V2G)
* [Shelly EM](https://shellystore.co.uk/product/shelly-em/) for energy monitoring enabling solar energy capture (like S2V)
  and load following (like V2H); here it is assumed that grid power is monitored through channel 0 and EVSE power through
  channel 1. The EVSE channel is only used for monitoring and reporting and could be substituted with the solar power, for
  example.

There's also a complete project that uses those libraries to provide V2X
functions along with logging, scheduled events, and web or console control
and its installation and basic use are detailed below.

This code may look more Javaesque than Pythonesque - I have more expertise in Java but I've chosen Python so that I can
learn a little bit more.

This uses code from a library that can use a Web API to control the Wallbox Quasar, but that code is only used to
restart the wallbox in the case of modbus failure, a condition that happens once every few days to myself. The library
used for this can be found here:

* https://github.com/cliviu74/wallbox

This has been tested and seems to work well.

I have also added logging to InfluxDB OSS version 2. This is the open-source variant and is documented here:

* https://docs.influxdata.com/influxdb/v2/
* https://docs.influxdata.com/influxdb/v2/install/?t=Linux for installation instructions if using Linux (also go to
  that page for other operating systems as the instructions are also there).

I do not believe it will work with version 1. If you just try `apt install influxdb`, it is likely that you will get
version 1, so I would suggest installing as per the official instructions on the page above.

## Detailed Setup Instructions

### Prerequisites
- Python 3.11.7 or 3.12.3
- An EVSE device (currently supports Wallbox Quasar)
- A power monitor (currently supports Shelly EM)
- Optional: InfluxDB OSS v2 for logging
- Optional: poetry (an alternative installation method to pip)

### Installation Steps

1. **Clone the Repository (or download it)**
   ```bash
   git clone https://github.com/robynrox/evse-controller.git
   cd evse-controller
   ```

   Alternatively download the ZIP file from GitHub by navigating to
   https://github.com/robynrox/evse-controller, clicking the Code dropdown and selecting Download ZIP. Then unpack it.

2. **Choose Setup Method**

   A. Using Dev Container (Experimental):
   - Install Docker and VS Code with Dev Containers extension
   - Open project in VS Code
   - Click "Reopen in Container" when prompted
   - Container will automatically install dependencies
   
   Note: Container support is currently experimental and hasn't been thoroughly tested. 
   For production use, I recommend using either the pip or Poetry installation methods.

   B. Using pip:
   ```bash
   # Navigate to your project directory
   cd path/to/evse-controller
   
   # Create virtual environment in a .venv subdirectory
   python3 -m venv .venv
   
   # Activate the virtual environment
   # On Linux/macOS:
   source .venv/bin/activate
   # On Windows:
   .\.venv\Activate.ps1
   
   # Install in development mode
   pip install -e .
   ```

   C. Using Poetry (Alternative):
   ```bash
   # Install Poetry if you haven't already
   # On Linux/macOS/WSL:
   curl -sSL https://install.python-poetry.org | python3 -

   # On Windows (PowerShell):
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

   # Navigate to project directory
   cd path/to/evse-controller

   # Install dependencies using Poetry
   poetry install

   # Install development dependencies (includes pytest for testing)
   poetry install --with dev

   # Activate the virtual environment
   poetry shell

   # Run unit tests as desired
   pytest
   ```

   Note: The virtual environment will be created in your project directory, regardless of which installation method you choose. You can clone or download this repository to any location on your system.

3. **Configuration**

   Before configuring, you may want to use the discovery tool to find your devices.
   See `evse-discovery/README.md` for detailed information about the discovery process.

   There are two ways to configure the application:

   A. Interactive Configuration:
   ```bash
   python configure.py
   ```
   This will guide you through setting up:
   - Wallbox connection details
   - Shelly EM configuration
   - InfluxDB settings (optional)
   - Charging preferences
   
   B. Manual Configuration:
   - Edit `config.yaml` directly (created by configure.py)
   - Configuration structure:
     ```yaml
     wallbox:
       url: "WB012345.ultrahub"  # Hostname or IP address
       username: "myemail@address.com"  # Optional, for auto-restart
       password: "yourpassword"         # Optional, for auto-restart
       serial: 12345                    # Optional, for auto-restart
     shelly:
       primary_url: "shellyem-123456ABCDEF.ultrahub"  # Hame or Io  IPdadrress
       secondary_url: null              # Optional second Shelly
     influxdb:
       enabled: false
       url: "http://localhost:8086"
       token: ""
       org: ""
     logging:
       file_level: "DEBUG"
       console_level: "WARNING"
       directory: "log"
       file_prefix: "evse"
       max_bytes: 10485760             # 10MB
       backup_count: 30
     charging:
       max_charge_percent: 90          # Maximum battery charge percentage
       solar_period_max_charge: 80     # Maximum charge during solar generation periods
       default_tariff: "COSY"          # COSY, OCTGO or FLUX
     ```

   Note: The old `configuration.py`/`secret.py` method is deprecated and will be removed in a future version.

4. **Start the Application**
   ```bash
   python -m evse_controller.app
   ```
   Access the web interface at http://localhost:5000

   It is also possible to start the application with `python -m evse_controller.smart_evse_controller` if the web interface is not required.

### Configuration Options

Detailed explanation of each configuration option:

#### Wallbox Section
- `url`: IP address or hostname of your Wallbox Quasar
- `username`: Your Wallbox account email (optional, for auto-restart feature)
- `password`: Your Wallbox account password (optional, for auto-restart feature)
- `serial`: Your Wallbox serial number (optional, for auto-restart feature)

#### Shelly Section
- `primary_url`: IP address or hostname of your primary Shelly EM
- `secondary_url`: IP address or hostname of your second Shelly EM (optional)

#### InfluxDB Section
- `enabled`: Whether to enable InfluxDB logging (true/false)
- `url`: URL of your InfluxDB instance (default: http://localhost:8086)
- `token`: Authentication token for InfluxDB
- `org`: Organization name for InfluxDB

#### Charging Section
- `max_charge_percent`: Maximum battery charge percentage (0-100)
- `solar_period_max_charge`: Maximum charge during solar generation periods (0-100)
- `default_tariff`: Default electricity tariff (COSY, OCTGO, or FLUX)

#### Logging Section
- `file_level`: Logging level for file output (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `console_level`: Logging level for console output (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `directory`: Directory for log files
- `file_prefix`: Prefix for log filenames
- `max_bytes`: Maximum size of each log file in bytes (default: 10MB)
- `backup_count`: Number of backup log files to keep

Note: The configuration file is automatically generated by running 
`configure.py`, which provides an interactive setup process. You can also
edit the `config.yaml` file directly if you prefer.

## Provided samples

The following samples are provided:

* `src/evse_controller/smart_evse_controller.py`: Control the wallbox for Octopus Go or Cosy Octopus. This is what I expect to maintain going forward.
  It will have control logic to drive the Flux tariff added as well, and possibly Agile at some point.
* `src/evse_controller/app.py`: At the time of writing, this runs the controller along with a web interface that allows the same basic
  controls that you can type interactively into the terminal.


I removed the command-line argument parsing since interactive control and web control are now available.

## API Documentation

The system provides a REST API that can be explored and tested using the built-in Swagger UI:

1. Start the application using `python -m evse_controller.app`
2. Open a web browser and navigate to `http://localhost:5000/api/docs`
3. The Swagger UI provides:
   - Interactive documentation for all API endpoints
   - The ability to test API calls directly from your browser
   - Detailed request/response models
   - Example values and expected responses

Key API features include:
- Control operations (charge, discharge, pause)
- Status monitoring
- Schedule management
- Configuration

### Development Environment Notes

If using VS Code (recommended):
1. The Dev Container configuration will automatically set up the correct environment
2. If developing outside the Dev Container, you'll need to select the correct Python interpreter:
   - Open Command Palette (View > Command Palette, or `Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment (in the project's `.venv` directory)

### Docker Compose Support (Experimental)

A Docker Compose configuration is available but has not been thoroughly tested recently:

```yaml
version: '3.8'
services:
  evse-controller:
    build: .
    volumes:
      - evse-data:/data
    environment:
      - EVSE_DATA_DIR=/data
    ports:
      - "5000:5000"

volumes:
  evse-data:
    name: evse-controller-data
```

For production use, I recommend using either the pip or Poetry installation methods.

## Limitations

- Currently only supports Wallbox Quasar for EVSE and Shelly EM for power monitoring. Other devices would require new interface implementations.
- The scheduling system supports Octopus Go, Cosy Octopus, and Octopus Flux tariff patterns. Agile tariff support is not implemented. Tariffs from other suppliers are also not implemented. There is an interface allowing for reasonably straightforward implementation of additional tariff support.
- The Wallbox occasionally requires automatic restarts due to Modbus communication issues, causing approximately 6 minutes of downtime when this occurs. Manual power cycling might be needed 3-4 times per year.
- The web interface is designed for local network use and doesn't include authentication or security features for remote access.
- The web interface currently has limited accessibility features. Users requiring screen readers or keyboard-only navigation may experience difficulties. If you need accessibility features, please open an issue on GitHub to discuss your requirements.

## Roadmap

* Creation of abstract APIs to control EV charging and discharging and to use current-monitoring CT clamps other than
  the Shelly (the APIs are complete)
* Add a user interface allowing for rapid termination of any current EV charging or discharging session (HTML seems to
  be the obvious way to go - this is now in progress and a working prototype is available)
* Add V2G and S2V capabilities that may be independently specified during a scheduled slot (this capability is now part
  of the library routines and is being added to the user interface)
* Add scheduling functionality based on a user-selected desired schedule including percentage-of-charge targets
  (basic scheduling is now available)
* I'm trying to attach greater importance to bug-fixing; it's more important for it to be solid than look pretty.

The above is an ideal and some of it is sure to be done out of order!

## Explanatory video

I have produced a video that explains my setup, how I use the system, and goes into some detail regarding the flux.py
scheduler. Note that it is long at 66 minutes! It is somewhat outdated now, but most of it still applies. You can find
that here:

* https://youtu.be/4bIpY-AyUUw
