# SanState (GTA V: AltV server) authentication backend. 2021

README created for publication of this repository in 2023, 2y after its deprecation.

This repo contains login and register backend endpoints written in Python Flask. There's also an email integration to verify email adresses and recover passwords. This had to be an independent EarlyAuth microservice distinct from the main server and act as a firewall and IP authorization which redirects users to the game server.