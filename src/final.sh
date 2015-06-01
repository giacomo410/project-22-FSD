python init.py

gnome-terminal -e "bash -c \"python gatherer_tagger.py; exec bash\""

gnome-terminal -e "bash -c \"python detector.py; exec bash\""
