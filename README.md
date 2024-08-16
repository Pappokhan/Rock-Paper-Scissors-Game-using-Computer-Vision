# Rock-Paper-Scissors Game with Hand Gesture Recognition

This project is a fun Rock-Paper-Scissors game that uses your webcam to recognize hand gestures in real time. The game detects if you show Rock, Paper, or Scissors and compares it with a random choice from the computer. Enjoy a countdown before each new round and see the winner right away. You can quit anytime by pressing 'q'.

## Features
- **Real-time Gesture Recognition:** Uses MediaPipe and OpenCV to recognize hand gestures.
- **Interactive Gameplay:** The game provides a countdown before each round.
- **Instant Results:** See the winner immediately after each round.
- **Easy to Quit:** Press 'q' to exit the game anytime.


### Prerequisites
- Python 3.x
- OpenCV: `pip install opencv-python`
- MediaPipe: `pip install mediapipe`

## How It Works
- The game uses a webcam feed to detect hand gestures.
- MediaPipe's hand tracking model identifies hand landmarks and classifies gestures as Rock, Paper, or Scissors.
- The game logic then compares the player's gesture with the computer's random choice to determine the winner.


## License
This project is open-source and available under the [MIT License](LICENSE).
