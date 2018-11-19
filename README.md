# rpi-daq-analysis


## Example:

```python main.py --fileName=toto.raw --headerSize=48 --maxEvents=100```

Will run on raw data file, estimate pedestal and noise for each connected channel (according to electronic map for 6 inches modules). At the end, pedestal and noise maps are plotted.

Header size should be 48 if the same configuration bit string was used for each CHIP. It should 192 if one bit string is used per CHIP. 
