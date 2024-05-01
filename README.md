# What is this repository?
I have build this small script in order to search for an appointment spot from the Berlin Immigration Office, a.k.a Landesamt für Einwanderung (LEA).

# How to run?
You need to have [Docker](https://www.docker.com/) or [Orbstac](https://orbstack.dev/) on your machine.
Then, you can run the following command on your terminal.
```
docker compose up --build
```

By default, this script will run every two minutes.

# Why do we need an script?
It is almost impossible to get an appointment from the Berlin Immigration Office. I have
been trying to get an appointment for months. It has been thousands of attempts, but none
of them were successful.

I am really tired of clicking, and getting this annoying error message.
![There are currently no dates available for the selected service! Please try again later.](docs/error_message.png)

I decided to let my computer get this message instead of me, and notify me when there is an available spot.

# Is the script successful?
Yes and no. My automation found only one appointment slot after running two days, but unfortunately I could not get it.

# Why do I publish this script?
- You can execute this script on your computer, and search for an appointment for yourself.
- Python and browser automation are new topics for me. I would learn from the expert opinions.
- I have spent approximately 15 hours in order to make this work, and I would like other fellow developers living in Berlin to have some starting point.