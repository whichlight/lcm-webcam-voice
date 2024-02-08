# lcm webcam voice

Here's the prototype for LCM and physical objects demo created for the prompt "LCM" during the AIxUIdailies coding challenge. You can [see the demo video here](https://twitter.com/whichlight/status/1737753583859433513).

See all of the prototypes for the challenge [here](https://twitter.com/whichlight/status/1740225262552514613).

## Setup

1. Do the fal authentication: https://www.fal.ai/docs/authentication/key-based
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run

1. run `listen.py` to get the voice to text for prompts

2. then run `see.py` to take regular snapshots from the cam

3. then run `run_lcm_fal.py` to loop taking the prompt and the image and running LCM, saving the image link to a txt file

4. use something like Photobooth to see what's on the webcam

5. Run server.py to see the image

There's a ton of latency, so the next thing to do here is rewrite it in the browser, which fal is great for.
