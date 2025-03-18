docker ps
docker rm rasa-bot
docker pull rasa/rasa:latest
chmod -R 777 /mnt/Data/projects/Data_Analytics/chatbot-rasa/rasa_data
docker run -it --name rasa-bot -p 5005:5005 -v /mnt/Data/projects/Data_Analytics/chatbot-rasa/rasa_data:/app rasa/rasa init
docker stop rasa-bot
docker rm rasa-bot
docker run -it --name rasa-bot -p 5005:5005 -v /mnt/Data/projects/Data_Analytics/chatbot-rasa/rasa_data:/app rasa/rasa shell --enable-api --cors "*"




