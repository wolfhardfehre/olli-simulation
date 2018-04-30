# Open Olli Simulation

[![Build Status](https://travis-ci.org/wolfhardfehre/olli-simulation.svg?branch=master)](https://travis-ci.org/wolfhardfehre/olli-simulation) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Maintainability](https://api.codeclimate.com/v1/badges/9c340690fb19fda2b2df/maintainability)](https://codeclimate.com/github/wolfhardfehre/olli-simulation/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/9c340690fb19fda2b2df/test_coverage)](https://codeclimate.com/github/wolfhardfehre/olli-simulation/test_coverage)

## Introduction

A small tool to simulate the movement of a autonomous shuttle called 'Olli'. This repository is part of the
[Open Olli Hackathon][1] and will build the foundation for a On-Demand-System consisting of a server and a
mobile application. The underlying vehicle data can be found [here][2]. To build a rail like infrastructure
[OpenStreetMap][3] data is used and queried through the [OverpassApi][4].

## Installation

1) You'll need python 3.5
2) Clone this repository
3) Add a folder called `resources` and in this folder the file called `vehicle_states.csv` you can download [here][2].
4) Add a file call `secret.py` into `app/app` folder and paste this line `TOKEN=<Your Mapbox Token>` with your Mapbox Token.

### Virtual Environment (Ubuntu)

1) `sudo apt install python3-venv`
2) `python3 -m venv venv`                               (create virtual env)
3) `source venv/bin/activate`                           (activate virtual env)
4) `pip install --upgrade pip`                          (pip upgrade)
5) `pip install -r requirements.txt`                    (install libs)
[automation]
6) `deactivate`                                         (to leave the virtual env)
7) `pip install autoenv==1.0.0`                         (install autoenv locally)
8) ``echo "source `which activate.sh`" >> ~/.bashrc``   (link autoenv to automatically start `venv` when `cd`ing into it) 
9) `source ~/.bashrc`                                   (update system to new `bashrc` settings)
10) you probably have to configure PyCharm settings (interpreter) if you use this IDE


## Run Tests

`python -m unittest discover`

## Communications

* Via [Slack][5]

## License

    Copyright 2018 Where's my Olli Team

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


[1]: https://hackathon.innoz.de
[2]: https://hackathon.innoz.de/data
[3]: https://www.openstreetmap.org
[4]: https://wiki.openstreetmap.org/wiki/Overpass_API
[5]: https://open-olli-hack.slack.com/messages
