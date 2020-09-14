# Page load timer

## Setting up the environm env

#### Virtualenv
I use virtualenv but it is not strictly speaking necessary

```
virtualenv venv
source /venv/bin/activate
```

#### Environment variables
You will environment variables for the location of the Selenium browser, and the database,  ```BROWSER``` and ```DATABASE```

```
export DATABASE=mongodb://root:example@192.168.1.35:27017/
export BROWSER=http://127.0.0.1:4444/wd/hub
```

You can either export these manually each time (not reccomended) or add them to the activation script for the virtual environment (reccomended)
Simply edtit the file ```/venv/bin/activate``` and add 
```
export DATABASE=mongodb://user:password@hostname:port/
export BROWSER=http://127.0.0.1:4444/wd/hub
```
#### Python packages installation
```
pip3 install -r requirements.txt
or
pip install -r requirements.txt
```

### Other requirements
You will need to run a Selenium browser, and to do that, you need Java, so that must be installed
Selenium can be downloaded from [here](https://www.selenium.dev/downloads/), just look for ```latest stable release```
When this ```README``` is written, [this](https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar) is the latest stable version

To run Selenium, open up the terminal and ```cd``` into the directory where selenium was downloaded and run

```
java -jar selenium-server-standalone-3.141.59.jar
```
replace ```3.141.59``` with your version

This will run Selenium at ```127.0.0.1:4444```

Note that if necessary, Selenium can also be run remotely, but it must be run on a computer *WITH A MONITOR*
So the script can run anywhere, as long is has access to the Selenium browser

#### Initializing the database
Just create a database called ```timer```

# Usage
```
python run.py --cores 1 --sites ./sites.txt
```

The default value for ```cores``` is ```1``` and the default value for ```sites``` is ```sites.txt```

When you start up the program, there should pop up firefox windows, as many as the ```cores``` argument was set to. The program will print out how many cores were selected and it will list out all the pages to be opened from the file chosen by the  ```sites``` argument.

The program will save into ```MongoDB``` into two collections, ```root``` and ```timings```

Collection ```root``` will store:
* ```datetime```: DateTime of the run
* ```url```: URL of the page
* ```time```: Total runtime to load the page
* ```timings```: List of ```ObjectId``` that maps to the collection ```timings```

Collection ```timings``` will store several properties **as they appear in the data collected from the network tab**, typically something similar to

```
{'connectEnd': 1328,
 'connectStart': 1328,
 'decodedBodySize': 222,
 'domainLookupEnd': 1328,
 'domainLookupStart': 1328,
 'duration': 67,
 'encodedBodySize': 126,
 'entryType': 'resource',
 'fetchStart': 1328,
 'initiatorType': 'script',
 'name': 'https://cdn.polyfill.io/v2/polyfill.min.js?features=default-3.6,Array.prototype.includes,fetch,Promise',
 'nextHopProtocol': 'h2',
 'redirectEnd': 0,
 'redirectStart': 0,
 'requestStart': 1331,
 'responseEnd': 1395,
 'responseStart': 1394,
 'secureConnectionStart': 0,
 'serverTiming': [{'description': '', 'duration': 0, 'name': 'HIT'},
                  {'description': 'Edge time',
                   'duration': 0,
                   'name': 'fastly'}],
 'startTime': 1328,
 'transferSize': 277,
 'workerStart': 0}
```

