from requests import Session

from config.error import ValidationException
from llm.llama import Llama
from tweet.tweet_repository import TweetRepository
from utils.json_utils import convert_json_str_to_json


class ConversationsService:
    def __init__(self):
        self.tweet_repository = TweetRepository()

    def analyze_company_conversations(self, db: Session, company_id):
        # Se buscan tweets enviados a una compañia
        sent_to_author = self.tweet_repository.get_tweets_sent_to_author(db, company_id)
        if not sent_to_author:
            return None
        # Se inicia llama y se crea prompt para obtener resultados.
        llama = Llama()
        user_message = "Check the following tweets and get the 5 most common topics and complains in a structured way:\n"
        tweet_messages = ""
        for tweet in sent_to_author:
            tweet_messages += "---------------------"
            tweet_messages += "\n" + str(tweet.tweet_id) + ": " + tweet.text + "\n"
        user_message += tweet_messages
        user_message += "\nMake it structured like a json, add to the json a top_5_topics, top_5_complains as a list of str, and then a dict named issues with the name of the every issue and inside a list of tweet_id in order to organize them. Just respond the json and nothing more."
        llama.add_user_message(user_message)
        content = llama.get_response()
        # Se parsea respuesta str a json para regresar al usuario y poder ser usada de mejor forma.
        response = convert_json_str_to_json(content)
        if not response:
            raise ValidationException("Llama JSON is invalid")
        issues = response.get("issues")
        if not issues:
            return response
        for key, value in issues.items():
            topic_tweets = issues[key]
            issues[key] = {"tweets": topic_tweets,
                           "percentage_of_tweets": len(topic_tweets) / len(sent_to_author)}
        return response
