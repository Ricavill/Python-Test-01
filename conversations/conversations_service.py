from requests import Session

from llm.llama import Llama
from tweet.tweet_repository import TweetRepository


class ConversationsService:
    def __init__(self):
        self.tweet_repository = TweetRepository()

    def build_conversation_map(self, tweets):
        """ Build a dictionary mapping tweet_id to its replies. """
        conversation_map = {tweet.tweet_id: [] for tweet in tweets}
        tweet_lookup = {tweet.tweet_id: tweet for tweet in tweets}

        for tweet in tweets:
            if tweet.in_response_to_tweet_id in conversation_map:
                conversation_map[tweet.in_response_to_tweet_id].append(tweet)

        return conversation_map, tweet_lookup

    def get_conversation(self, tweet_id, conversation_map, tweet_lookup, conversation=None):
        """ Recursively reconstructs a conversation thread in memory. """
        if conversation is None:
            conversation = []

        tweet = tweet_lookup.get(tweet_id)
        if not tweet:
            return conversation

        conversation.append(tweet)

        for reply in conversation_map.get(tweet_id, []):
            self.get_conversation(reply.tweet_id, conversation_map, tweet_lookup, conversation)

        return conversation

    def reconstruct_conversations(self, db: Session):
        """ Finds all root tweets and reconstructs their conversation threads in memory. """
        tweets = self.tweet_repository.get_all_orm(db)
        conversation_map, tweet_lookup = self.build_conversation_map(tweets)
        root_tweets = [tweet for tweet in tweets if tweet.in_response_to_tweet_id is None]

        conversations = []
        for tweet in root_tweets:
            conversation = self.get_conversation(tweet.tweet_id, conversation_map, tweet_lookup)
            conversation.sort(key=lambda x: x.created_at)  # Sort conversation by time
            conversations.append(conversation)

        return conversations

    def analyze_company_conversations(self, db: Session, company_id):
        sent_to_author = self.tweet_repository.get_tweets_sent_to_author(db, company_id)
        if not sent_to_author:
            return None
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
        response = llama.convert_json_str_to_json(content)
        issues = response.get("issues")
        if not issues:
            return response
        for key, value in issues.items():
            topic_tweets = issues[key]
            issues[key] = {"tweets": topic_tweets,
                           "percentage_of_tweets": len(topic_tweets) / len(sent_to_author)}
        return response
