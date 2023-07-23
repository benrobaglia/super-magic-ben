# Super Magic Ben DApp

Super Magic Ben is an on-chain speaker verification neural network model called Kaldi that aims to revolutionize identity verification by leveraging the unique characteristics of individuals' voices. Deployed on the Cartesi platform, this project represents a powerful combination of blockchain's transparency and decentralization with the sophisticated capabilities of neural networks for voice recognition.

Traditional methods of identity verification, such as passwords or fingerprint scans, are susceptible to security breaches and identity theft. Biometric technologies, including voice recognition, offer an innovative and more robust approach to identity verification.

Voice biometrics, a form of speaker verification, analyzes an individual's unique vocal characteristics, including pitch, tone, and speech patterns, to create a voiceprint. Just like fingerprints, voiceprints are distinct to each person, making it highly reliable for identity verification. This technology holds tremendous promise in enhancing security measures, ensuring access to authorized individuals while thwarting unauthorized access attempts.

By leveraging Cartesi, our project can overcome the computational limitations of traditional on-chain smart contracts, enabling the deployment of sophisticated machine learning models such as neural networks. By using Kaldi I vector models, we are able to achieve computation efficiency and accuracy for the verification process. 

The project's potential use cases are diverse and far-reaching. In the financial sector, speaker verification can be employed for secure access to banking accounts, preventing fraudulent transactions, and enhancing user authentication for financial services. In the healthcare industry, it can be used to secure access to sensitive patient information and ensure the accuracy of medical records. 

Our on-chain speaker verification neural network model, deployed on the Cartesi platform, represents a pioneering approach to identity verification. By leveraging the unique characteristics of individuals' voices, we offer a robust and secure method for identity verification, harnessing the power of blockchain's transparency and decentralization. 

## Kaldi model
The Kaldi Automated Speech Recognition (ASR) model is implemented in the `speaker_id.py` file, in the class `SpeakerId`. This model computes the x-vectors of the speaker, an abstract embedding of the speaker's voice that represents it. The main available functions are `SpeakerId.create_speaker`, that creates a new user voice print under the form of a x-vector in the database and `SpeakerId.verify_speaker` that compares the input voice (transformed in an x-vector) to the x-vector associated to his id in the database.

## Interacting with the application

We use the Jupyter Notebook `data_science_front_end.ipynb` to interact with the application.


## Running the environment in host mode

We have developed and tested our DApp's back-end on the host machine, allowing it to be debugged using regular development tools such as an IDE.

The host environment can be executed with the following command:

```shell
docker compose -f ../docker-compose.yml -f ./docker-compose.override.yml -f ../docker-compose-host.yml up     
```

And shut down with:

```shell
docker compose -f ../docker-compose.yml -f ./docker-compose.override.yml -f ../docker-compose-host.yml down -v     
```


This DApp's back-end is written in Python, so to run it in your machine you need to have `python3` installed.

In order to start the calculator back-end, run the following commands in a dedicated terminal:

```shell
cd calculator/
python3 -m venv .env
. .env/bin/activate
pip install -r requirements.txt
ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 calculator_speaker_id.py
```

This will run the calculator back-end and send the corresponding notices to port `5004`.
It can optionally be configured in an IDE to allow interactive debugging using features like breakpoints.


After the back-end successfully starts, it should print an output like the following:

```log
INFO:__main__:HTTP rollup_server url is http://127.0.0.1:5004
INFO:__main__:Sending finish
```

After that, you can interact with the application normally [as explained above](#interacting-with-the-application).
