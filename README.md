#1. Convert .raw to .flac
sox -r 44100 -e unsigned -b 24 -c 1 coeff.raw coeff.flac

#2 play .flac
flac -c -d coeff.flac | aplay


